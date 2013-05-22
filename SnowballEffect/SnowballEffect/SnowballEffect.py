import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

class Character:
    """Simple character class for the storing of values"""
    def __init__(self):
        self.goldList = list()
        self.levelUpTimes = list()
        self.kills = list()
        self.items = list()
        self.name = ""

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

colorList = list()
colorList.append('b^')
colorList.append('g^')
colorList.append('r^')
colorList.append('c^')
colorList.append('m^')
colorList.append('y^')
colorList.append('k^')
colorList.append('bo')
colorList.append('go')
colorList.append('co');

goldFile = open('gold.json', 'r')
levelUpFile = open('levelups.json', 'r')
killsFile = open('herokills.json', 'r')
itemsFile = open('itemtimes.json', 'r')

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

iCounter = 0
totalGold = 0
figureCounter = 1
color = 0

yAxis = 0
yAxisGold = 0

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
    '''if(each.name == 'npc_dota_hero_nyx_assassin'):'''
    fig = plt.figure(each.name + "Gold")
    ax = plt.subplot(111)
    plt.title(each.name)
    plt.xlabel("Time")
    plt.ylabel("Amount")
    colorString = colorList[color]
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
    plt.savefig(each.name + "_gold.png")
    fig = plt.figure(each.name + "Progression")
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
        print item.name
    plot4, = plt.plot(timeArray, itemArray, 'c^')
    plt.ylim([0, yAxis + 1])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend([plot2, plot3, plot4], ["Levels", "Kills", "Items"], loc='center left', bbox_to_anchor=(1,0.5))
    plt.savefig(each.name + "_progression.png")
'''for each in characterList:
    plt.figure(each.name)
    colorString = colorList[color]
    for gold in each.goldList:
        plt.plot(gold.time, gold.amount, 'bo', linestyle='-')
    plt.ylabel(each.name)
    totalGold = 0
    color += 1
plt.show()
color = 0

for each in characterList:
    plt.figure(each.name)
    colorString = colorList[color]
    timeArray = []
    levelArray = []
    for level in each.levelUpTimes:
        timeArray.append(level.time)
        levelArray.append(level.level)
    plt.savefig('levelProgression.png');
    plt.plot(timeArray, levelArray, colorString, linestyle='-')
    plt.ylabel("Total Level Progression for each character")
    color += 1
plt.show()
color = 0

for each in characterList:
    colorString = colorList[color]
    timeArray = []
    killsArray = []
    for kill in each.kills:
        timeArray.append(kill.time)
        killsArray.append(each.kills.index(kill) + 1)
    plt.savefig('killTimes.png');
    plt.plot(timeArray, killsArray, colorString, linestyle='-')
    plt.ylabel("Kill times")
    color += 1
plt.show();
color = 0'''

raw_input()

