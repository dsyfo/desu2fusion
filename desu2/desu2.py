#! /usr/bin/python
import sys

RACES = ['OMEGA', 'MEGAMI', 'DEITY', 'VILE', 'SNAKE', 'DRAGON', 'DIVINE', \
         'AVIAN', 'FALLEN', 'AVATAR', 'BEAST', 'WILDER', 'GENMA', 'FAIRY', \
         'TYRANT', 'KISHIN', 'TOUKI', 'JAKI', 'FEMME', 'GHOST', 'FIEND', 'HERO' ]

ELEMENTS = ['ERTHYS', 'AEROS', 'AQUANS', 'FLAEMIS']

class Demon:
    def __init__(self, race, level, left=None, right=None, cost=None):
        self.race = race
        self.level = int(level)
        self.left = left
        self.right = right
        self.name = str(race) + str(level)
        if cost:
            self.cost = cost
        else:
            if self.left and self.right:
                self.cost = self.left.get_cost() + self.right.get_cost()
                if self.race in ELEMENTS:
                    self.cost += 1000
            else:
                self.cost = 9999999

    def get_cost(self):
        if not self.cost:
            self.cost = self.left.get_cost() + self.right.get_cost()
            if self.race in ELEMENTS:
                self.cost += 1000
        return self.cost

    def __repr__(self):
        s = str(self.race) + " Lv" + str(self.level) + ", $" + str(self.cost)
        l = "\n" + str(self.left) if self.left else ""
        r = "\n" + str(self.right) if self.right else ""
        t = "%s%s" % (l, r)
        t = t.replace('\n','\n\t')
        return "%s%s" % (s, t)

races = {}
f = open("races.txt")
for line in f.readlines():
    line = line.split()
    if len(line) > 0:
        for word in line:
            if word not in RACES + ELEMENTS:
                print line
        if len(line) > 1:
            races[key] += [(line[0],line[1])]
        else:
            key = line[0]
            races[key] = []
f.close()

levels = {}
f = open("levels.txt")
for line in f.readlines():
    line = line.split()
    if len(line) > 0:
        if line[0] not in RACES + ELEMENTS:
            print line
        levels[line[0]] = [int(l) for l in line[1:]]
f.close()

base = []
f = open('costs.txt')
for line in f.readlines():
    line = line.split()
    if len(line) == 3:
        if line[0] not in RACES + ELEMENTS:
            print line
        base += [Demon(line[0], int(line[1]), left=None, right=None, cost=int(line[2]))]
f.close()
fastbase = [i.name for i in base]

def fuse(demon1, demon2):
    race = None
    if demon1.race in ELEMENTS:
        (demon1, demon2) = (demon2, demon1)
    if demon2.race in ELEMENTS:
        demon2.level = demon1.level + 1
    if demon1.race == demon2.race:
        racelist = ELEMENTS
    else:
        racelist = RACES
    for i in racelist:
        for combo in races[i]:
            if demon1.race in combo and demon2.race in combo:
                race = i
                break
        if race:
            break
    if not race:
        return Demon(None, 0)
    level = float(demon1.level+demon2.level)/2
    for l in levels[race]:
        if l >= level:
            level = l
            break
    return Demon(race, level, 0)

def reverse_fuse(demon3):
    global base
    global fastbase
    if demon3.name in fastbase:
        base_demon = [i for i in base if i.race == demon3.race and i.level == demon3.level][0]
        return base_demon
    upper = demon3.level
    lower = 0
    for l in levels[demon3.race]:
        if l >= upper:
            break
        else:
            lower = l
    best_cost = 9999999999
    for combo in races[demon3.race]:
        (race1, race2) = combo
        for i in levels[race1]:
            for j in levels[race2]:
                if i < demon3.level and j < demon3.level:
                    avg = (i+j)/2
                else:
                    avg = upper+1
                if race1 in ELEMENTS:
                    i = j
                    avg = i
                if race2 in ELEMENTS:
                    j = i
                    avg = i
                if demon3.race in ELEMENTS:
                    lower = 1
                if avg>=lower and avg<upper:
                    left = reverse_fuse(Demon(race1, i))
                    right = reverse_fuse(Demon(race2, j))
                    cost = left.get_cost() + right.get_cost()
                    if cost < best_cost:
                        best_cost = cost
                        demon3.left = left
                        demon3.right = right
                        demon3.cost = best_cost
                        if demon3.race in ELEMENTS:
                            demon3.cost += 1000
    if demon3.name not in fastbase:
        base += [demon3]
        fastbase += [demon3.name]
    return demon3

demon3 = Demon(sys.argv[1].upper(), int(sys.argv[2]))
demon3 = reverse_fuse(demon3)
print demon3
