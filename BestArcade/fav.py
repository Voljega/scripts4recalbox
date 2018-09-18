#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import os.path

dataDir = r"data"
smallSetFile = r"SmallSet.ini"
bigSetFile = r"BigSet.ini"

def parseSetFile(setFile, setDict) :
    file = open(setFile,'r')
    genre = None
    # Parse iniFile in iniFile dir    
    for line in file.readlines() :
        line = line.rstrip('\n\r ')
        if (line.startswith('[') and not line == '[FOLDER_SETTINGS]' and not line == '[ROOT_FOLDER]') :            
            genre = line
            if genre not in setDict :                
                setDict[genre] = []
        else :
            if (genre is not None and not line == '' ) :
                setDict[genre].append(line)
                
    file.close()

def loadFavs(scriptDir, bioses, setDict) :    
    parseSetFile(os.path.join(scriptDir,dataDir,smallSetFile),setDict)    
    parseSetFile(os.path.join(scriptDir,dataDir,bigSetFile),setDict)
    
    print('Nb Genre : %s' %len(setDict))    
    sumGames = 0
    for key in setDict.keys() :
        # print(key)
        # print(setDict[key])
        sumGames = sumGames + len(setDict[key])
        
    print('Nb Games : %s' %sumGames)
    print('Nb Bios : %s' %len(bioses))