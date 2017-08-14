#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys,os,glob,collections
from random import randrange
reload(sys)
sys.setdefaultencoding('utf-8')

cfgInDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
romsInDir = '/recalbox/share/roms'
logDir= '/recalbox/share/'
exclusionList = ['random','favorites','moonlight','imageviewer']

System = collections.namedtuple('System', 'name extension games')
Game =  collections.namedtuple('Game', 'path name image hidden romExist imgExist scraped')

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

def gameListExtraction (syst,roms) :
    gamelistFile = os.path.join(romsInDir,syst.name,"gamelist.xml")
    gs = []
    
    if os.path.exists(gamelistFile) :
        parser = etree.XMLParser(encoding="utf-8")
        games = etree.parse(gamelistFile, parser=parser).findall(".//game")
        
        for g in games:
            try :
                path = get(g,'path')
                gpath = os.path.join(romsInDir, syst.name , get(g,'path').encode('utf-8').replace('./','')) #full path to rom
                name = get(g,'name')#.encode('utf-8') if get(g,'name') is not None else None
                image = get(g,'image').encode('utf-8').replace('./','') if get(g,'image') is not None else None
                imagePath = os.path.join(romsInDir, syst.name , image) if image is not None else None
                imageExists = os.path.exists(imagePath) if imagePath is not None else False
                gs.append(Game(gpath,name,imagePath,get(g,'hidden'),os.path.exists(gpath),imageExists,True))
                if gpath in roms :
                    roms.remove(gpath)
                    
            except :
                print(sys.exc_info())
                
        print("unscraped roms left : %i" % len(roms))
        for r in roms :
            gs.append(Game(r,None,None,None,True,False,False))
    
    return gs
    

# gets systems list
def systemList(p):
    systems=[]
    for i in etree.parse(p).findall(".//system"):
      system,extension=get(i,"name"),get(i,"extension")
      if system == "odyssey2" : system = "o2em"
      gamelistFile = os.path.join(romsInDir,system,"gamelist.xml")
      if (system not in exclusionList ):
          s = System(system,extension,[])
          systems.append(s)
          
    return systems

def isRom(filename,extensions) :
    for ext in extensions :
        if filename.endswith(ext) :
            return True
            
    return False
    
def listRoms(dir,extensions) :
    roms = []
    romsFound = [os.path.join(dir,filename) for filename in os.listdir(dir) if isRom(filename,extensions) and not os.path.isdir(os.path.join(dir,filename)) ]
    roms = roms + romsFound
    subDirs = [os.path.join(dir,filename) for filename in os.listdir(dir) if os.path.isdir(os.path.join(dir,filename))]
    
    for subDir in subDirs :
        roms = roms + listRoms(subDir,extensions)
        
    return roms
    
def parseSystems(systems) :
    pSystems = []
    for system in systems :
        sysPath = os.path.join(romsInDir,system.name);
        extensions = system.extension.split(" ")
        roms = listRoms(sysPath,extensions)
        print("found %i roms for %s" % (len(roms),system.name))
        pSystems.append(System(system.name, system.extension, gameListExtraction(system,roms)))
        
    return pSystems

def genCSV(systems):
    fid = open(os.path.join(logDir,"romListing.csv"),"w+")
    try :
        fid.write('System;Name;RomExists;ImageExists;Scraped;Hidden;Path;ImagePath\n')
        for s in systems:
            print("Generating CSV for %s , %i games" %(s.name,len(s.games)))
            for g in s.games :                
                fid.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (s.name, g.name.encode('utf-8') if g.name is not None else None, g.romExist, g.imgExist, g.scraped, g.hidden, g.path.encode('utf-8') if g.path is not None else None , g.image.encode('utf-8') if g.image is not None else None))
    
    finally :
        fid.close()
        
# get a system by name
def getSystem(systems, params):
    paramSys = []
    for p  in params :
        for s in systems :
            if p == s.name : paramSys.append(s)
            
    return paramSys
    
if __name__ == "__main__":
    systems = systemList(cfgInDir)
    paramSystems = getSystem(systems,sys.argv)
    genCSV(parseSystems(systems if len(paramSystems) ==0 else paramSystems))
    