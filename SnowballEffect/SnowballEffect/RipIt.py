import sys
import os
import urllib2
from HTMLParser import HTMLParser
from os.path import join

class DotaHtmlParser(HTMLParser):
    def handle_data(self, data):
        global currentTag
        global currentTeam   
        global matchList
        if(currentTag == "matches"):
        	if(data != "The International" and data != "Dreamhack"):
        		matchList.append(data)
        currentTag = "null"	
    def handle_starttag(self, tag, attrs):
        global currentTag
        global currentTeam
        global i
        if(tag == 'a'):
            for element in attrs:
                if(element[0] == 'href'):
                    if("/matches/" in element[1]):
                    	currentTag = "matches"

    def handle_endtag(self, tag):
        if(tag == 'section'):
            currentTag = 'null'
        if(tag == 'a'):
            currentTag = 'null'

global currentTag
global currentTeam

global matchList
matchList = list()

currentTag = 0

url = "http://dotabuff.com/matches/"
page = urllib2.urlopen(url)
data = page.read()

parser = DotaHtmlParser()

parser.feed(data)

for x in range(2,21):
	url = "http://dotabuff.com/matches?page" + str(x)
	page = urllib2.urlopen(url)
	data = page.read()

	parser = DotaHtmlParser()

	parser.feed(data)

	page.close()
	print (x)

for e in matchList:
	print e

raw_input()