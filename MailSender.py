#-*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

def sendMail(itemlist):
    if len(itemlist) == 0:
        return
	# my test mail
    mail_username='njuprincerain@gmail.com'
    mail_password='NJUprince'
    from_addr = 'njuprincerain@gmail.com'
    to_addrs= ['njuprincerain@gmail.com']

	# HOST & PORT
    HOST = 'smtp.gmail.com'
    PORT = 587

    message = MIMEMultipart('alternative')
    message['Subject'] = u'来自地里的战报'
    message['From'] = from_addr

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
