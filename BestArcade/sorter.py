#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import os.path, shutil
import gamelist

class Sorter :
    
    fbaKey = "fba_libretro"
    mame2010Key = "mame2010"
    mame2003Key = "mame2003"
    setKeys = [fbaKey,mame2003Key,mame2010Key]
    
    bioses = ['acpsx','atarisy1','cpzn1','cpzn2','cvs2gd','cvsgd','decocass','konamigv','konamigx','megaplay',
        'megatech','neogeo','nss','pgm','playch10','skns','stvbios','taitofx1','taitogn','taitotz','tps',
        'atarisy1','coh1000t','hng64','crysbios','coh1000a','coh1002e','coh1001l','coh1002m','coh1000t',
        'sys573','sys246','sys256','chihiro','naomi','naomigd','ar_bios','aleck64','neocdz','isgsm',
        'midssio','nmk004','ym2608']
    
    def __init__(self,configuration,usingSystems,favorites,scriptDir) :
        self.configuration = configuration
        self.usingSystems = usingSystems
        self.favorites = favorites
        self.scriptDir = scriptDir
    
    def setFileCopy(self,romsetFile,genre,fileName,targetDir,useGenreSubFolder,dryRun) :
        if not dryRun :         
            if os.path.exists(romsetFile) :
                if useGenreSubFolder :
                    shutil.copy2(romsetFile, os.path.join(self.configuration['exportDir'],targetDir,genre,fileName+".zip"))
                else :
                    shutil.copy2(romsetFile, os.path.join(self.configuration['exportDir'],targetDir,fileName+".zip"))

    def setImageCopy(self,paths,fileName,targetDir,dryRun) :
        if not dryRun :
            for path in paths.split(';') :
                filePath = os.path.join(path.strip(),fileName)            
                if os.path.exists(filePath):
                    shutil.copy2(filePath, os.path.join(self.configuration['exportDir'],targetDir,'downloaded_images',fileName))
                    return
    
    def computeScore(self,setKey,setDir,game,test) :
        score = test[setKey].status if (test is not None and setKey in test) else -2
        
        if score == -2 and os.path.exists(os.path.join(setDir,game+".zip")) :
            score = -1 
        
        return score
    
    def isPreferedSetForGenre(self,genre,keySet) :        
        return self.configuration[genre+'PreferedSet'] == keySet
    
    def keepSet(self,keepNotTested,usePreferedSetForGenre,exclusionType,keepLevel,scores,key,genre,keep) :        
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
            if usePreferedSetForGenre and self.configuration[genreTest+'PreferedSet'] : # check not empty
                if self.isPreferedSetForGenre(genreTest,key):
                    return scores[key] >= keepLevel
                else :
                    return False
            if scores[key] == maxScore :
                if key == self.configuration['preferedSet'] :                
                    return scores[key] >= keepLevel
                elif self.fbaKey not in keep and self.mame2010Key not in keep:  # check not already in keep
                    return scores[key] >= keepLevel
                    
    def writeCSV(self,csvFile,game,score,genre,dat,test,setKey) :
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
    
    def getStatus(self,status) :
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
    
    def writeGamelistHiddenEntry(self,gamelistFile,game,genre,useGenreSubFolder) :
        gamelist.writeGamelistHiddenEntry(gamelistFile,game+".zip",genre,useGenreSubFolder)
        
    def writeGamelistEntry(self,gamelistFile,game,image,dat,genre,useGenreSubFolder,test,setKey):
        frontPic = "./downloaded_images/"+image
        
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
            status = self.getStatus(test[setKey].status)        
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
    
    def createSets(self,allTests,dats) :
        
        print("Creating or cleaning output directory %s" %self.configuration['exportDir'])
        if os.path.exists(self.configuration['exportDir']) :
            for file in os.listdir(os.path.join(self.configuration['exportDir'])) :
                fullPath = os.path.join(self.configuration['exportDir'],file)        
                shutil.rmtree(fullPath) if os.path.isdir(fullPath) else os.remove(fullPath)
        else :
            os.makedirs(self.configuration['exportDir'])
            
        notInAnySet = []
        onlyInOneSet = dict()
        dryRun = True if self.configuration['dryRun'] == '1' else False
        useGenreSubFolder = True if self.configuration['genreSubFolders'] == '1' else False
        keepNotTested = True if self.configuration['keepNotTested'] == '1' else False
        keepLevel = int(self.configuration['keepLevel'])
        usePreferedSetForGenre = True if self.configuration['usePreferedSetForGenre'] == '1' else False
        scrapeImages = True if self.configuration['useImages'] == '1' and self.configuration['images'] else False
        
        scoreSheet = open(os.path.join(self.configuration['exportDir'],"scoreSheet.csv"),"w",encoding="utf-8")
        scoreSheet.write('rom;fbaScore;mame2003Score;mame2010Score\n')
        
        CSVs, gamelists, roots = dict(), dict(), dict()
        header="Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
        for setKey in self.usingSystems :
            # init CSVS
            CSVs[setKey] = open(os.path.join(self.configuration['exportDir'],setKey+".csv"),"w",encoding="utf-8")
            CSVs[setKey].write(header)
            # init gamelists
            roots[setKey] = etree.Element("datafile")
            roots[setKey].append(dats[setKey+"Header"])   
            os.makedirs(os.path.join(self.configuration['exportDir'],setKey))
            os.makedirs(os.path.join(self.configuration['exportDir'],setKey,'downloaded_images')) if scrapeImages else None        
            gamelists[setKey] = gamelist.initWrite(os.path.join(self.configuration['exportDir'],setKey))
        
        for genre in self.favorites.keys() :
            print("Handling genre %s" %genre)
            
            if useGenreSubFolder :
                for setKey in self.usingSystems :
                    os.makedirs(os.path.join(self.configuration['exportDir'],setKey,genre))
                    if scrapeImages :
                        gamelist.writeGamelistFolder(gamelists[setKey],genre,genre+'.png')
                        self.setImageCopy(os.path.join(self.scriptDir,'data','images'),genre+'.png',setKey,dryRun)
                
            # copy bios in each subdirectory
            for bios in self.bioses :
                for setKey in self.usingSystems :
                    setBios = os.path.join(self.configuration[setKey],bios+".zip")
                    self.setFileCopy(setBios,genre,bios,setKey,useGenreSubFolder,dryRun)
                    self.writeGamelistHiddenEntry(gamelists[setKey],bios,genre,useGenreSubFolder)
            
            for game in sorted(self.favorites[genre]) :
                audit = game +" -> "            
                scores = dict()
                testForGame = allTests[game] if game in allTests else None
                
                for setKey in self.setKeys :    
                    scores[setKey] = self.computeScore(setKey,self.configuration[setKey],game,testForGame) if setKey in self.usingSystems else -2                
                
                audit = audit + " SCORES: "+ str(scores[self.fbaKey]) + " " + str(scores[self.mame2003Key]) + " " + str(scores[self.mame2010Key]) + " ,"                                    
                scoreSheet.write('%s;%i;%i;%i\n' %(game,scores[self.fbaKey], scores[self.mame2003Key], scores[self.mame2010Key]))
                
                selected = []
                for setKey in self.usingSystems :
                    selected.append(setKey) if self.keepSet(keepNotTested,usePreferedSetForGenre,self.configuration['exclusionType'],keepLevel,scores,setKey,genre,selected) else None
                
                audit = audit + " SELECTED: "+ str(selected)
                
                for setKey in self.usingSystems :
                    setRom = os.path.join(self.configuration[setKey],game+".zip")
                    image = self.configuration['imgNameFormat'].replace('{rom}',game)
                    if setKey in selected :
                        self.setFileCopy(setRom,genre,game,setKey,useGenreSubFolder,dryRun)                
                        self.writeCSV(CSVs[setKey],game,scores[setKey],genre,dats[setKey],testForGame,setKey)
                        self.writeGamelistEntry(gamelists[setKey],game,image,dats[setKey],genre,useGenreSubFolder,testForGame,setKey)
                        roots[setKey].append(dats[setKey][game].node) if game in dats[setKey] else None
                        if scrapeImages :                          
                            self.setImageCopy(self.configuration['images'],image,setKey,dryRun)
                
                if len(selected) == 0 :                
                    notInAnySet.append(game)
                elif len(selected) == 1 :
                    if selected[0] not in onlyInOneSet :
                        onlyInOneSet[selected[0]] = []
                    onlyInOneSet[selected[0]].append(game)
                
                print("    %s" %audit)
        
        # writing and closing everything
        for setKey in self.usingSystems :
            treeSet = etree.ElementTree(roots[setKey])
            treeSet.write(os.path.join(self.configuration['exportDir'],setKey+".dat"), xml_declaration=True, encoding="utf-8")
            CSVs[setKey].close()
            gamelist.closeWrite(gamelists[setKey])    
        
        scoreSheet.close()
            
        print ("\n<------------------ RESULTS ------------------>")
        print("NOT FOUND IN ANY SET : %i" %len(notInAnySet))
        print(notInAnySet)               