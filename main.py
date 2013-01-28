from MailSender import *
from ContentGetter import *

if __name__ == '__main__':
	resultDict = getContent()
	sendMail(resultDict)
