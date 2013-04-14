import json
import sys
import matplotlib.pyplot as plt

class Character:
    """Simple character class for the storing of values"""
    def __init__(self):
        self.goldList = list()
        self.name = ""

class Gold:
    def __init__(self, gold, gameTime):
        self.amount = gold
        self.time = gameTime

file = open('gold.json', 'r')

newstring = file.read()
obj = json.loads(newstring)

characterList = list()
characterTracker = Character()

for o in obj['gold']:
    if(characterTracker.name == ""):
        characterTracker.name = o['hero']
        characterTracker.goldList.append(Gold(o['gold'], o['time']/30))
    if(characterTracker.name == o['hero']):
        characterTracker.goldList.append(Gold(o['gold'], o['time']/30))
        print o['gold']
    else:
        characterList.append(characterTracker)
        characterTracker = Character()
characterList.append(characterTracker)
iCounter = 0
figureCounter = 1
for each in characterList:
    plt.figure(each.name)
    for gold in each.goldList:
        plt.plot(iCounter, gold.amount, 'bo')
        iCounter += 1
    plt.ylabel(each.name)
    iCoutner = 0
plt.show()

raw_input()

