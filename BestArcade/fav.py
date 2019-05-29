#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import os.path

dataDir = r"data"
smallSetFile = r"SmallSet.ini"
bigSetFile = r"BigSet.ini"

def parseSetFile(setFile, favorites) :
    file = open(setFile,'r')
    genre = None
    # Parse iniFile in iniFile dir    
    for line in file.readlines() :
        line = line.rstrip('\n\r ')
        if (line.startswith('[') and not line == '[FOLDER_SETTINGS]' and not line == '[ROOT_FOLDER]') :            
            genre = line
            if genre not in favorites :                
                favorites[genre] = []
        else :
            if (genre is not None and not line == '' ) :
                favorites[genre].append(line)
                
    file.close()

def loadFavs(scriptDir, bioses) :    
    favorites = dict()
    parseSetFile(os.path.join(scriptDir,dataDir,smallSetFile),favorites)    
    parseSetFile(os.path.join(scriptDir,dataDir,bigSetFile),favorites)
    
    print('Nb Genre : %s' %len(favorites))    
    sumGames = 0
    for key in favorites.keys() :
        # print(key)
        # print(setDict[key])
        sumGames = sumGames + len(favorites[key])
        
    print('Nb Games : %s' %sumGames)
    print('Nb Bios : %s' %len(bioses))
    return favorites