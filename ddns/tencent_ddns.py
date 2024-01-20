# coding = utf-8
import json
import linecache
import smtplib
import os
import re
import time
import requests
from email.mime.text import MIMEText
from json import load
from urllib.request import urlopen
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models


def save_public_ip(public_ip):
    """
    获取公网地址
    保存获取到的公网IP
    """
    file = open("./tencent_ddns.log", 'w')
    file.write(public_ip)
    file.close()

def getIPv6Address():
    getIPV6 = os.popen("ip addr show")
    output = str(getIPV6.read())
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

def compare_public_ip():
    """
    获取公网地址
    与实时获取的公网IP对比
    """
    # 读取上一次执行后保存的公网IP
    filename = './tencent_ddns.log'
    old_public_ip = linecache.getline(filename, 1)
    # 实时获取公网IP
    public_ip = getIPv6Address()
    if old_public_ip.strip() == public_ip.strip():
        pass
    else:
        # 执行更新
        setIp(public_ip)


def setIp(public_ip):
    """
    更新域名解析
    """
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential("SecretId", "SecretKey")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ModifyRecordRequest()
        params = {
            "Domain": "disle.com.cn",
            "SubDomain": "www",
            "RecordType": "AAAA",
            "RecordLine": "默认",
            "Value": public_ip,
            "RecordId": 1706991124,
            "Remark": "Automatically"
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
        resp = client.ModifyRecord(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        # 调用发送邮件函数
        Content = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+' ' + '\r'+'域名'+"pc.digiisle.com.cn"+'的DNS解析已更新。'+'\r'+'更新后的IP地址为：'+public_ip+'\r'+"接口返回信息："+'\r'+resp.to_json_string()
        send_email(Content)
        # 存储本次更新的ip用于比较
        save_public_ip(public_ip)

    except TencentCloudSDKException as err:
        print(err)

def send_email(Content):
    """发送邮件"""
    mail_host = 'smtp.qq.com'  # 邮箱服务器
    mail_user = 'xxx@qq.com'  # 用户名
    mail_auth = 'xxx'  # 授权码
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
    try:
        # 对比两次获取到的结果
        compare_public_ip()
    except Exception as result:
        print(result)
