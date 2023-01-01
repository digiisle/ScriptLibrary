import linecache
import smtplib
from email.mime.text import MIMEText
from json import load
from urllib.request import urlopen


def send_email(new_public_ip, old_public_ip):
    """发送邮件"""
    mail_host = 'smtp.qq.com'  # 邮箱服务器
    mail_user = 'xxx@qq.com'  # 用户名
    mail_auth = 'xxxxxxxxxxxxxxxxxxxxxx'  # 授权码
    sender = 'xxx@qq.com'  # 邮件发送方邮箱
    # 邮件接收方邮箱地址，注意需要[]包裹，可以写多个邮件地址进行群发
    receivers = ['xxx@outlook.com']
    # 设置email信息：邮件内容设置
    new_public_ip = "The new IP address is："+new_public_ip+'\r'
    old_public_ip = "The old IP address is："+old_public_ip
    content = new_public_ip+old_public_ip
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = '[warning]ip address has been changed'  # 邮件头
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


def compare_public_ip():
    """
    获取公网地址
    与上一次执行保存的公网IP对比
    """
    # 实时获取公网IP

    public_ip = load(urlopen('https://api.erickqian.top/getip/'))['ip']
    # 读取上一次执行保存的公网IP
    filename = '/opt/scriptlibrary/ipChangeMonitoring.log'
    old_public_ip = linecache.getline(filename, 1)
    if old_public_ip.strip() == public_ip.strip():
        pass
    else:
        # 调用发送邮件函数
        send_email(public_ip, old_public_ip)
        # 实时获取公网IP
        public_ip = load(urlopen('https://api.erickqian.top/getip/'))['ip']
        file = open("/opt/scriptlibrary/ipChangeMonitoring.log", 'w')
        file.write(public_ip)
        file.close()


if __name__ == "__main__":
    try:
        # 对比两次获取到的结果
        compare_public_ip()
    except Exception as result:
        print(result)
