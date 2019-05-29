#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import sys
import os.path
import conf, fav, test, dat
from sorter import Sorter

scriptDir = r""

dataDir = r"data"
outputDir = r"output"
confFile = r"conf.conf"
scriptDir=r""

favorites = dict()
configuration = dict()
usingSystems = []
    
def checkErrors(inputTests,keepLevel) :        
    print("Input Tests")
    test.loadTests(Sorter.setKeys,os.path.join(scriptDir,dataDir),usingSystems)
    print("Output Tests")
    outputTests = test.loadTests(Sorter.setKeys,os.path.join(configuration['exportDir']),usingSystems)
    print("Possible errors")
    for rom in inputTests.keys() :
        
        # new names : bbakraid,snowbro3,fantzn2x,dynwar,rbisland,sf,moomesa,leds2011,batrider,sbomber
        #changedName = ['bkraidu','snowbros3','fantzn2','dw','rainbow','sf1','moo','ledstorm2','batrid','sbomberb']
        
        romNotInFav = True;
        for genre in favorites :
            for name in favorites[genre] :
                if name == rom :
                    romNotInFav = False
        
        if romNotInFav :                    
            print("    Orphan rom %s not in favs" %rom)            
        
        # at least higher than keepLevel in one set
        higherThanKeepLevel = True
        for key in inputTests[rom] :
            higherThanKeepLevel = higherThanKeepLevel and inputTests[rom][key].status >= int(keepLevel)
        
        if higherThanKeepLevel :
            if rom not in outputTests :
                if not rom.startswith('mp_') and not rom.startswith('nss_') :
                    print("    ERROR %s not found in ouput csvs, but in input " %rom, inputTests[rom].keys())
            else :
                for key in inputTests[rom] :
                    if key not in outputTests[rom] :
                        print("    ERROR %s should be exported for %s" %(rom,key))

def printDict(dictList) :    
    for key in dictList :
        print(key, ':', dictList[key])            
        
def useSystems(configuration) :
    systems = []
    for setKey in Sorter.setKeys :
        systems.append(setKey) if os.path.exists(configuration[setKey]) else None
        
    print('Using systems',systems)
    return systems
    
if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    print('Script path : ',scriptDir)
    # load conf.conf
    configuration = conf.loadConf(os.path.join(scriptDir,confFile))
    input('Your outputDir is '+configuration['exportDir']+".\nIts content will be erased.\nIf you don't want to proceed, close this window, else press enter")    
    print('\n<--------- Load Configuration --------->')
    printDict(configuration)
    usingSystems = useSystems(configuration)
    # create favorites containing fav games
    print('\n<--------- Load Favorites Ini Files --------->')
    favorites = fav.loadFavs(scriptDir,Sorter.bioses)
    # parse dat files
    print('\n<--------- Load FBA & Mame Dats --------->')
    datsDict = dict(zip(Sorter.setKeys,['FBAlphav0.2.97.44-temp.dat','mame2003.dat','mame2010.dat']))
    dats = dat.parseDats(scriptDir,dataDir,datsDict,usingSystems)
    # parse test files
    print('\n<--------- Load Tests Files --------->')
    allTests = test.loadTests(Sorter.setKeys,os.path.join(scriptDir,dataDir),usingSystems)
    # create bestarcade romsets
    print('\n<--------- Create Sets --------->')
    sorter = Sorter(configuration,usingSystems,favorites,scriptDir)
    sorter.createSets(allTests,dats)
    print("\n<--------- Detecting errors ----------->")
    checkErrors(allTests,configuration['keepLevel'])
    print('<--------- Process finished ----------->')
    input('\n             (Press Enter)              ')

# TODOS
# missing doctype on generated dat  ?
# if name from dat is empty, take one from test file
