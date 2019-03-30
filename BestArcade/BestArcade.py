#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys, collections
import os.path
import shutil
import conf, fav, test, dat, gamelist

scriptDir = r""

dataDir = r"data"
outputDir = r"output"
confFile = r"conf.conf"

fbaKey = "fba_libretro"
mame2010Key = "mame2010"
mame2003Key = "mame2003"
setKeys = [fbaKey,mame2003Key,mame2010Key]
datsDict = dict(zip(setKeys,['FBAlphav0.2.97.43.dat','mame2003.dat','mame2010.dat']))

extension = ".zip"

bioses = ['acpsx','atarisy1','cpzn1','cpzn2','cvs2gd','cvsgd','decocass','konamigv','konamigx','megaplay',
        'megatech','neogeo','nss','pgm','playch10','skns','stvbios','taitofx1','taitogn','taitotz','tps',
        'atarisy1','coh1000t','hng64','crysbios','coh1000a','coh1002e','coh1001l','coh1002m','coh1000t',
        'sys573','sys246','sys256','chihiro','naomi','naomigd','ar_bios','aleck64']

setDict = dict()
configuration = dict()
usingSystems = []

def setFileCopy(romsetFile,genre,fileName,targetDir,useGenreSubFolder) :
#    print('mockCopyFile',romsetFile)
    if os.path.exists(romsetFile) :
        if useGenreSubFolder :
            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,genre,fileName+".zip"))
        else :
            shutil.copy2(romsetFile, os.path.join(configuration['exportDir'],targetDir,fileName+".zip"))

def computeScore(setKey,setDir,game,test) :
    score = test[setKey].status if (test is not None and setKey in test) else -2
    
    if score == -2 and os.path.exists(os.path.join(setDir,game+".zip")) :
        score = -1 
    
    return score

def isPreferedSetForGenre(configuration,genre,keySet) :        
    return configuration[genre+'PreferedSet'] == keySet

def keepSet(keepNotTested,usePreferedSetForGenre,exclusionType,keepLevel,scores,key,genre,keep) :        
    maxScore = max(scores.values())
    if keepNotTested and scores[key] == -1 :        
        return True
    elif exclusionType == 'NONE' :
        return scores[key] >= keepLevel
    elif exclusionType == 'EQUAL' :
        if scores[key] == maxScore :
            return scores[key] >= keepLevel
    elif exclusionType == 'STRICT' :
        genreTest = genre.replace('[','')
        genreTest = genreTest.replace(']','')
        if usePreferedSetForGenre and configuration[genreTest+'PreferedSet'] : # check not empty
            if isPreferedSetForGenre(configuration,genreTest,key):
                return scores[key] >= keepLevel
            else :
                return False
        if scores[key] == maxScore :
            if key == configuration['preferedSet'] :                
                return scores[key] >= keepLevel
            elif fbaKey not in keep and mame2010Key not in keep:  # check not already in keep
                return scores[key] >= keepLevel
                
def writeCSV(csvFile,game,score,genre,dat,test,setKey) :
    if game in dat :
        name = dat[game].description
        year = dat[game].year
        manufacturer = dat[game].manufacturer
    else :
        name, year, manufacturer = '','',''
        
    if test is not None and setKey in test :
        hardware = test[setKey].hardware
        comments = test[setKey].comments
        notes = test[setKey].notes
    else :
        hardware,comments,notes = '','',''
    
    genreExport = genre.replace('[','')
    genreExport = genreExport.replace(']','')    
    csvFile.write("%i;%s;%s;%s;%s;%s;%s;%s;%s\n" 
                  %(score,genreExport,name,game,year,manufacturer,hardware,comments,notes))

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
        if '[' in name :
            indPar = name.index('[')
            name = name[:(indPar-1)].strip()                    
            
        year = dat[game].year if dat[game].year else ''
        developer = dat[game].manufacturer.replace('&', '&amp;') if dat[game].manufacturer else ''
        cloneof = dat[game].cloneof
    else :
        fullName, name, year, developer, cloneof = '','','','',''
        
    if test is not None and setKey in test :
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
    
    print("Creating or cleaning output directory %s" %configuration['exportDir'])
    if os.path.exists(configuration['exportDir']) :
        for file in os.listdir(os.path.join(configuration['exportDir'])) :
            fullPath = os.path.join(configuration['exportDir'],file)        
            shutil.rmtree(fullPath) if os.path.isdir(fullPath) else os.remove(fullPath)
    else :
        os.makedirs(configuration['exportDir'])
        
    notInAnySet = []
    onlyInOneSet = dict()
    useGenreSubFolder = True if configuration['genreSubFolders'] == '1' else False
    keepNotTested = True if configuration['keepNotTested'] == '1' else False
    keepLevel = int(configuration['keepLevel'])
    usePreferedSetForGenre = True if configuration['usePreferedSetForGenre'] == '1' else False    
    
    scoreSheet = open(os.path.join(configuration['exportDir'],"scoreSheet.csv"),"w",encoding="utf-8")
    scoreSheet.write('rom;fbaScore;mame2003Score;mame2010Score\n')
    
    CSVs, gamelists, roots = dict(), dict(), dict()
    header="Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
    for setKey in usingSystems :
        # init CSVS
        CSVs[setKey] = open(os.path.join(configuration['exportDir'],setKey+".csv"),"w",encoding="utf-8")
        CSVs[setKey].write(header)
        # init gamelists
        roots[setKey] = etree.Element("datafile")
        roots[setKey].append(dats[setKey+"Header"])   
        os.makedirs(os.path.join(configuration['exportDir'],setKey))
        gamelists[setKey] = gamelist.init(os.path.join(configuration['exportDir'],setKey))
    
    for genre in setDict.keys() :
        print("Handling genre %s" %genre)
        
        if useGenreSubFolder :
            for setKey in usingSystems :
                os.makedirs(os.path.join(configuration['exportDir'],setKey,genre))
            
        # copy bios in each subdirectory
        for bios in bioses :
            for setKey in usingSystems :
                setBios = os.path.join(configuration[setKey],bios+".zip")
                setFileCopy(setBios,genre,bios,setKey,useGenreSubFolder)
                writeGamelistHiddenEntry(gamelists[setKey],bios,genre,useGenreSubFolder)
        
        for game in sorted(setDict[genre]) :
            audit = game +" -> "            
            scores = dict()
            testForGame = allTests[game] if game in allTests else None
            
            for setKey in setKeys :    
                scores[setKey] = computeScore(setKey,configuration[setKey],game,testForGame) if setKey in usingSystems else -2                
            
#            printDict(scores) if game == 'jdredd' else None
            
            audit = audit + " SCORES: "+ str(scores[fbaKey]) + " " + str(scores[mame2003Key]) + " " + str(scores[mame2010Key]) + " ,"                                    
            scoreSheet.write('%s;%i;%i;%i\n' %(game,scores[fbaKey], scores[mame2003Key], scores[mame2010Key]))
            
            selected = []
            for setKey in usingSystems :
                selected.append(setKey) if keepSet(keepNotTested,usePreferedSetForGenre,configuration['exclusionType'],keepLevel,scores,setKey,genre,selected) else None
            
            audit = audit + " SELECTED: "+ str(selected)
            
            for setKey in usingSystems :
                setRom = os.path.join(configuration[setKey],game+".zip")
                if setKey in selected :
                    setFileCopy(setRom,genre,game,setKey,useGenreSubFolder)                
                    writeCSV(CSVs[setKey],game,scores[setKey],genre,dats[setKey],testForGame,setKey)
                    writeGamelistEntry(gamelists[setKey],game,dats[setKey],genre,useGenreSubFolder,testForGame,setKey)
                    roots[setKey].append(dats[setKey][game].node) if game in dats[setKey] else None              
            
            if len(selected) == 0 :                
                notInAnySet.append(game)
            elif len(selected) == 1 :
                if selected[0] not in onlyInOneSet :
                    onlyInOneSet[selected[0]] = []
                onlyInOneSet[selected[0]].append(game)
            
            print("    %s" %audit)
    
    # writing and closing everything
    for setKey in usingSystems :
        treeSet = etree.ElementTree(roots[setKey])
        treeSet.write(os.path.join(configuration['exportDir'],setKey+".dat"), xml_declaration=True, encoding="utf-8")
        CSVs[setKey].close()
        gamelist.close(gamelists[setKey])    
    
    scoreSheet.close()
        
    print ("\n<------------------ RESULTS ------------------>")
    print("NOT FOUND IN ANY SET : %i" %len(notInAnySet))
    print(notInAnySet)
    print("ONLY IN ONE SET :")
    printDict(onlyInOneSet)          
    
def checkErrors(inputTests,keepLevel) :        
    print("Input Tests")
    test.loadTests(setKeys,os.path.join(scriptDir,dataDir),usingSystems)
    print("Output Tests")
    outputTests = test.loadTests(setKeys,os.path.join(configuration['exportDir']),usingSystems)
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
    for setKey in setKeys :
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
    # create setDict containing fav games
    print('\n<--------- Load Favorites Ini Files --------->')
    fav.loadFavs(scriptDir,bioses,setDict)
    # parse dat files
    print('\n<--------- Load FBA & Mame Dats --------->')
    dats = dat.parseDats(scriptDir,dataDir,datsDict,usingSystems)
    # parse test files
    print('\n<--------- Load Tests Files --------->')
    allTests = test.loadTests(setKeys,os.path.join(scriptDir,dataDir),usingSystems)
    # create bestarcade romsets
    print('\n<--------- Create Sets --------->')    
    createSets(allTests,dats)
    print("\n<--------- Detecting errors ----------->")
    checkErrors(allTests,configuration['keepLevel'])
    print('<--------- Process finished ----------->')
    input('\n             (Press Enter)              ')

# TODOS
# missing doctype on generated dat  ?
# generate new release
