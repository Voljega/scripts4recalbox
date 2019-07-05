#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys,os,shutil,collections
from random import randrange
import time
import pygame
from pygame.locals import *

cfgInDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
romsInDir = '/recalbox/share/roms'
logDir= '/recalbox/share/'
exclusionList = ['random','favorites','moonlight','imageviewer','prboom','ports','cavestory','lutro']
backgroundPic = 'background-random-{reso}.png'
reso = '1080'

System = collections.namedtuple('System', 'name fullname command games')
Game =  collections.namedtuple('Game', 'path name image emulator core genre')
Rdm = collections.namedtuple('Rdm','systems genres gamestrings')
arcadeSys = ['mame','daphne','fba','fba_libretro','neogeo']
desc = ' READY FOR A RANDOM{GENRE} GAME{SYSTEM} ?'
imgList = ['QuestionBlock-BLUE.png','QuestionBlock-GREEN.png','QuestionBlock-LIGHT-BLUE.png','QuestionBlock-LIGHT-GREEN.png','QuestionBlock-ORANGE.png','QuestionBlock-PINK.png','QuestionBlock-RED.png','QuestionBlock-YELLOW.png']
imgCount = 8;

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

# gets systems list
def systemList(p):
    systems=[]
    for i in etree.parse(p).findall(".//system"):
      system,fullname,command=get(i,"name"),get(i,"fullname"),get(i,"command")
      gamelistFile = os.path.join(romsInDir,system,"gamelist.xml")
      if (os.path.exists(gamelistFile) and system not in exclusionList ):
          s = System(system,fullname,command,[])
          systems.append(s)
          
    return systems

def showPic(image,syst) :
    backgroundFile = os.path.join(romsInDir, 'random', 'downloaded_images',backgroundPic.replace('{reso}',reso))
    log(backgroundFile)
    file = os.path.join(romsInDir, syst.name, image)
    if os.path.exists(file) :
        log('showPic %s' %file)
        # INITS
        pygame.init()
        pygame.mouse.set_visible(0)
        backgroundPicture = pygame.image.load(backgroundFile)
        picture = pygame.image.load(file)
        # # CREATE FULLSCREEN DISPLAY. X = 1920- Y = 1080
        fullscreen = pygame.display.set_mode((1920,1080), FULLSCREEN)
        fullscreen.blit(backgroundPicture, (0,0))
        # # PASTE PICTURE ON FULLSCREEN
        x = (1920 - picture.get_width()) /2
        y = (1080 - picture.get_height()) /2
        fullscreen.blit(picture, (x,y))
        # # SHOW FULLSCREEN 
        pygame.display.flip()
        # # WAIT 5 SECONDS (need import time)
        time.sleep(5)
        # # EXIT PYGAME (Not needed but recommanded)
        pygame.display.quit()
        pygame.quit()
    
# selects a game and launches command
def selectGame(system,games,ctrlStr,ratio):
    game = games[randrange(len(games))]
    core = game.core if game.core != None else 'default'
    emulator = game.emulator if game.emulator != None else 'default'
    log("Selected %s from system %s with core %s and emulator %s" % (game.name, system.name, core, emulator))
    command = system.command.replace('%SYSTEM%',system.name)
    command = command.replace('%ROM%','"' + game.path +'"')
    command = command.replace('%EMULATOR%',emulator)
    command = command.replace('%CORE%',core)
    command = command.replace('%CONTROLLERSCONFIG%',ctrlStr)
    command = command.replace('%RATIO%',ratio)
    command = command.replace('%NETPLAY%','')
    showPic(game.image,system)
    log('')
    log("out: "+command)
    os.popen(command)

def matchCriteria(game,genres,gamestrings) :
    gameGenre = get(game,'genre').lower() if get(game,'genre') is not None else None
    gameName = get(game,'name').lower() if get(game,'name') is not None else None
    genreB = gameGenre in genres if genres is not None and len(genres) > 0 else True
    stringB = False
    if gamestrings is not None and len(gamestrings) > 0 :
        for string in gamestrings :
            stringB = string in gameName or stringB
    else :
        stringB = True
        
    return stringB and genreB
    
# randomly selects a valid system (with games)
def selectableGames(syst, genres, gamestrings):
    gamelistFile = os.path.join(romsInDir,syst.name,"gamelist.xml")
    gs = []
    try :
        parser = etree.XMLParser(encoding="utf-8")
        games = etree.parse(gamelistFile, parser=parser).findall(".//game")
        games = list(filter(lambda x: matchCriteria(x, genres, gamestrings), games))
        if (len(games) > 0) : # remove systems with no games                        
            for g in games:                
                hidden = get(g,'hidden')
                gpath = os.path.join(romsInDir, syst.name , get(g,'path').encode('utf-8')) #full path to rom
                if (hidden != 'true' and os.path.exists(gpath)): #do not use hidden games and nonexistent files
                    gs.append(Game(gpath,get(g,'name'),get(g,'image'),get(g,'emulator'),get(g,'core'),get(g,'genre')))
            
            if (len(gs) > 0):
                     log("%i games matching in %s directory" % (len(gs),syst.name))
                     return gs
    except :
        print(str(sys.exc_info()))
        return gs
    

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

def cleanLog() :
    if os.path.exists(logDir + "randomlog.txt") :
        f = open(logDir + "randomlog.txt","r")
        nbLines = len(f.readlines())
        f.close()
        
        if nbLines > 200 :            
            os.remove(logDir + "randomlog.txt")
    
def log(stri, cr = True):
    print(stri)
    f = open(logDir + "randomlog.txt","a+")	
    f.write(stri)
    if cr :
        f.write('\n')
    f.close()
    
# get a system by name
def paramSystems(systems, rdmSystems):
   paramSystems = []
   if len(rdmSystems) ==0 :
        return systems
   else :
       for s in rdmSystems:
           rSystems = list(filter(lambda r: r.name.lower() == s, systems))
           if len(rSystems) > 0 :
            paramSystems.append(rSystems[0])
       return paramSystems
       
def readRdmFile(rdmFile) :
    file = open(rdmFile,'r')
    systems, genres, gamestrings = [],[],[]
    for line in file.readlines() :
        param = line.split(':')
        key=param[0].rstrip('\n\r ').lstrip(' ').lower()
        if key == 'systems' :
            systems =  param[1].lower().rstrip('\n\r ').replace(' ','').split(';')
        if key == 'genres' :
            genres =  param[1].lower().rstrip('\n\r ').lstrip(' ').split(';')
        if key == 'gamestrings' :
            gamestrings = param[1].lower().rstrip('\n\r ').replace(' ','').split(';')
            
    return Rdm(systems,genres,gamestrings)
    
def initWriteRdm(systName,fullname,g,randomDir,gamelist) :
    global imgCount
    if g is not None :
        f = open(os.path.join(randomDir,systName,systName+g.replace(' ','')+'.rdm'),'w')
        writeGamelistEntry(gamelist,'./'+systName+'/'+systName+g.replace(' ','')+'.rdm',fullname+' '+g,desc.replace('{GENRE}',' '+g).replace('{SYSTEM}',' ON '+fullname if systName is not 'all' else ''),'./downloaded_images/'+imgList[imgCount%8])
        imgCount = imgCount + 1
    else :
        f = open(os.path.join(randomDir,systName,systName+'All.rdm'),'w')
        writeGamelistEntry(gamelist,'./'+systName+'/'+systName+'All.rdm',fullname+' All',desc.replace('{GENRE}','').replace('{SYSTEM}',' ON '+fullname if systName is not 'all' else ''),'./downloaded_images/'+imgList[imgCount%8])
        imgCount = imgCount + 1
    if not systName == 'all' :
        if systName == 'arcade' :
            f.write('systems:'+';'.join(arcadeSys)+'\n')
        else :
            f.write('systems:'+systName+'\n')
    if g is not None :
        f.write('genres:'+g.lower()+'\n')
    f.close()

def initsystemSubFolder(systName,fullname,genres,randomDir,gamelist) :
    global imgCount
    sysDir = os.path.join(randomDir,systName)
    log('Init system: '+sysDir)
    if os.path.exists(sysDir) and 'random' in sysDir :
        shutil.rmtree(sysDir)
    os.mkdir(sysDir)
    writeGamelistFolder(gamelist,systName,fullname if not systName == 'all' else 'All','./downloaded_images/'+imgList[imgCount%8],None)
    imgCount = imgCount + 1
    log(sysDir +' genres: '+' '.join(genres))
    initWriteRdm(systName,fullname if not systName == 'all' else 'All',None,randomDir,gamelist)
    
    for g in genres :
        if g is not None :
            initWriteRdm(systName,fullname if not systName == 'all' else 'All',g,randomDir,gamelist)

def aggregateGenresList(genreDict,genres) :
    for genre in genres :
        if genre in genreDict :
            genreDict[genre] = genreDict[genre] +1
        else :
            genreDict[genre] = 1

def writeGamelistEntry(gamelist,romPath,name,desc,frontPic):
    gamelist.write("    <game>\n")
    gamelist.write("        <path>"+romPath+"</path>\n")
    gamelist.write("        <name>"+name+"</name>\n") if name else None
    gamelist.write("        <desc>"+desc+"</desc>\n") if desc else None
    gamelist.write("        <image>"+frontPic+"</image>\n") if frontPic else None
    gamelist.write("    </game>\n")
    
def writeGamelistFolder(gamelist,name,fullname,image,desc):
    gamelist.write("    <folder>\n")
    gamelist.write("        <path>./"+name+"</path>\n")
    gamelist.write("        <name>"+fullname+"</name>\n")
    gamelist.write("        <desc>"+desc+"</desc>\n") if desc else None
    gamelist.write("        <image>"+image+"</image>\n")
    gamelist.write("    </folder>\n")
            
def init() :
    log('INIT Random roms folder')
    respo = raw_input('Are you sure you stopped emulationstation (y/n) ? ')
    if respo.lower() not in ['y','yes'] :
        log("Use command '/etc/init.d/S31emulationstation stop' ;)")
        sys.exit()
    randomDir = os.path.join('/recalbox/share/roms', 'random')
    allGenres = dict()
    arcadeGenres = dict()
    gamelist = open(os.path.join(randomDir,"gamelist.xml"),'w')
    gamelist.write('<?xml version="1.0"?>\n')
    gamelist.write("<gameList>\n")
    for rSyst in recalboxSystems :
        genres = set([g.genre for g in selectableGames(rSyst,None,None)])
        if None in genres :
            log('WARNING syst '+rSyst.name+' has some games with no genre tag')
            genres.remove(None)
        initsystemSubFolder(rSyst.name,rSyst.fullname,genres,randomDir,gamelist)
        aggregateGenresList(allGenres,genres)
        if rSyst.name in arcadeSys :
            aggregateGenresList(arcadeGenres,genres)
    
    allGenres = list(filter(lambda g: allGenres[g] > 1, allGenres.keys()))
    initsystemSubFolder('all','',allGenres,randomDir,gamelist)
    arcadeGenres = list(filter(lambda g: arcadeGenres[g] > 1, arcadeGenres.keys()))
    initsystemSubFolder('arcade','Arcade',arcadeGenres,randomDir,gamelist)
    gamelist.write("</gameList>\n")
    gamelist.close()
    
if __name__ == "__main__":
    cleanLog()
    log('')
    log("---------")
    log("in: "+ " ".join(sys.argv))
    log('')
    # Load recalbox systems from es_systems.cfg (share_init) which have a gamelist
    recalboxSystems = systemList(cfgInDir)
    if sys.argv[-1].lower() == 'init' or len(sys.argv) == 1 :
        init()
        
    else :
        ctrlStr = parseControllerCfg(sys.argv[1:len(sys.argv)-2])
        ratio = sys.argv[-1]
        # Load systems, genres, gamestrings params from rdm content
        rdmParams = readRdmFile(sys.argv[-3])
        # Restrict selectable systems using params
        paramSystems = paramSystems(recalboxSystems,rdmParams.systems)
        log('Selectable systems based on your parameters: ',False)
        log(','.join([s.name for s in paramSystems]))
        log('Genre criteria: ',False)
        log(','.join(rdmParams.genres))
        log('Game strings criteria: ',False)
        log(','.join(rdmParams.gamestrings))
        log('')
        # Main loop
        
        while(len(paramSystems) > 0) :
            launchSyst = paramSystems[randrange(len(paramSystems))] if len(paramSystems) > 0  else recalboxSystems[randrange(len(recalboxSystems))]
            log('Randomly Selected System: '+launchSyst.name)
            possibleGames = selectableGames(launchSyst,rdmParams.genres,rdmParams.gamestrings)
            if possibleGames is not None and len(possibleGames) > 0 :
                selectGame(launchSyst,possibleGames,ctrlStr,ratio)
                break;
            else :
                log('No games matching your criterias in system '+launchSyst.name)
                paramSystems.remove(launchSyst)
                
        if(len(paramSystems) <= 0) :
            log('Sorry, no games matching your criterias in any system, maybe try different parameters ?')

# initialisation
# - generate rdm files
# - generate gamelist
# complete README with init thingy