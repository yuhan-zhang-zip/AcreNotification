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
	opener.addheaders.append(('Cookie', "<user token>"))
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

