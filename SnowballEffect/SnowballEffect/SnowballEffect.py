import json
import sys
import os
import urllib2
from HTMLParser import HTMLParser
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import operator

class Game:
    def __init__(self, characters, number, gameWinner):
        self.characters = characters
        self.gameNumber = number
        self.winner = gameWinner
class Character:
    """Simple character class for the storing of values"""
    def __init__(self):
        self.goldList = list()
        self.levelUpTimes = list()
        self.kills = list()
        self.items = list()
        self.name = ""
        self.team = ""
        self.scalingGold = list()

class Gold:
    def __init__(self, gold, gameTime):
        self.amount = gold
        self.time = gameTime

class LevelUp:
    def __init__(self, currentLevel, gameTime):
        self.time = gameTime
        self.level = currentLevel

class Kill:
    def __init__(self, time, dead):
        self.time = time
        self.killed = dead

class Item(object):
    """docstring for ClassName"""
    def __init__(self, name, time):
        self.name = name
        self.time = time

class PlotIt:
    def __init__(self):
        self.time = list()
        self.amount = list()
        self.ymin = list()
        self.ymax = list()

class DotaHtmlParser(HTMLParser):
    def handle_data(self, data):
        global currentTag
        global currentTeam
        if(currentTag == "hero"):
            data = data.replace(' ', '_')
            data = data.lower()
            data = "npc_dota_hero_" + data
            for c in characterList:
                if(c.name == data):
                    c.team = currentTeam    
        currentTag = "null"
    def handle_starttag(self, tag, attrs):
        global currentTag
        global currentTeam
        global gameWinner
        if(tag == 'section'):
            for element in attrs:
                if(element[0] == 'class'):
                    if(element[1] == 'radiant'):
                        currentTeam = 'radiant'
                    if(element[1] == 'dire'):
                        currentTeam = 'dire'
        if(tag == 'a'):
            for element in attrs:
                if(element[0] == 'class'):
                    if(element[1] == 'hero-link'):
                        currentTag = "hero"
        if(tag == 'span'):
            for element in attrs:
                if(element[0] == 'class'):
                    if(element[1] == 'team dire'):
                        gameWinner = 'Dire'
                    if(element[1] == 'team radiant'):
                        gameWinner = 'Radiant'
    def handle_endtag(self, tag):
        if(tag == 'section'):
            currentTag = 'null'
        if(tag == 'a'):
            currentTag = 'null'

def myround(x, base=5):
    return int(base * round(float(x)/base))

global currentTag
global currentTeam
global gameWinner

gameList = list()

print "Please press one of the following to generate charts for Dota 2. After selecting your option, please press the enter key"
print "1. Levels and Gold gained over the course of the game for all games"
print "2. Same as option 1 but for a single game."
print "3. Varience for players to be plotted"

option = raw_input()

if(option == '2'):
    print "Please enter in the game that you would like to look at"
    chosenGame = raw_input()

for root, direc, files in os.walk(os.getcwd()):
    for d in direc:
        print d
        currentTag = "test"
        currentTeam = "temp"

        goldFile = open(d + '\gold.json', 'r')
        levelUpFile = open(d + '\levelups.json', 'r')
        killsFile = open(d + '\herokills.json', 'r')
        itemsFile = open(d  + '\itemtimes.json', 'r')

        goldFileJson = goldFile.read()
        levelFileJson = levelUpFile.read()
        killsFileJson = killsFile.read()
        itemsFileJson = itemsFile.read()

        obj = json.loads(goldFileJson)
        obj2 = json.loads(levelFileJson)
        obj3 = json.loads(killsFileJson)
        obj4 = json.loads(itemsFileJson)

        characterList = list()
        characterTracker = Character()

        for o in obj['gold']:
            if(characterTracker.name == ""):
                characterTracker.name = o['hero']
                characterTracker.goldList.append(Gold(o['gold'], o['time']/30))
            if(characterTracker.name == o['hero']):
                characterTracker.goldList.append(Gold(o['gold'], o['time']/30))
            else:
                characterList.append(characterTracker)
                characterTracker = Character()

        characterList.append(characterTracker)

        for char in characterList:
            for o in obj2['leveluptimes']:
                if(char.name == o['hero']):
                    char.levelUpTimes.append(LevelUp(o['level'], o['time']/30))

        for char in characterList:
            for o in obj3['herokills']:
                if(char.name == o['killer']):
                    char.kills.append(Kill(o['time']/30, o['dead']))

        for char in characterList:
            for o in obj4['itemtimes']:
                    if(char.name == o['hero']):
                        char.items.append(Item(o['item'], o['time']/30))

        url = "http://dotabuff.com/matches/" + d
        page = urllib2.urlopen(url)
        data = page.read()

        parser = DotaHtmlParser()

        parser.feed(data)

        yAxis = 0
        yAxisGold = 0

        if(option == '1'):
            for each in characterList:
                for level in each.levelUpTimes:
                    if(level.level > yAxis):
                        yAxis = level.level
                if(len(each.kills) > yAxis):
                    yAxis = len(each.kills)
                overallGold = each.goldList[0].amount
                for gold in each.goldList:
                    overallGold += gold.amount
                if(overallGold > yAxisGold):
                    yAxisGold = overallGold               

            for each in characterList:
                fig = plt.figure(each.name + each.team + d + "Gold")
                ax = plt.subplot(111)
                plt.title(each.name)
                plt.xlabel("Time")
                plt.ylabel("Amount")
                goldArray = []
                timeArray = []

                scalingAmount = each.goldList[0].amount

                for gold in each.goldList:
                    goldArray.append(scalingAmount)
                    timeArray.append(gold.time)
                    scalingAmount += gold.amount

                plot1, = plt.plot(timeArray, goldArray, 'bo', linestyle = '-')
                plt.ylim([0,yAxisGold + 100])
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                ax.legend([plot1], ["Gold"], loc='center left', bbox_to_anchor=(1,0.5))
                plt.savefig(d + '/' + each.name + '_' + each.team + "_gold.png")
                
                fig = plt.figure(each.name + each.team + d + "Progression")
                ax = plt.subplot(111)
                plt.title(each.name)
                plt.xlabel("Time")
                plt.ylabel("Amount")
                timeArray = []
                levelArray = []
                for level in each.levelUpTimes:
                    timeArray.append(level.time)
                    levelArray.append(level.level)
                    if(level.level == 6):
                        plt.axvline(level.time)
                    if(level.level == 11):
                        plt.axvline(level.time)
                    if(level.level == 16):
                        plt.axvline(level.time)
                plot2, = plt.plot(timeArray, levelArray, 'go', linestyle = '-')
                timeArray = []
                killsArray = []
                for kill in each.kills:
                    timeArray.append(kill.time)
                    killsArray.append(each.kills.index(kill) + 1)
                plot3, = plt.plot(timeArray, killsArray, 'ro', linestyle = '-')
                timeArray = []
                itemArray = []
                for item in each.items:
                    timeArray.append(item.time)
                    itemArray.append(1)
                    print each.name, item.name
                    if(each.name == 'npc_dota_hero_nyx_assassin' and item.name == 'modifier_item_dagon'):
                        plt.axvline(item.time, color='r')
                plot4, = plt.plot(timeArray, itemArray, 'c^')
                plt.ylim([0, yAxis + 1])
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                ax.legend([plot2, plot3, plot4], ["Levels", "Kills", "Items"], loc='center left', bbox_to_anchor=(1,0.5))
                plt.savefig(d + "/" + each.name + "_" + each.team + "_progression.png")

            goldFile.close()
            levelUpFile.close()
            killsFile.close()
            itemsFile.close()

        gameList.append(Game(characterList, d, gameWinner))

        gameWinner = 'null'

if(option == '3'):
    print "Please slect a character"
    selectedCharacter = raw_input()
    selectedCharacter = selectedCharacter.replace(' ', '_')
    selectedCharacter = selectedCharacter.lower()
    selectedCharacter = "npc_dota_hero_" + selectedCharacter
    print selectedCharacter
    goldVarience = list()
    for game in gameList:
        for each in game.characters:
            print selectedCharacter
            print each.name
            if(each.name == selectedCharacter):
                print "B-------------------"
                scalingAmount = each.goldList[0].amount
                for gold in each.goldList:
                    goldArray = []
                    timeArray = []
                    
                    goldArray.append(scalingAmount)
                    timeArray.append(gold.time)
                    scalingAmount += gold.amount
                    goldVarience.append(Gold(scalingAmount, myround(gold.time)))

    goldPlot = list()
    plotting = PlotIt()

    ymin = 0
    ymax = 0

    yerr = [ymin, ymax]

    tempTime = goldVarience[0].time

    goldVarience.sort(key=operator.attrgetter('time'))

    plt.figure()

    for element in goldVarience:
        if(tempTime == element.time):
            goldPlot.append(element.amount)
        if(element.time > tempTime):
            ymin = min(goldPlot)
            print ymin
            ymax = max(goldPlot)
            print ymax
            mean =  np.mean(goldPlot)
            plotting.time.append(tempTime)
            plotting.amount.append(mean)
            plotting.ymax.append(ymax - mean)
            plotting.ymin.append(mean - ymin)
            goldPlot = list()
            goldPlot.append(element.amount)
            tempTime = element.time
    plt.errorbar(plotting.time, plotting.amount, yerr=[plotting.ymin, plotting.ymax], fmt='o', ecolor='g')
    '''plt.plot(plotting.time, plotting.amount)'''

    for each in plotting.amount:
        print each
    plt.show()

raw_input()




