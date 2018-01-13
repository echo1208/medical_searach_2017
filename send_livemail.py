import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

def sendmail(word):
    now = datetime.datetime.now()
    strnow = "{0:%Y年%m月%d日}".format(now)
    smtpserver = 'smtp.live.com'
    username = 'XXXXXXXXX@hotmail.com'  # for SMTP AUTH, set SMTP username here
    password = 'XXXXXXXX'  # for SMTP AUTH, set SMTP password here
    titletext = "{0}のPubmedから引用した『{1}』関連記事".format(strnow,word)
    bodyPath = "body.txt".replace("/", os.sep)
    msg = open(bodyPath)
    body = msg.read()
    msg.close()
    sender = "XXXXXXXXXXX"
    recepient = 'XXXXXXXXXXXXX'

    msg = MIMEText(body)
    # msg = EmailMessage(body)
    msg['Subject'] = titletext
    msg['From'] = sender
    msg['To'] = recepient
    # msg.add_attachment("cloudfront.log")

    server = smtplib.SMTP(smtpserver,587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.set_debuglevel(1)
    server.send_message(msg)
    server.close()

    print("message successfully sent")
