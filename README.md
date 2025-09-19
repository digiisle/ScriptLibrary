# ScriptLibrary
常用脚本集，不定期更新。

## huaweicloud_ddns
监控设备IP地址是否发生变化，若发生变化则同步将华为云上的DNS解析地址修改为新地址，并邮件通知。

## ipChangeMonitoring
通过python脚本定时监控检查主机公网IP地址是否发生改变，若发生改变，则通过邮件方式发送通知。

### 使用方式
### 文件下载到本地目录下
[下载地址](https://github.com/ErickQian/ipChangeMonitoring/archive/refs/heads/master.zip)  
下载解压到最终运行目录，如`/opt/ipChangeMonitoring/`下；
### 修改自定义参数
修改`send_email`函数对应内容
```python
def send_email(new_public_ip, old_public_ip):
    """发送邮件"""
    mail_host = 'smtp.qq.com'  # 邮箱服务器
    mail_user = '******@qq.com'  # 用户名
    mail_auth = '******'  # 授权码
    sender = '******@qq.com'  # 邮件发送方邮箱
    # 邮件接收方邮箱地址，可以写多个邮件地址进行群发
    receivers = ['******@qq.com']
    # 设置email信息：邮件内容设置
    new_public_ip = "The new IP address is："+new_public_ip+'\r'
    old_public_ip = "The old IP address is："+old_public_ip
    content = new_public_ip+old_public_ip
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = '[warning]ip address has been changed'  # 邮件头
    message['From'] = sender  # 发送人
    message['To'] = receivers[0]  # 收件人
```  

修改`save_public_ip`和`read_old_public_ip`函数对应内容
```python
def save_public_ip():
    """
    获取公网地址
    保存到文件
    """
    # 获取公网IP
    public_ip = getIPv6Address()
    # 实际使用时填写根目录"/opt/ipChangeMonitoring/ipChangeMonitoring.log"
    file = open("/opt/ipChangeMonitoring/ipChangeMonitoring.log", 'w')
    file.write(public_ip)
    file.close()
def read_old_public_ip():
    """
    读取上一次执行获取到的公网IP
    """
    # 实际使用时填写根目录"/opt/ipChangeMonitoring/ipChangeMonitoring.log"
    filename = '/opt/ipChangeMonitoring/ipChangeMonitoring.log'
    old_public_ip = linecache.getline(filename, 1)
    return (old_public_ip)
```
### linux创建定时任务
将`ipChangeMonitoring.service`和`ipChangeMonitoring.timer`复制到`/etc/systemd/system/`目录下，并执行`systemctl daemon-reload`  
启动定时器`systemctl start ipChangeMonitoring.timer`  
设置为开机自启`systemctl enable ipChangeMonitoring.timer`  
查看所有已启用的定时器`systemctl list-timers`

## iptool
IP地址计算器
```bash
>iptool
欢迎使用本程序！
输入 'quit' 退出程序，按 Ctrl+C 强制退出。
请输入IP/mask or IP/subnet：
192.168.1.0/24
**************************************************
IP版本号： 4
是否是私有地址： true
网络号： 192.168.1.0
前缀长度： 24
子网掩码： 255.255.255.0
IP地址总数: 256
可用IP地址总数： 254
起始可用IP地址： 192.168.1.1
最后可用IP地址： 192.168.1.254
可用IP地址范围： 192.168.1.1 ~ 192.168.1.254
广播地址： 192.168.1.255
**************************************************
请输入IP/mask or IP/subnet：
192.168.1.1/255.255.255.0
**************************************************
IP版本号： 4
是否是私有地址： true
网络号： 192.168.1.0
前缀长度： 24
子网掩码： 255.255.255.0
IP地址总数: 256
可用IP地址总数： 254
起始可用IP地址： 192.168.1.1
最后可用IP地址： 192.168.1.254
可用IP地址范围： 192.168.1.1 ~ 192.168.1.254
广播地址： 192.168.1.255
**************************************************
请输入IP/mask or IP/subnet：

Bye! Hope to see you again!
```