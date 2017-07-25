#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys,os,glob,collections
from random import randrange

cfgInDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
romsInDir = '/recalbox/share/roms'
logDir= '/recalbox/share/'
exclusionList = ['random','favorites','moonlight','imageviewer']

System = collections.namedtuple('System', 'name command games')
Game =  collections.namedtuple('Game', 'path name image emulator core')

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

# gets systems list
def systemList(p):
    systems=[]
    for i in etree.parse(p).findall(".//system"):
      system,command=get(i,"name"),get(i,"command")
      gamelistFile = os.path.join(romsInDir,system,"gamelist.xml")
      if (os.path.exists(gamelistFile) and system not in exclusionList ):
          s = System(system,command,[])
          systems.append(s)
          
    return systems

# selects a game and launches command
def selectGame(syst,ctrlStr):    
    game = syst.games[randrange(len(syst.games))]
    core = game.core if game.core != None else 'default'
    emulator = game.emulator if game.emulator != None else 'default'
    log("Selected %s from system %s with core %s and emulator %s" % (game.name, syst.name, core, emulator))
    command = syst.command.replace('%SYSTEM%',syst.name)
    command = command.replace('%ROM%','"' + game.path +'"')
    command = command.replace('%EMULATOR%',emulator)
    command = command.replace('%CORE%',core)
    command = command.replace('%CONTROLLERSCONFIG%',ctrlStr)
    log("out: "+command)
    os.popen(command)

# randomly selects a valid system (with games)
def selectSystem(systems,syst):    
    gamelistFile = os.path.join(romsInDir,syst.name,"gamelist.xml")            
    try :
        parser = etree.XMLParser(encoding="utf-8")
        games = etree.parse(gamelistFile, parser=parser).findall(".//game")        
        if (len(games) > 0) : # remove systems with no games 
            gs = []            
            for g in games:                
                hidden = get(g,'hidden')
                gpath = os.path.join(romsInDir, syst.name , get(g,'path').encode('utf-8')) #full path to rom                
                if (hidden != 'true' and os.path.exists(gpath)): #do not use hidden games and nonexistent files
                    gs.append(Game(gpath,get(g,'name'),get(g,'image'),get(g,'emulator'),get(g,'core')))
            
            if (len(gs) > 0):
                     syst = System(syst.name,syst.command,gs)
                     log("%i games selected in %s directory" % (len(syst.games),syst.name))
                     return syst
            else :
                     print(" ")                            
    except :
        print(sys.exc_info())
    if len(syst.games) > 0 :
        return syst
    else :
        log("no games in %s directory" % syst.name)
        return selectSystem(systems,systems[randrange(len(systems))])#unvalid system, reselect

# manages spaces in controllers names
def parseControllerCfg(arg):
    for i in range(1,6):
       pname = "-p" + str(i) + "name"
       try:
           pindex = arg.index(pname)
           arg[pindex+1] = '"' + arg[pindex+1] + '"'           
       except ValueError:
           print ("%s not in args list" %pname)
    
    return " ".join(arg)    

def log(stri):
    print(stri)
    f = open(logDir + "randomlog.csv","a+")	
    f.write(stri +"\n")
    f.close()
    
# get a system by name
def getSystem(systems, param):
   name=os.path.splitext(os.path.split(param)[1])[0]
   for s in systems:
       if s.name==name: return s
    
if __name__ == "__main__":
    log("---------")
    log("in: "+ " ".join(sys.argv))
    ctrlStr = parseControllerCfg(sys.argv[1:len(sys.argv)-2])    
    systems = systemList(cfgInDir)
    paramSystem = getSystem(systems,sys.argv[-1])    
    launchSyst = paramSystem if paramSystem != None else systems[randrange(len(systems))]    
    ssystem = selectSystem(systems,launchSyst)
    selectGame(ssystem,ctrlStr)