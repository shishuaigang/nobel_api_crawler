# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import smtplib
import get_git_log


class send_mail:
    def __init__(self, rec_list, mail_subject, t):
        self.receiver = rec_list
        self.mail_subject = mail_subject
        self.t = t

    def send_mail(self):
        try:  # 判定是否存在temp.html，如没有，则抛出异常
            gitlog = get_git_log.gitlog()
            os.chdir(r"Test_results")
            os.rename('temp.html', 'TestReport_' + self.t + '.html')
            # 定义发件人邮箱，密码和收件人的list
            sender = 'sgshi@in-road.com'
            passwd = 'Shishuaigang123!'
            msg = MIMEMultipart()
            msg["Subject"] = self.mail_subject  # 邮件主题
            msg["From"] = sender
            msg["To"] = ','.join(self.receiver)  # 收件人邮箱列表，以逗号分隔
            #  邮件正文
            part_con = MIMEText(
                "Hi all,\nThis is the test report for " + self.mail_subject + "\n\nlast commit: " + gitlog, 'plain',
                'utf-8')
            msg.attach(part_con)  # 邮件添加正文
            part_attach = MIMEApplication(open('TestReport_' + self.t + '.html', 'rb').read())
            part_attach.add_header('Content-Disposition', 'attachment', filename='TestReport_' + self.t + '.html')
            msg.attach(part_attach)  # 邮件添加附件
            s = smtplib.SMTP("smtp.exmail.qq.com", timeout=30)  # 连接邮件服务器
            s.login(sender, passwd)  # 登录服务器
            s.sendmail(sender, self.receiver, msg.as_string())  # 发送邮件
            s.close()
        except IOError as e:
            print "Please check the file 'temp.html' exist or not"
