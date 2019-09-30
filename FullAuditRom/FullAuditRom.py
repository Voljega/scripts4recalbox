#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys,os,glob,collections,gamelist
from random import randrange
#reload(sys)
#sys.setdefaultencoding('utf-8')

# LOCAL
#cfgInDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
#romsInDir = '/recalbox/share/roms'
#logDir= '/recalbox/share/'

# USB_SHARE
cfgInDir = r'I:\recalbox\system\.emulationstation\es_systems.cfg'
romsInDir = r'I:\recalbox\roms'
logDir= r'C:\Temp\Prov'

exclusionList = ['random','favorites','moonlight','imageviewer']

System = collections.namedtuple('System', 'name extension games')
GameEntry =  collections.namedtuple('Game', 'isFolder abspath path name desc releasedate image imagePath, developer publisher genre hidden romExist imgExist scraped')

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

def findUnscrapped(roms,gRoms) :
    unscrappedCount = 0
    for rom in roms :
        found = False
        pathRom = rom.split('\\')[-1]        
        for grom in gRoms :        
            gRomPath = grom.path.split('/')[-1]            
            if pathRom == gRomPath :
                found = True
        if not found and 'Moaar' not in rom and 'downloaded_images' not in rom and 'manuals' not in rom and '\Extras\\' not in rom :            
            unscrappedCount = unscrappedCount + 1
        else :
            roms.remove(rom)

    return unscrappedCount

def gameListExtraction (syst,roms) :         
    gamelistRoms = gamelist.read(os.path.join(romsInDir,syst.name), False)
    
#    for g in gamelistRoms:
#        print(g.abspath)
#        if g.abspath in roms :
#            roms.remove(g.abspath)                    
#            
#    print("unscraped roms left : %i" % len(roms))
#    print("unscraped roms left : %i" % findUnscrapped(roms,gamelistRoms))
#    for r in roms :        
#        gamelistRoms.append(GameEntry(False,None,None,r,None,None,None,None,None,None,None,False,True,False,False))
    
    return gamelistRoms   

# gets systems list
def systemList(p):
    systems=[]
    for i in etree.parse(p).findall(".//system"):
      system,extension=get(i,"name"),get(i,"extension")
      if system == "odyssey2" : system = "o2em"      
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

def listDirBasedRoms(dir,extensions) :    
    roms = []
    romsFound = [os.path.join(dir,filename) for filename in os.listdir(dir) if isRom(filename,extensions) and os.path.isdir(os.path.join(dir,filename))]
    roms = roms + romsFound
    subDirs = [os.path.join(dir,filename) for filename in os.listdir(dir) if not isRom(filename,extensions) and os.path.isdir(os.path.join(dir,filename))]
    
    for subDir in subDirs :        
        roms = roms + listDirBasedRoms(subDir,extensions)
        
    return roms
    
def parseSystems(systems) :
    pSystems = []
    for system in systems :
        print("<--Auditing "+system.name+"-->")
        sysPath = os.path.join(romsInDir,system.name);
        extensions = system.extension.split(" ")
        print("Listing roms")
        print("dir based system: %r" %(system.name not in ['dos','daphne']))
        roms = listRoms(sysPath,extensions) if system.name not in ['dos','daphne'] else listDirBasedRoms(sysPath,extensions)
        print("found %i roms for %s" % (len(roms),system.name))        
        print("Reading gamelist")
        pSystems.append(System(system.name, system.extension, gameListExtraction(system,roms)))
        
    return pSystems

def cleanName(name):
    if name is not None :    
        firstOPar = name.find('[')
        if not firstOPar == -1 :
            name = name[:firstOPar]
        firstOPar = name.find('(')
        if not firstOPar == -1 :
            name = name[:firstOPar]
            
        return name.rstrip()
    else :
        return None

def genCSV(systems):
    print('\n')
    print('<--CSV generation-->')
    fid = open(os.path.join(logDir,"romListing.csv"),"w",encoding="utf-8")
    try :
        fid.write('System;Name;CleanedName;RomExists;ImageExists;Scraped;Hidden;Path;ImagePath\n')
        for s in systems:
            print("Generating CSV for %s , %i games" %(s.name,len(s.games)))
            for g in s.games :
#                print(s.name+';'+g.name+';'+cleanName(g.name)+';'+g.romExist+';'+g.imgExist+';'+g.scraped+';'+g.hidden+';'+g.path+';'+g.imagePath)                                
                fid.write('%s;%s;%s;%r;%r;%r;%r;%s;%s\n' % (s.name, g.name, cleanName(g.name), g.romExist, g.imgExist, g.scraped, g.hidden, g.path , g.imagePath))
    
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
    