#-*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import json

def sendMail(resultDict):
    # mail account info
    mail_username='njuprincerain@gmail.com'
    mail_password='NJUprince'
    from_addr = 'njuprincerain@gmail.com'
    to_addrs= []

    # HOST & PORT
    HOST = 'smtp.gmail.com'
    PORT = 587

    message = MIMEMultipart('alternative')
    message['Subject'] = u'来自地里的战报'
    message['From'] = from_addr

    # get maillist
    mailFile = open("emailList.json", 'r')
    emailDict = json.loads(mailFile.read())
    mailFile.close()

    for major, itemlist in resultDict.iteritems():
        mailStr = emailDict[major]
        if len(mailStr) == 0:
            break
        to_addrs = mailStr.split(' ')
        htmlLinkList = u""
        for item in itemlist:
            htmlLinkList += '''
            <a href = "%s">%s</a>
            </br>
            ''' % (item.link, item.title)

        html = u'''
        <html>
            <head>
                <title>Notification</title>
            </head>
            <body>
                <h1>1point3acre Notification</h1>
                <p>
                %s
                </p>
            </body>
        </html>
        ''' % htmlLinkList
        mimetext = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
        message.attach(mimetext)
        msgstr = message.as_string()

        session = smtplib.SMTP(HOST, PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(mail_username, mail_password)
        session.sendmail(from_addr, to_addrs, msgstr)
        sleep(5)
        session.quit()