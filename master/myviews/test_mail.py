# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender = 'shengbo@starmerx.com'
receivers = ['yakai@starmerx.com','yuanmin@starmerx.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# receivers = ['happybebe@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("王胜波", 'utf-8')
message['To'] = Header("test", 'utf-8')
subject = '东莞vip，西雅图库存数据'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('请见附件', 'plain', 'utf-8'))

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('/home/winbo/djang_poj/wms/master/myviews/report.xls', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="report.xls"'
message.attach(att1)

# 构造附件2，传送当前目录下的 runoob.txt 文件
# att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
# att2["Content-Type"] = 'application/octet-stream'
# att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
# message.attach(att2)

try:
    smtpObj = smtplib.SMTP('smtp.exmail.qq.com',25)
    smtpObj.login('shengbo@starmerx.com','nVuc7Uohpirvcunf')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException:
    print "Error: 无法发送邮件"