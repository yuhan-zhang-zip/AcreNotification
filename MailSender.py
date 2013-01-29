#-*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import json
from ContentGetter import getThreadContent

def _getMailContent(itemlist):
    # Get template
    mainFile = open("/home/rainite/public_html/static/report.html")
    mainTemplate = unicode(mainFile.read(), 'utf-8')
    threadFile = open("/home/rainite/public_html/static/accordiongroup.html")
    threadTemplate = unicode(threadFile.read(), 'utf-8')
    mainFile.close()
    threadFile.close()

    accordionStr = ""
    for item in itemlist:
        threadRawContent = getThreadContent(item)
        accordion = threadTemplate % (item.link, item.title ,threadRawContent)
        accordionStr += accordion + "<hr>"
    return mainTemplate % accordionStr

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
            continue
        to_addrs = mailStr.split(' ')
        
        html = _getMailContent(itemlist)
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
