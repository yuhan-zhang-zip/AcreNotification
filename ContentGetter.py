#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import cPickle
import re
from PathResolver import getAbsoluteDir
import os

class Item:
	pass


def _getResultDictFromRawContent(content):
	'''
	Form raw content into result dict
	@param content: raw content of html, 
    @return resultDict{"major": itemlist} 
    '''
	absoluteDir = getAbsoluteDir()
	# Get thread counter from cPickle
	tfilePath = os.path.join(absoluteDir, "threadCounter.pkl")
	threadFile = open(tfilePath, "r")
	threadCounter = cPickle.load(threadFile)
	soup = BeautifulSoup(content)
	# find tbodylist <tag>
	tbodylist = soup.find(summary="forum_82").find_all(id = re.compile("normalthread"))
	# filter the newest tbody
	newTbodyList = [tbody for tbody in tbodylist if int(tbody["id"].split("_")[1]) > threadCounter]
	threadnumberList = [int(tbody["id"].split("_")[1]) for tbody in newTbodyList]
	# no new thread
	if len(threadnumberList) == 0:
		return None
	latestThread = max(threadnumberList)
	# Update latest thead
	threadFile = open(tfilePath, "w")
	cPickle.dump(latestThread, threadFile)
	threadFile.close()

	resultDict = dict()
	for tbody in newTbodyList:
		a = tbody.find_all("a")[2]
		item = Item()
		item.title = a.string
		item.link = a["href"]
		major = tbody.find(color="#F60").string
		if(resultDict.has_key(major)):
			resultDict[major].append(item)
		else:
			resultDict[major] = [item]
	return resultDict

def getRawContent(url):
	'''
	Get raw unicode content from a specified url
	@param url
	'''
	opener = urllib2.build_opener()
	# To deceive the website with cookie
	# It may be outdated oneday, update regularly
	opener.addheaders.append(('Cookie', "4Oaf_61d6_saltkey=wBRs2tE2; 4Oaf_61d6_lastvisit=1357873653; 4Oaf_61d6_auth=230dpz2iNfsAwUq3GbHmYonVJ8Y6ICuprhktjoDHz4LDzFqbdvhWrrejSsGNZyUKoP7o%2F21Rvviodyo8NrN6VEUfnA; jiathis_rdc=%7B%22http%3A//www.1point3acres.com/bbs/thread-47382-1-1.html%22%3A668350534%2C%22http%3A//www.1point3acres.com/bbs/thread-47382-3-1.html%22%3A668436777%2C%22http%3A//www.1point3acres.com/bbs/thread-47677-1-1.html%22%3A1021709071%2C%22http%3A//www.1point3acres.com/bbs/thread-47672-1-1.html%22%3A1021815771%2C%22http%3A//www.1point3acres.com/bbs/thread-47675-1-1.html%22%3A1022041863%2C%22http%3A//www.1point3acres.com/bbs/thread-47678-1-1.html%22%3A1023877426%2C%22http%3A//www.1point3acres.com/bbs/thread-44458-1-1.html%22%3A1025190747%2C%22http%3A//www.1point3acres.com/bbs/thread-47674-1-1.html%22%3A1027612369%2C%22http%3A//www.1point3acres.com/bbs/thread-47667-1-1.html%22%3A1028163412%2C%22http%3A//www.1point3acres.com/bbs/thread-47690-1-1.html%22%3A1028224749%2C%22http%3A//www.1point3acres.com/bbs/thread-47739-1-1.html%22%3A1107886028%2C%22http%3A//www.1point3acres.com/bbs/thread-47773-1-1.html%22%3A1108134743%2C%22http%3A//www.1point3acres.com/bbs/thread-45762-1-1.html%22%3A1108182358%2C%22http%3A//www.1point3acres.com/bbs/thread-45762-7-1.html%22%3A1108192931%2C%22http%3A//www.1point3acres.com/bbs/thread-47644-1-1.html%22%3A1111497172%2C%22http%3A//www.1point3acres.com/bbs/thread-47940-1-1.html%22%3A1297254606%2C%22http%3A//www.1point3acres.com/bbs/thread-47482-1-1.html%22%3A1297266749%2C%22http%3A//www.1point3acres.com/bbs/thread-3722-2-1.html%22%3A1299963735%2C%22http%3A//www.1point3acres.com/bbs/thread-3545-1-1.html%22%3A1300004213%2C%22http%3A//www.1point3acres.com/bbs/thread-47883-1-1.html%22%3A1300178075%2C%22http%3A//www.1point3acres.com/bbs/thread-21158-1-1.html%22%3A1300276841%2C%22http%3A//www.1point3acres.com/bbs/thread-38881-1-1.html%22%3A1300345111%2C%22http%3A//www.1point3acres.com/bbs/thread-2612-1-1.html%22%3A1300398572%2C%22http%3A//www.1point3acres.com/bbs/thread-18629-1-1.html%22%3A1300441519%2C%22http%3A//www.1point3acres.com/bbs/thread-44076-1-1.html%22%3A1300745128%2C%22http%3A//www.1point3acres.com/bbs/thread-36722-1-1.html%22%3A1300788251%2C%22http%3A//www.1point3acres.com/bbs/thread-41512-1-1.html%22%3A1300866076%2C%22http%3A//www.1point3acres.com/bbs/thread-47613-1-1.html%22%3A1303828118%2C%22http%3A//www.1point3acres.com/bbs/thread-47613-4-1.html%22%3A1303861383%2C%22http%3A//www.1point3acres.com/bbs/thread-40247-1-1.html%22%3A1303895252%2C%22http%3A//www.1point3acres.com/bbs/thread-47962-1-1.html%22%3A1303945769%2C%22http%3A//www.1point3acres.com/bbs/thread-47706-1-1.html%22%3A1303980886%2C%22http%3A//www.1point3acres.com/bbs/thread-48064-1-1.html%22%3A1549376342%2C%22http%3A//www.1point3acres.com/bbs/thread-47981-1-1.html%22%3A1549423059%2C%22http%3A//www.1point3acres.com/bbs/thread-47922-1-1.html%22%3A1550279417%2C%22http%3A//www.1point3acres.com/bbs/thread-47688-1-1.html%22%3A1550335516%2C%22http%3A//www.1point3acres.com/bbs/thread-47825-1-1.html%22%3A1550370541%2C%22http%3A//www.1point3acres.com/bbs/thread-48125-1-1.html%22%3A1550428319%2C%22http%3A//www.1point3acres.com/bbs/thread-48007-1-1.html%22%3A1552073817%2C%22http%3A//www.1point3acres.com/bbs/thread-47464-1-1.html%22%3A1552125231%2C%22http%3A//www.1point3acres.com/bbs/thread-47027-1-1.html%22%3A1552190994%2C%22http%3A//www.1point3acres.com/bbs/thread-3722-1-1.html%22%3A1555494979%2C%22http%3A//www.1point3acres.com/bbs/thread-3873-1-1.html%22%3A1555581236%2C%22http%3A//www.1point3acres.com/bbs/thread-5529-1-1.html%22%3A1555610857%2C%22http%3A//www.1point3acres.com/bbs/thread-1893-1-1.html%22%3A1555645703%2C%22http%3A//www.1point3acres.com/bbs/thread-33495-1-1.html%22%3A1555820549%2C%22http%3A//www.1point3acres.com/bbs/thread-32353-1-1.html%22%3A1555886737%2C%22http%3A//www.1point3acres.com/bbs/thread-32373-1-1.html%22%3A1555926966%2C%22http%3A//www.1point3acres.com/bbs/thread-29657-1-1.html%22%3A1555993733%2C%22http%3A//www.1point3acres.com/bbs/thread-4543-1-1.html%22%3A1556093427%2C%22http%3A//www.1point3acres.com/bbs/thread-4545-1-1.html%22%3A2%7C1358765791853%2C%22http%3A//www.1point3acres.com/bbs/thread-23489-1-1.html%22%3A%220%7C1358766693194%22%7D; 4Oaf_61d6_viewuids=574_1578_66856_3048_250_672_15404_4748; 4Oaf_61d6_home_diymode=1; 4Oaf_61d6_forum_lastvisit=D_125_1358513610D_82_1358948874; 4Oaf_61d6_visitedfid=82D41D71D28D27D144D70D125D73D92; 4Oaf_61d6_nofocus_19=1; 4Oaf_61d6_smile=4D1; 4Oaf_61d6_onlineusernum=207; 4Oaf_61d6_sid=R05ks0; 4Oaf_61d6_ulastactivity=cba8u6Wd2INNwNDkrfHOaie0wbSP6JcEUNrUW95LmijmtOhRX%2BWw; __utma=142000562.59071019.1357877254.1358948860.1358991070.16; __utmb=142000562.1.10.1358991070; __utmc=142000562; __utmz=142000562.1358767391.14.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); 4Oaf_61d6_checkpm=1; 4Oaf_61d6_lastact=1358991073%09home.php%09misc; 4Oaf_61d6_sendmail=1"))
	reader = opener.open(url)
	content = reader.read()
	reader.close()
	# unicodify content
	return unicode(content, 'gbk')
	

def getThreadContent(item):
	'''
	Get specific thead content of the item
    @param item
    '''
	title = item.title
	link  = item.link
	unicontent = getRawContent(link)
	soup = BeautifulSoup(unicontent)
	return unicode(soup.find(id="JIATHIS_CODE_HTML4"))


def getMainContent():
	''' Get content from report page
	    form an result dict major -> itemlist
	'''
	unicontent =  getRawContent("http://www.1point3acres.com/bbs/forum-82-1.html")
	resultDict = _getResultDictFromRawContent(unicontent)
	return resultDict

