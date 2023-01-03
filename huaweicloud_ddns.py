# coding = utf-8
import json,linecache,smtplib,ssl,time,requests
from email.mime.text import MIMEText
from json import load
from urllib.request import urlopen

# ddns解析域名
domain = 'yogknight.top'
# 华为云账号
name = 'yogknight'
# 华为云密码
password = 'xxxxxxxxxxxxxxxxxxxxxx'
# 进入管理控制台\我的凭证 选择一个项目名称
scopeName = 'cn-southwest-2'
# 进入https://support.huaweicloud.com/api-dns/dns_api_62002.html查看获取zoneid
zone_id = 'xxxxxxxxxxxxxxxxxxxxxx'
# 首次运行不填写 运行一次后会在在控制台打印出值
recordset_id = 'xxxxxxxxxxxxxxxxxxxxxx'


def save_public_ip(public_ip):
    """
    获取公网地址
    保存获取到的公网IP
    """
    file = open("/opt/scriptlibrary/huaweicloud_ddns.log", 'w')
    file.write(public_ip)
    file.close()


def compare_public_ip():
    """
    获取公网地址
    与实时获取的公网IP对比
    """
    # 读取上一次执行后保存的公网IP
    filename = '/opt/scriptlibrary/huaweicloud_ddns.log'
    old_public_ip = linecache.getline(filename, 1)
    # 实时获取公网IP
    ssl._create_default_https_context = ssl._create_unverified_context
    public_ip = load(urlopen('https://api.erickqian.top/getip/'))['ip']
    if old_public_ip.strip() == public_ip.strip():
        pass
    else:
        # 执行更新
        setIp(public_ip)


def setIp(public_ip):
    """
    获取token
    """
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": name
                        },
                        "name": name,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "name": scopeName
                }
            }
        }
    }
    headers['Content-Type'] = 'application/json'
    res = requests.post(
        url=getTokenUrl, data=json.dumps(data), headers=headers)
    status_code = str(res.status_code)
    if status_code != '201':
        print(res.text)
        print('请查阅https://support.huaweicloud.com/api-iam/iam_30_0001.html获取错误详情')
        return

    # 设置token
    token = res.headers['X-Subject-Token']
    headers['x-auth-token'] = token

    # 获取解析id
    if recordset_id == '':
        res = requests.get(url=getRecordsetUrl,
                           data=json.dumps(data), headers=headers)
        if len(res.json()['recordsets']) == 0:
            print('请登录域名管理后台添加 %s 的A记录解析' % domain)
        else:
            print('%s 的id为:' % domain, res.json()[
                  'recordsets'][0]['id'], '请写入recordset_id字段中')
        return

    # 更新解析
    data = {
        "name": "yogknight.top.",
        "description": "Automation scripts to update",
        "type": "AAAA",
        "ttl": 3600,
        "records": [
            public_ip
        ]
    }
    res = requests.put(url=domainUrl, data=json.dumps(data), headers=headers)
    # print(res.text)
    #print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()), 'ip已更新', public_ip)
    Content = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+' ' + \
        '域名'+domain+'的DNS解析已更新。'+'\r'+'更新后的IP地址为：'+public_ip+'\r'+res.text
    # 调用发送邮件函数
    send_email(Content)
    # 存储本次更新的ip用于比较
    save_public_ip(public_ip)


def send_email(Content):
    """发送邮件"""
    mail_host = 'smtp.qq.com'  # 邮箱服务器
    mail_user = 'xxx@qq.com'  # 用户名
    mail_auth = 'xxxxxxxxxxxxxxxxxxxxxx'  # 授权码
    sender = 'xxx@qq.com'  # 邮件发送方邮箱
    # 邮件接收方邮箱地址，注意需要[]包裹，可以写多个邮件地址进行群发
    receivers = ['xxx@outlook.com']
    # 设置email信息：邮件内容设置
    content = Content
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = '[info]DNS resolution has been updated automatically'  # 邮件头
    message['From'] = sender  # 发送人
    message['To'] = receivers[0]  # 收件人
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 链接服务器
        smtpObj.login(mail_user, mail_auth)  # 登录
        # 发送邮件
        smtpObj.sendmail(
            sender, receivers, message.as_string()
        )
        smtpObj.quit()  # 关闭连接
    except smtplib.SMTPException as e:
        print('error', e)


if __name__ == "__main__":
    getTokenUrl = "https://iam.myhuaweicloud.com/v3/auth/tokens?nocatalog=true"
    getRecordsetUrl = "https://dns.myhuaweicloud.com/v2/recordsets?&type=A&name=%s" % domain
    domainUrl = 'https://dns.myhuaweicloud.com/v2/zones/%s/recordsets/%s' % (
        zone_id, recordset_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    try:
        # 对比两次获取到的结果
        compare_public_ip()
    except Exception as result:
        print(result)
