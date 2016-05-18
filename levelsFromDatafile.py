# -*- coding: utf-8 -*-
"""
Created on Mon May 16 17:25:10 2016

@author: jaymz_ubuntu
"""

import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

levelWidth = 0.2

dataFile = 'data_files/Mg-II.levels'
dataFileSeparator = ','

showElectricDipole =        False
showElectricQuadrupole =    False

title = 'Energy Level Diagram for ' + dataFile
scale = 'cm$^{-1}$'

file = open(dataFile,'r')
minY, maxY = 0, 0
yMargin = 0.1

levels = []
transitions = []
for line in file:
    if(len(line)>=11 and line[0:11] == '$TRANSITION'):
        ln = line.split(dataFileSeparator)
        transitions.append({'i': int(ln[1]), 'f': int(ln[2])})
        if(len(ln)>3):
            for part in ln:
                command=part.split('=')
                if(command[0]=='$LABEL'):
                    transitions[-1]['label']=command[1]
                elif(command[0]=='$COLOR'):
                    transitions[-1]['color']=command[1]
                elif(command[0]=='$SHOW-NM'):
                    if(command[1].rstrip()=='1' or command[1].rstrip().lower()=='t'):
                        transitions[-1]['show-nm']=True
                    else:
                        transitions[-1]['show-nm']=False
    elif(line[0] == '$'):
        ln = line.split(dataFileSeparator)
        for command in ln:  
            vals = command.split("=")
            if(len(command)==0):
                continue
            if(vals[0] == '$TITLE'):
                title = vals[1]
            elif(vals[0] == '$SCALE'):
                scale = vals[1]
            else:
                print('Invalid Command encountered data file' + dataFile)
                print('---->' + line)
    else:
        ln = line.split(dataFileSeparator)
        if(len(ln[0])==0):
            continue
        v=float(ln[0])
        levels.append({'energy' : v, 'label' : ln[1]})
        minY = min(v,minY)
        maxY = max(v,maxY)
file.close()

for i in range(0,len(levels)):
    st = levels[i]['label']
    st=st.split('^')
    
    levels[i]['n']=int(st[0])
    levels[i]['mult']=int(st[1][0])
    levels[i]['j']=Fraction(st[1].split('_')[-1])
    if('S' in st[1]):
        levels[i]['l']=0
    elif('P' in st[1]):
        levels[i]['l']=1
    elif('D' in st[1]):
        levels[i]['l']=2
    elif('F' in st[1]):
        levels[i]['l']=3
    else:
        levels[i]['l']=-1
    
    if(levels[i]['l'] == 0):
        xstart = 1
    elif(levels[i]['l'] == 1):
        xstart = 2
    elif(levels[i]['l'] == 2):
        xstart = 3
    elif(levels[i]['l'] == 3):
        xstart = 4
    levels[i]['xstart']=xstart

if(showElectricDipole):
    for i in range(0,len(levels)):
        for j in range(i+1,len(levels)):
            delta_j = abs(levels[i]['j']-levels[j]['j'])
            if(delta_j == Fraction(1,1) or delta_j == Fraction(0,1)):
                if(abs(levels[i]['l']-levels[j]['l'])==1):
                    transitions.append({'i' : i, 'f' : j})
                    
if(showElectricQuadrupole):
    for i in range(0,len(levels)):
        for j in range(i+1,len(levels)):
            delta_j = abs(levels[i]['j']-levels[j]['j'])
            if(delta_j == Fraction(2,1) or delta_j == Fraction(0,1)):
                if(abs(levels[i]['l']-levels[j]['l'])==2):
                    transitions.append({'i' : i, 'f' : j})

def nmString(transition):
    return str(int(1239.8393589807376/abs(levels[trans['i']]['energy'] - levels[trans['f']]['energy']))) + 'nm'

for trans in transitions:
    if(not trans.has_key('label')):
        if(trans.has_key('show-nm') and not trans['show-nm']):
            continue
        else:
            trans['label']=nmString(trans)
    elif(trans.has_key('show-nm') and trans['show-nm']):
        trans['label']=trans['label'] + ' (' + nmString(trans) +')'

for level in levels:
    plt.plot([level['xstart']-levelWidth,level['xstart']+levelWidth],[level['energy'],level['energy']],'-0')
for level in levels:
    plt.annotate('$'+level['label'].split('_')[0]+ '_{'+ str(level['j']) + '}$',xy=(level['xstart']+levelWidth,level['energy']))
for t in transitions:
    x=levels[t['i']]['xstart']
    y=levels[t['i']]['energy']
    dx = levels[t['f']]['xstart']-levels[t['i']]['xstart']
    dy = levels[t['f']]['energy']-levels[t['i']]['energy']
    dr = np.sqrt(dx**2+dy**2)
    headLength, headWidth = 0.0, 0.00
    tColor = 'red'
    if(t.has_key('color')):
        tColor=t['color']
    plt.arrow(x,y,dx-dx/dr*headLength,dy-dy/dr*headLength,head_width=headWidth,head_length=headLength,color=tColor.rstrip())
    plt.annotate(t['label'],xy=(x+dx/2,y+dy/2),color=tColor.rstrip())
yRange = maxY-minY
plt.ylim(minY-yMargin*yRange,maxY+yMargin*yRange)
plt.ylabel(scale)
plt.title(title)
plt.xlim(0,5)
plt.xticks([1,2,3,4],['S','P','D','F'])
plt.show()