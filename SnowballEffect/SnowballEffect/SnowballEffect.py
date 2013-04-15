import json
import sys
import matplotlib.pyplot as plt

class Character:
    """Simple character class for the storing of values"""
    def __init__(self):
        self.goldList = list()
        self.levelUpTimes = list()
        self.kills = list()
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

colorList = list()
colorList.append('b^')
colorList.append('g^')
colorList.append('r^')
colorList.append('c^')
colorList.append('m^')
colorList.append('y^')
colorList.append('k^')
colorList.append('w^')
colorList.append('bo')
colorList.append('go')

goldFile = open('gold.json', 'r')
levelUpFile = open('levelups.json', 'r')
killsFile = open('herokills.json', 'r')

goldFileJson = goldFile.read()
levelFileJson = levelUpFile.read()
killsFileJson = killsFile.read()

obj = json.loads(goldFileJson)
obj2 = json.loads(levelFileJson)
obj3 = json.loads(killsFileJson)

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
            char.levelUpTimes.append(LevelUp(o['level'], o['time']))

for char in characterList:
    for o in obj3['herokills']:
        if(char.name == o['killer']):
            char.kills.append(Kill(o['time'], o['dead']))

iCounter = 0
totalGold = 0
figureCounter = 1
color = 0

for each in characterList:
    plt.figure(each.name)
    colorString = colorList[color]
    for gold in each.goldList:
        plt.plot(gold.time, gold.amount, 'bo')
    plt.ylabel(each.name)
    totalGold = 0
    color += 1
plt.show()
color = 0

for each in characterList:
    '''plt.figure(each.name)'''
    colorString = colorList[color]
    for level in each.levelUpTimes:
        plt.plot(level.time/30, level.level, colorString)
    plt.ylabel("Total Level Progression for each character")
    color += 1
plt.show()
color = 0

for each in characterList:
    print each.name
    colorString = colorList[color]
    print colorString
    for k in each.kills:
        plt.plot(k.time/30, (each.kills.index(k) + 1), colorString)
    plt.ylabel("Kill times")
    color += 1
plt.show()
color = 0

raw_input()

