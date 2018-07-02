#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys, collections
import os.path
import shutil
import conf, fav, test, dat

scriptDir = r"C:\DevZone\workspaceFX\scripts4recalbox\BestArcade"

dataDir = r"data"
outputDir = r"output"
confFile = r"conf.conf"
fbaKey = "fba_libretro"
mame2010Key = "mame2010"
mame2003Key = "mame2003"
extension = ".zip"

bioses = ['acpsx','atarisy1','cpzn1','cpzn2','cvs2gd','cvsgd','decocass','konamigv','konamigx','megaplay',
        'megatech','neogeo','nss','pgm','playch10','skns','stvbios','taitofx1','taitogn','taitotz','tps',
        'atarisy1','coh1000t','hng64','crysbios','coh1000a','coh1002e','coh1001l','coh1002m','coh1000t',
        'sys573','sys246','sys256','chihiro','naomi','naomigd','ar_bios','aleck64']

setDict = dict()
configuration = dict()

def setFileCopy(romsetFile,genre,fileName,targetDir,useGenreSubFolder) :
    a = 1
#    if os.path.exists(romsetFile) :        
#        if useGenreSubFolder :
#            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,genre,fileName+".zip"))
#        else :
#            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,fileName+".zip"))        

def computeScore(setKey,setDir,game,test) :
    score = test[setKey].status if setKey in test else -2
    
    if score == -2 and os.path.exists(os.path.join(setDir,game+".zip")) :
        score = -1 
    return score

def keepSet(keepNotTested,exclusionType,keepLevel,scores,key,keep) :
    maxScore = max(scores.values())   
    if keepNotTested and scores[key] == -1 :
        keep.append(key)
    elif exclusionType == 'NONE' :
        keep.append(key) if scores[key] >= keepLevel else None
    elif exclusionType == 'EQUAL' :
        if scores[key] == maxScore :
            keep.append(key) if scores[key] >= keepLevel else None
    elif exclusionType == 'STRICT' :
        if scores[key] == maxScore :
            if fbaKey not in keep and mame2010Key not in keep:
                keep.append(key) if scores[key] >= keepLevel else None
                
def writeCSV(csvFile,game,score,genre,dat,test,setKey) :
    if game in dat :
        name = dat[game].description
        year = dat[game].year
        manufacturer = dat[game].manufacturer
    else :
        name, year, manufacturer = '','',''
        
    if setKey in test :
        hardware = test[setKey].hardware
        comments = test[setKey].comments
        notes = test[setKey].notes
    else :
        hardware,comments,notes = '','',''
        
    csvFile.write("%i;%s;%s;%s;%s;%s;%s;%s;%s\n" 
                  %(score,genre,name,game,year,manufacturer,hardware,comments,notes))

def createSets(allTests,dats) :    
    
    scoreSheet = open(os.path.join(configuration['exportDir'],"scoreSheet.csv"),"w",encoding="utf-8")
    fbaCSV = open(os.path.join(configuration['exportDir'],fbaKey+".csv"),"w",encoding="utf-8")
    mame2003CSV = open(os.path.join(configuration['exportDir'],mame2003Key+".csv"),"w",encoding="utf-8")
    mame2010CSV = open(os.path.join(configuration['exportDir'],mame2010Key+".csv"),"w",encoding="utf-8")
    header="Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
    fbaCSV.write(header)
    mame2003CSV.write(header)
    mame2010CSV.write(header)
    scoreSheet.write('rom;fbaScore;mame2003Score;mame2010Score\n')
    
    notInAnySet = []
    onlyInOneSet = dict()
    useGenreSubFolder = True if configuration['genreSubFolders'] == '1' else False
    keepNotTested = True if configuration['keepNotTested'] == '1' else False
    keepLevel = int(configuration['keepLevel'])    
    
    if not useGenreSubFolder :
        os.makedirs(os.path.join(configuration['exportDir'],fbaKey))
        os.makedirs(os.path.join(configuration['exportDir'],mame2003Key))
        os.makedirs(os.path.join(configuration['exportDir'],mame2010Key))
    
    for genre in setDict.keys() :
        print("Handling genre %s" %genre)
        
        if useGenreSubFolder :
            os.makedirs(os.path.join(configuration['exportDir'],fbaKey,genre))
            os.makedirs(os.path.join(configuration['exportDir'],mame2003Key,genre))
            os.makedirs(os.path.join(configuration['exportDir'],mame2010Key,genre))        
        
        # copy bios in each subdirectory
        for bios in bioses :            
            fbaBios = os.path.join(configuration['fbaSet'],bios+".zip")
            mame2003Bios = os.path.join(configuration['mame2003Set'],bios+".zip")
            mame2010Bios = os.path.join(configuration['mame2010Set'],bios+".zip")
            
            setFileCopy(fbaBios,genre,bios,fbaKey,useGenreSubFolder)
            setFileCopy(mame2003Bios,genre,bios,mame2003Key,useGenreSubFolder)
            setFileCopy(mame2010Bios,genre,bios,mame2010Key,useGenreSubFolder)        
        
        for game in sorted(setDict[genre]) :
            audit = game +" -> "
            
            scores = dict()
            if game in allTests :
                 scores[fbaKey] = computeScore(fbaKey,configuration['fbaSet'],game,allTests[game])
                 scores[mame2003Key] = computeScore(mame2003Key,configuration['mame2003Set'],game,allTests[game])
                 scores[mame2010Key] = computeScore(mame2010Key,configuration['mame2010Set'],game,allTests[game])                 
            else :
                scores[fbaKey], scores[mame2003Key], scores[mame2010Key] = -2, -2, -2
            
            audit = audit + " SCORES: "+ str(scores[fbaKey]) + " " + str(scores[mame2003Key]) + " " + str(scores[mame2010Key]) + " ,"                                    
            scoreSheet.write('%s;%i;%i;%i\n' %(game,scores[fbaKey], scores[mame2003Key], scores[mame2010Key]))
            
            selected = []
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,fbaKey,selected)            
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,mame2010Key,selected)
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,mame2003Key,selected)
            
            audit = audit + " SELECTED: "+ str(selected)
            
            fbaRom = os.path.join(configuration['fbaSet'],game+".zip")
            mame2003Rom = os.path.join(configuration['mame2003Set'],game+".zip")
            mame2010Rom = os.path.join(configuration['mame2010Set'],game+".zip")            
            
            #"Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
            
            if fbaKey in selected :
                setFileCopy(fbaRom,genre,game,fbaKey,useGenreSubFolder)                
                writeCSV(fbaCSV,game,scores[fbaKey],genre,dats[fbaKey],allTests[game],fbaKey)                
            if mame2003Key in selected :    
                setFileCopy(mame2003Rom,genre,game,mame2003Key,useGenreSubFolder)
                writeCSV(mame2003CSV,game,scores[mame2003Key],genre,dats[mame2003Key],allTests[game],mame2003Key)
            if mame2010Key in selected :
                setFileCopy(mame2010Rom,genre,game,mame2010Key,useGenreSubFolder)
                writeCSV(mame2010CSV,game,scores[mame2010Key],genre,dats[mame2010Key],allTests[game],mame2010Key)
         
            if len(selected) == 0 :                
                notInAnySet.append(game)
            elif len(selected) == 1 :
                if selected[0] not in onlyInOneSet :
                    onlyInOneSet[selected[0]] = []
                onlyInOneSet[selected[0]].append(game)
            
            #print("    %s" %audit)
    
    fbaCSV.close()
    mame2003CSV.close()
    mame2010CSV.close()
    scoreSheet.close()
        
    print ("\n<------------------ RESULTS ------------------>")
    print("NOT FOUND IN ANY SET : %i" %len(notInAnySet))
    print(notInAnySet)
    print("ONLY IN ONE SET :")
    printDict(onlyInOneSet)          
    
def writeSets() :
    print("Write Sets")
    
def checkErrors(inputTests,keepLevel) :        
    print("Input Tests")
    test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(scriptDir,dataDir))
    print("Output Tests")
    outputTests = test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(configuration['exportDir']))
    print("Possible errors")
    for rom in inputTests.keys() :
        
        # new names : bbakraid,snowbro3,fantzn2x,dynwar,rbisland,sf,moomesa,leds2011,batrider,sbomber
        #changedName = ['bkraidu','snowbros3','fantzn2','dw','rainbow','sf1','moo','ledstorm2','batrid','sbomberb']
        
        romNotInFav = True;
        for genre in setDict :
            for name in setDict[genre] :
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
                print("    ERROR %s not found in ouput csvs, but in input " %rom, inputTests[rom].keys())
            else :
                for key in inputTests[rom] :
                    if key not in outputTests[rom] :
                        print("    ERROR %s should be exported for %s" %(rom,key))

def printDict(dictList) :    
    for key in dictList :
        print(key, ':', dictList[key])            
    
if __name__ == "__main__":
    # load conf.conf
    configuration = conf.loadConf(os.path.join(scriptDir,confFile))
    print('\n<--------- Load Configuration --------->')
    printDict(configuration)
    # create setDict containing fav games
    print('\n<--------- Load Favorites Ini Files --------->')
    fav.loadFavs(configuration,bioses,setDict)
    # parse dat files
    print('\n<--------- Load FBA & Mame Dats --------->')
    dats = dat.parseDats(scriptDir,dataDir,[fbaKey,mame2003Key,mame2010Key],['FBAlphav0.2.97.43.dat','mame2003.dat','mame2010.dat'])
    # parse test files
    print('\n<--------- Load Tests Files --------->')
    allTests = test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(scriptDir,dataDir))
    # create bestarcade romsets
    print('\n<--------- Create Sets --------->')
    createSets(allTests,dats)
    print("\n<--------- Detecting errors ----------->")
    checkErrors(allTests,configuration['keepLevel'])
# writeSets()
# write scoresheet, handle non-present romsets, write gamelists, empty existing target sets (write set dat)
