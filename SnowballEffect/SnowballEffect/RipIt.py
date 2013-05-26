import sys
import os
import urllib2
from HTMLParser import HTMLParser
from os.path import join

class DotaHtmlParser(HTMLParser):
    def handle_data(self, data):
        global currentTag  
        global matchList
        global foundCharacter
        global currentMatch
        if(characterSearch == ""):
	        if(currentTag == "matches"):
	        	if(data != "The International" and data != "Dreamhack"):
	        		matchList.append(data)
       	if(currentTag == "matches"): 
       		currentMatch = data
        currentTag = "null"	
    def handle_starttag(self, tag, attrs):
        global currentTag
        global foundCharacter
        global currentMatch
        global matchList
        if(tag == 'a'):
            for element in attrs:
                if(element[0] == 'href'):
                    if("/matches/" in element[1]):
                    	currentTag = "matches"
        if(tag == "img" and characterSearch != ""):
        	for element in attrs:
        		if(element[0] == 'alt' and characterSearch == element[1]):
                            if(currentMatch not in matchList):
                                matchList.append(currentMatch)
                                currentMatch = ""
                                print element[1]
    def handle_endtag(self, tag):
        if(tag == 'img'):
            currentTag = 'null'
        if(tag == 'a'):
            currentTag = 'null'

global currentTag
global currentMatch
global foundCharacter
global characterSearch

global matchList

characterSearch = "null"
matchList = list()

characterSearch = raw_input("Please enter in a character you wish to search for: ")

currentTag = 0

url = "http://dotabuff.com/matches/"
page = urllib2.urlopen(url)
data = page.read()

parser = DotaHtmlParser()

parser.feed(data)

page.close()

for x in range(2,21):
	url = "http://dotabuff.com/matches?page" + str(x)
	page = urllib2.urlopen(url)
	data = page.read()

	parser.feed(data)

	page.close()


for e in matchList:
    print e

print("finish")

raw_input()