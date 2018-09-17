#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys, collections
import os.path
import shutil
import conf, fav, test, dat, gamelist

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
usingSystems = []

def setFileCopy(romsetFile,genre,fileName,targetDir,useGenreSubFolder) :
#    a = 1
    if os.path.exists(romsetFile) :        
        if useGenreSubFolder :
            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,genre,fileName+".zip"))
        else :
            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,fileName+".zip"))        

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

def getStatus(status) :
    if status == -1 :
        return 'UNTESTED'
    elif status == 0 :
        return 'NON_WORKING'
    elif status == 1 :
        return 'BADLY WORKING'
    elif status == 2 :
        return 'MOSTLY WORKING'
    elif status == 3 :
        return 'WORKING'
    else :
        return 'UNTESTED &amp; FRESHLY ADDED'

def writeGamelistHiddenEntry(gamelistFile,game,genre,useGenreSubFolder) :
    gamelist.writeGamelistHiddenEntry(gamelistFile,game+".zip",genre,useGenreSubFolder)
    
def writeGamelistEntry(gamelistFile,game,dat,genre,useGenreSubFolder,test,setKey):
    frontPic = "./downloaded_images/"+game+".png"
    
    if game in dat :
        fullName = dat[game].description
        fullName.replace('&', '&amp;')
        name = fullName
        if '(' in name :
            indPar = name.index('(')
            name = name[:(indPar-1)].strip()            
            
        year = dat[game].year if dat[game].year else ''
        developer = dat[game].manufacturer.replace('&', '&amp;') if dat[game].manufacturer else ''
        cloneof = dat[game].cloneof
    else :
        fullName, name, year, developer, cloneof = '','','','',''
        
    if setKey in test :
        hardware = test[setKey].hardware
        comments = test[setKey].comments
        notes = test[setKey].notes
        status = getStatus(test[setKey].status)        
    else :
        hardware,comments,notes,status = '','','','UNTESTED &amp; FRESHLY ADDED'
        
    desc = ('Rom : '+game+' , Clone of : ' + cloneof + '\n') if cloneof else ('Rom : '+game+'\n')
    desc = desc + ('Fullname : '+fullName+'\n')
    desc = desc + ('Status : ' + status + '\n' )
    desc = desc + (('Hardware : ' + hardware + '\n') if hardware else '')
    desc = desc + ((comments + '\n') if comments else '')
    desc = desc + ((notes + '\n') if notes else '')
    desc = desc + '        '
    
    gamelist.writeGamelistEntry(gamelistFile,game+".zip",name,desc,year,frontPic,developer,developer,genre,useGenreSubFolder)    

def createSets(allTests,dats) :
    
    print("Cleaning output directory")
    for file in os.listdir(os.path.join(configuration['exportDir'])) :
        fullPath = os.path.join(configuration['exportDir'],file)        
        shutil.rmtree(fullPath) if os.path.isdir(fullPath) else os.remove(fullPath)
    
    scoreSheet = open(os.path.join(configuration['exportDir'],"scoreSheet.csv"),"w",encoding="utf-8")
    fbaCSV = open(os.path.join(configuration['exportDir'],fbaKey+".csv"),"w",encoding="utf-8") if fbaKey in usingSystems else None    
    mame2003CSV = open(os.path.join(configuration['exportDir'],mame2003Key+".csv"),"w",encoding="utf-8") if mame2003Key in usingSystems else None    
    mame2010CSV = open(os.path.join(configuration['exportDir'],mame2010Key+".csv"),"w",encoding="utf-8") if mame2010Key in usingSystems else None    
    header="Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
    fbaCSV.write(header) if fbaKey in usingSystems else None
    mame2003CSV.write(header) if mame2003Key in usingSystems else None
    mame2010CSV.write(header) if mame2010Key in usingSystems else None
    scoreSheet.write('rom;fbaScore;mame2003Score;mame2010Score\n')
    
    rootFba = etree.Element("datafile") if fbaKey in usingSystems else None
    rootMame2003 = etree.Element("datafile") if mame2003Key in usingSystems else None
    rootMame2010 = etree.Element("datafile") if mame2010Key in usingSystems else None
    rootFba.append(dats[fbaKey+"Header"]) if fbaKey in usingSystems else None
    rootMame2003.append(dats[mame2003Key+"Header"]) if mame2003Key in usingSystems else None
    rootMame2010.append(dats[mame2010Key+"Header"]) if mame2010Key in usingSystems else None
       
    notInAnySet = []
    onlyInOneSet = dict()
    useGenreSubFolder = True if configuration['genreSubFolders'] == '1' else False
    keepNotTested = True if configuration['keepNotTested'] == '1' else False
    keepLevel = int(configuration['keepLevel'])    
    
    os.makedirs(os.path.join(configuration['exportDir'],fbaKey)) if fbaKey in usingSystems else None
    os.makedirs(os.path.join(configuration['exportDir'],mame2003Key)) if mame2003Key in usingSystems else None
    os.makedirs(os.path.join(configuration['exportDir'],mame2010Key)) if mame2010Key in usingSystems else None
    fbaGamelist = gamelist.init(os.path.join(configuration['exportDir'],fbaKey)) if fbaKey in usingSystems else None
    mame2003Gamelist = gamelist.init(os.path.join(configuration['exportDir'],mame2003Key)) if mame2003Key in usingSystems else None
    mame2010Gamelist = gamelist.init(os.path.join(configuration['exportDir'],mame2010Key)) if mame2010Key in usingSystems else None
    
    
    for genre in setDict.keys() :
        print("Handling genre %s" %genre)
        
        if useGenreSubFolder :
            os.makedirs(os.path.join(configuration['exportDir'],fbaKey,genre)) if fbaKey in usingSystems else None
            os.makedirs(os.path.join(configuration['exportDir'],mame2003Key,genre)) if mame2003Key in usingSystems else None
            os.makedirs(os.path.join(configuration['exportDir'],mame2010Key,genre)) if mame2010Key in usingSystems else None        
        
        # copy bios in each subdirectory
        for bios in bioses :            
            fbaBios = os.path.join(configuration['fbaSet'],bios+".zip") if fbaKey in usingSystems else None
            mame2003Bios = os.path.join(configuration['mame2003Set'],bios+".zip") if mame2003Key in usingSystems else None
            mame2010Bios = os.path.join(configuration['mame2010Set'],bios+".zip") if mame2010Key in usingSystems else None            
            setFileCopy(fbaBios,genre,bios,fbaKey,useGenreSubFolder) if fbaKey in usingSystems else None
            writeGamelistHiddenEntry(fbaGamelist,bios,genre,useGenreSubFolder) if fbaKey in usingSystems else None
            setFileCopy(mame2003Bios,genre,bios,mame2003Key,useGenreSubFolder) if mame2003Key in usingSystems else None
            writeGamelistHiddenEntry(mame2003Gamelist,bios,genre,useGenreSubFolder) if mame2003Key in usingSystems else None
            setFileCopy(mame2010Bios,genre,bios,mame2010Key,useGenreSubFolder) if mame2010Key in usingSystems else None
            writeGamelistHiddenEntry(mame2010Gamelist,bios,genre,useGenreSubFolder) if mame2010Key in usingSystems else None
        
        for game in sorted(setDict[genre]) :
            audit = game +" -> "
            
            scores = dict()
            if game in allTests :
                 scores[fbaKey] = computeScore(fbaKey,configuration['fbaSet'],game,allTests[game]) if fbaKey in usingSystems else -2
                 scores[mame2003Key] = computeScore(mame2003Key,configuration['mame2003Set'],game,allTests[game]) if mame2003Key in usingSystems else -2
                 scores[mame2010Key] = computeScore(mame2010Key,configuration['mame2010Set'],game,allTests[game]) if mame2010Key in usingSystems else -2
            else :
                scores[fbaKey], scores[mame2003Key], scores[mame2010Key] = -2, -2, -2
            
            audit = audit + " SCORES: "+ str(scores[fbaKey]) + " " + str(scores[mame2003Key]) + " " + str(scores[mame2010Key]) + " ,"                                    
            scoreSheet.write('%s;%i;%i;%i\n' %(game,scores[fbaKey], scores[mame2003Key], scores[mame2010Key]))
            
            selected = []
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,fbaKey,selected)  if fbaKey in usingSystems else None           
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,mame2010Key,selected) if mame2010Key in usingSystems else None
            keepSet(keepNotTested,configuration['exclusionType'],keepLevel,scores,mame2003Key,selected) if mame2003Key in usingSystems else None
            
            audit = audit + " SELECTED: "+ str(selected)
            
            fbaRom = os.path.join(configuration['fbaSet'],game+".zip") if fbaKey in usingSystems else None
            mame2003Rom = os.path.join(configuration['mame2003Set'],game+".zip") if mame2003Key in usingSystems else None
            mame2010Rom = os.path.join(configuration['mame2010Set'],game+".zip") if mame2010Key in usingSystems else None
            
            if fbaKey in selected and fbaKey in usingSystems :
                setFileCopy(fbaRom,genre,game,fbaKey,useGenreSubFolder)                
                writeCSV(fbaCSV,game,scores[fbaKey],genre,dats[fbaKey],allTests[game],fbaKey)
                writeGamelistEntry(fbaGamelist,game,dats[fbaKey],genre,useGenreSubFolder,allTests[game],fbaKey)
                rootFba.append(dats[fbaKey][game].node) if game in dats[fbaKey] else None              
            if mame2003Key in selected and mame2003Key in usingSystems :    
                setFileCopy(mame2003Rom,genre,game,mame2003Key,useGenreSubFolder)
                writeCSV(mame2003CSV,game,scores[mame2003Key],genre,dats[mame2003Key],allTests[game],mame2003Key)
                writeGamelistEntry(mame2003Gamelist,game,dats[mame2003Key],genre,useGenreSubFolder,allTests[game],mame2003Key)
                rootMame2003.append(dats[mame2003Key][game].node) if game in dats[mame2003Key] else None
            if mame2010Key in selected and mame2010Key in usingSystems :
                setFileCopy(mame2010Rom,genre,game,mame2010Key,useGenreSubFolder)
                writeCSV(mame2010CSV,game,scores[mame2010Key],genre,dats[mame2010Key],allTests[game],mame2010Key)
                writeGamelistEntry(mame2010Gamelist,game,dats[mame2010Key],genre,useGenreSubFolder,allTests[game],mame2010Key)
                rootMame2010.append(dats[mame2010Key][game].node) if game in dats[mame2010Key] else None
         
            if len(selected) == 0 :                
                notInAnySet.append(game)
            elif len(selected) == 1 :
                if selected[0] not in onlyInOneSet :
                    onlyInOneSet[selected[0]] = []
                onlyInOneSet[selected[0]].append(game)
            
            print("    %s" %audit)
    
    treeFba = etree.ElementTree(rootFba) if fbaKey in usingSystems else None
    treeFba.write(os.path.join(configuration['exportDir'],fbaKey+".dat"), xml_declaration=True, encoding="utf-8") if fbaKey in usingSystems else None
    treeMame2003 = etree.ElementTree(rootMame2003) if mame2003Key in usingSystems else None
    treeMame2003.write(os.path.join(configuration['exportDir'],mame2003Key+".dat"), xml_declaration=True, encoding="utf-8") if mame2003Key in usingSystems else None
    treeMame2010 = etree.ElementTree(rootMame2010) if mame2010Key in usingSystems else None
    treeMame2010.write(os.path.join(configuration['exportDir'],mame2010Key+".dat"), xml_declaration=True, encoding="utf-8") if mame2010Key in usingSystems else None
       
    fbaCSV.close() if fbaKey in usingSystems else None
    gamelist.close(fbaGamelist) if fbaKey in usingSystems else None
    mame2003CSV.close() if mame2003Key in usingSystems else None
    gamelist.close(mame2003Gamelist) if mame2003Key in usingSystems else None
    mame2010CSV.close() if mame2010Key in usingSystems else None
    gamelist.close(mame2010Gamelist) if mame2010Key in usingSystems else None
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
    test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(scriptDir,dataDir),usingSystems)
    print("Output Tests")
    outputTests = test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(configuration['exportDir']),usingSystems)
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
        
def useSystems(configuration) :
    systems = []
    systems.append(fbaKey) if os.path.exists(configuration['fbaSet']) else None
    systems.append(mame2003Key) if os.path.exists(configuration['mame2003Set']) else None
    systems.append(mame2010Key) if os.path.exists(configuration['mame2010Set']) else None
    print('Using systems',systems)
    return systems
    
if __name__ == "__main__":
    # load conf.conf
    configuration = conf.loadConf(os.path.join(scriptDir,confFile))
    print('\n<--------- Load Configuration --------->')
    printDict(configuration)
    usingSystems = useSystems(configuration)
    # create setDict containing fav games
    print('\n<--------- Load Favorites Ini Files --------->')
    fav.loadFavs(configuration,bioses,setDict)
    # parse dat files
    print('\n<--------- Load FBA & Mame Dats --------->')
    dats = dat.parseDats(scriptDir,dataDir,[fbaKey,mame2003Key,mame2010Key],['FBAlphav0.2.97.43.dat','mame2003.dat','mame2010.dat'],usingSystems)
    # parse test files
    print('\n<--------- Load Tests Files --------->')
    allTests = test.loadTests(fbaKey,mame2003Key,mame2010Key,os.path.join(scriptDir,dataDir),usingSystems)
    # create bestarcade romsets
    print('\n<--------- Create Sets --------->')    
    createSets(allTests,dats)
    print("\n<--------- Detecting errors ----------->")
    checkErrors(allTests,configuration['keepLevel'])
# write gamelists, missing doctype on generated dat  ?
# use directory from script
# use windows thing