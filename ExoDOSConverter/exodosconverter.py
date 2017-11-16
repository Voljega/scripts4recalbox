#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys,collections
import os.path
import shutil
import subprocess

exoDosDir = r"E:\No-Intro-Collection_2015-03-03\eXoDOS_Collection_v2.0"
outputDir = r'E:\ExoDOSConverted'

DosGame = collections.namedtuple('DosGame', 'name genre subgenre publisher developer year frontPic about')

def isGoodLine(l,cLines):
    for cL in cLines :
        if l.strip().lower().startswith(cL) :
            return False    
    return True

def reducePath(path,game):    
    if path.startswith(".\games") or path.startswith("\games") or path.startswith("games") :
        pathList = path.split('\\')        
        if pathList[0]=='.' :
            pathList = pathList[1:]        
        if len(pathList) > 1 and pathList[0].lower()=='games' and pathList[1].lower()==game.lower() :
            cleanedPath = "."
            for pathElt in pathList[2:] :
                cleanedPath = cleanedPath + "\\" + pathElt            
            return cleanedPath
        else :
            return path
    else :
        return path


def cleanCue(old,new,cleanName):
    oldFile = open(old,'r')
    newFile = open(new,'w')   
    for line in oldFile.readlines() :        
        if line.startswith("FILE") :
            params = line.split('"')            
            params[1] = cleanName + "." + params[1].split(".")[-1].lower()
            line = '"'.join(params)
            print("cue FILE line -> " +line.rstrip('\n\r'))
            
        newFile.write(line)
    oldFile.close()
    newFile.close()
  
def cleanCDname(path,game,dest):
    pathFile = os.path.join(dest,path)    
    if os.path.exists(pathFile) :
        if os.path.isdir(pathFile) :            
            return path
        else :                     
            pathList = path.split('\\')
            filename = pathList[-1]                       
            cleanName = filename.split(".")[0].lower()
            ext = filename.split(".")[-1]
            if len(cleanName)>8 :
                cleanName = cleanName[0:7]            
            dirPath = "\\".join(pathFile.split('\\')[:-1])
            for file in os.listdir(dirPath) :
                if file.split(".")[0].lower() == filename.split(".")[0].lower() :        
                    if len(file.split("."))>1 and file.split(".")[-1].lower() == "cue" :
                        print("create new clean cue file "+cleanName+"."+file.split(".")[-1])
                        print(file)
                        sourceFile = file;
                        targetFile = cleanName+"."+file.split(".")[-1].lower();
                        source = os.path.join(dirPath,sourceFile)
                        target = os.path.join(dirPath,targetFile)
    #                    print("%s != %s %r" %(sourceFile.lower(),targetFile,not sourceFile.lower() == targetFile))
    #                    print("%s == %s %r" %(sourceFile.lower(),targetFile, sourceFile.lower() == targetFile))
                        if not sourceFile.lower() == targetFile :
                            cleanCue(source,target,cleanName)
                            os.remove(os.path.join(dirPath,file))
                        else :
                            print ("cue already well named")
                            cleanCue(source,target+"1",cleanName)
                            os.remove(os.path.join(dirPath,file))
                            os.rename(target+"1",target)
                    else :
                        print("renamed %s to %s" %(file,cleanName+"."+file.split(".")[-1].lower()))
                        #double rename to avoid problems of same name with different case
                        os.rename(os.path.join(dirPath,file),os.path.join(dirPath,cleanName+"."+file.split(".")[-1].lower()+"1"))
                        os.rename(os.path.join(dirPath,cleanName+"."+file.split(".")[-1].lower()+"1"),os.path.join(dirPath,cleanName+"."+file.split(".")[-1].lower()))
                    
            cleanedPath = "\\".join(pathList[:-1])+"\\"+cleanName+"."+ext.lower()
            print("modify dosbox.bat : %s -> %s" %(path,cleanedPath))
            return cleanedPath
    else :
        print("<ERROR> %s doesn't exist" %pathFile)
        return path
    
    

def handleCDMount(line,game,dest) :    
    line = line.replace("@","")#always show imgmount command    
    command = line.split(" ")    
    startIndex = -1
    endIndex = -1
    count =0
    for param in command :
        if param == 'd' or param == 'a' or param == 'b':
            startIndex = count
        elif param == '-t' :
            endIndex = count
        count = count + 1
    
    paths = command[startIndex+1:endIndex]    
    prString = ""
    for path in paths :
        path = reducePath(path.replace('"',""),game)        
        if len(paths)==1 :
            #HANDLE FILENAME FOR LEN(PATHS ) == 1
            path = cleanCDname(path,game,dest)        
        prString = prString + " "+path
    
    # treat mount a and d here
    if line.startswith("mount a") or line.startswith("mount d") :        
        prString = dest.replace(outputDir+"\\","/recalbox/share/roms/dos/") + "/" + prString.strip()        
        prString = ' "' + prString.replace("\\","/") +'"'        
    
    fullString = " ".join(command[0:startIndex+1]) + prString + " " + " ".join(command[endIndex:])
    print(fullString)
    return fullString

def createDosboxBat(lines,dbB,dbCCfg,game,dest) :
    gameDir = os.path.join(exoDosDir,"Games",game)
    #nécessaire de voir où est monté mount c ?
    cutLines = ["cd ..","@cd ..","cls","mount c","@mount c","#","exit"]
    for line in lines :
        # keep conf in dosbox.cfg but comment it
        dbCCfg.write("# "+line)
        if isGoodLine(line,cutLines) :
            #remove cd to gamedir            
            if line.lower().startswith("cd ") or line.lower().startswith("@cd") :                
                path = reducePath(line.rstrip('\n\r ').split(" ")[-1].rstrip('\n\r '),game)                
#                print("<%s> <%s>" %(path,game))                
#                print("? %s -> %r" %(os.path.join(gameDir,path),os.path.exists(os.path.join(gameDir,path))))
                if path.lower() == game.lower() and not os.path.exists(os.path.join(gameDir,path)):
                    print("analyzing cd path %s -> path is game name and no existing subpath, removed" %line.rstrip('\n\r '))
                else :
                    print("analyzing cd path %s -> kept" %line.rstrip('\n\r '))
                    dbB.write(line)
            elif line.lower().startswith("@imgmount d") or line.lower().startswith("imgmount d"):
                dbB.write(handleCDMount(line,game,dest))
                dbB.write("pause\n")
            elif line.lower().startswith("mount ") or line.lower().startswith("@mount "):
                dbB.write(handleCDMount(line,game,dest))
                dbB.write("pause\n")
            else :
                dbB.write(line)       
    #insérer pause

def convertConfiguration(game,genre) :
    dest = os.path.join(outputDir,genre,game+".pc")
    dbC = open(os.path.join(dest,"dosbox.conf"),'r')#original
    dbCCfg = open(os.path.join(dest,"dosbox.cfg"),'w')#recalbox dosbox.cfg
    dbB = open(os.path.join(dest,"dosbox.bat"),'w')#recalbox dosbox.bat
    
    count =0
    lines = dbC.readlines()
    for line in lines :
        if line.startswith("fullscreen"):
            dbCCfg.write("fullscreen=true\n")
        elif line.startswith("fullresolution"):
            dbCCfg.write("fullresolution=desktop\n")
        elif line.startswith("output"):
            dbCCfg.write("output=texture\n")
            dbCCfg.write("renderer = auto\n")
            dbCCfg.write("vsync=false\n")            
        elif line.startswith("buttonwrap") :            
            dbCCfg.write("buttonwrap=false\n")
        elif line.startswith("mapperfile"):
            dbCCfg.write("mapperfile=mapper.map\n")
        elif line.startswith("ultradir"):
            dbCCfg.write(r"ultradir=C:\ULTRASND")
            dbCCfg.write("\n")
        elif line.startswith("[autoexec]"):
            dbCCfg.write(line)            
            createDosboxBat(lines[count+1:],dbB,dbCCfg,game,dest)
            break
        else :
            dbCCfg.write(line)
    
        count = count +1
    
    dbC.close()    
    dbCCfg.close()
    dbB.close()    
    os.remove(os.path.join(dest,"dosbox.conf"))

def handleMetadata(game,gamesDosDir) :
    meagreDir = os.path.join(gamesDosDir,game,"Meagre")
    manualDir = os.path.join(meagreDir,"Manual")
    picDir = os.path.join(meagreDir,"Front")
    screenPicDir = os.path.join(meagreDir,"Screen")
    aboutFile = os.path.join(meagreDir,"About","about.txt")
    iniFileDir = os.path.join(meagreDir,"IniFile")
    
    iniFilename = os.path.join(iniFileDir,os.listdir(iniFileDir)[0])
    iniFile = open(iniFilename,'r')
    
    # Parse iniFile in iniFile dir    
    for line in iniFile.readlines() :
        confLine = line.split("=")
        key = confLine[0]        
        if key == "Name" :
            name = confLine[1].rstrip('\n\r ')
            safeEscapedName = name.replace(":","")
            safeEscapedName = safeEscapedName.replace("/","-")
            safeEscapedName = safeEscapedName.replace("?","")
            safeEscapedName = safeEscapedName.replace("*","-")
        elif key == "Genre" :
            genre = confLine[1].rstrip('\n\r ')
        elif key == "SubGenre" :
            subgenre = confLine[1].rstrip('\n\r ')
        elif key == "SubGenre2" :
            subgenre = subgenre + " " + confLine[1].rstrip('\n\r ')
        elif key == "Publisher" :
            publisher = confLine[1].rstrip('\n\r ')
        elif key == "Developer" :
            developer = confLine[1].rstrip('\n\r ')
        elif key == "Year" :
            year = confLine[1].rstrip('\n\r ')
        elif key == "Front01" :
            frontPic = confLine[1].rstrip('\n\r ')
        elif key == "Screen01" :
            screenPic = confLine[1].rstrip('\n\r ')
    #RECUPERER SCREEN SI FRONT N'EXISTE PAS
    
    front = os.path.join(picDir,frontPic)
    screen = os.path.join(screenPicDir,screenPic)
    #copy front pic if exists else screenPic
    if not os.path.exists(os.path.join(outputDir,"downloaded_images")) :
        os.mkdir(os.path.join(outputDir,"downloaded_images"))
    if os.path.exists(front) and not os.path.isdir(front):
        print("copy pic file %s to %s" %(frontPic,os.path.join(outputDir,"downloaded_images",safeEscapedName +" - front.jpg")))
        shutil.copy2(front,os.path.join(outputDir,"downloaded_images",safeEscapedName +" - front.jpg"))
        frontPic = "./downloaded_images/"+safeEscapedName +" - front.jpg"
    elif os.path.exists(screen) and not os.path.isdir(screen):
        print("copy pic file %s to %s" %(screenPic,os.path.join(outputDir,"downloaded_images",safeEscapedName +" - front.jpg")))
        shutil.copy2(screen,os.path.join(outputDir,"downloaded_images",safeEscapedName +" - front.jpg"))
        frontPic = "./downloaded_images/"+safeEscapedName +" - front.jpg"
    #copy manual files
    if not os.path.exists(os.path.join(outputDir,"manuals")) :
        os.mkdir(os.path.join(outputDir,"manuals"))
    manualFiles = os.listdir(manualDir)
    if len(manualFiles) > 0 and not os.path.exists(os.path.join(outputDir,"manuals",safeEscapedName)):
        os.mkdir(os.path.join(outputDir,"manuals",safeEscapedName))
    for manual in manualFiles:
        print("copy manual file %s to %s" %(manual,os.path.join(outputDir,"manuals",safeEscapedName,manual)))
        shutil.copy2(os.path.join(manualDir,manual),os.path.join(outputDir,"manuals",safeEscapedName,manual))
    # get content of about in About dir    
    about = open(aboutFile).read()
    
    #aboutFile.close() // mandatory ?
    iniFile.close()
                
    dosGame = DosGame(name,genre,subgenre,publisher,developer,year,"./downloaded_images/"+safeEscapedName +" - front.jpg",about)
    print("")
    print("Metadata for %s : %s (%s), genre: %s , subgenre: %s" %(game,dosGame.name,dosGame.year,dosGame.genre,dosGame.subgenre))    
#    print("publisher: %s , developer: %s" %(dosGame.publisher,dosGame.developer))
#    print("pic : %s" %dosGame.frontPic)    
    print("")
    return dosGame

def copyGameFiles(game,genre):
    print("copy %s game dir" %game)
    dest = os.path.join(outputDir,genre,game+".pc")
    shutil.copytree(os.path.join(exoDosDir,"Games",game),dest)
    print("copy dosbox conf")
    shutil.copy2(os.path.join(exoDosDir,"Games","!dos",game,"dosbox.conf"),os.path.join(dest,"dosbox.conf"))    

def copyMapper(game,genre):
    source = dest = os.path.join(outputDir,"mapper.map")
    dest = os.path.join(outputDir,genre,game+".pc","mapper.map")
    shutil.copy2(source,dest)

def writeGamelistEntry(gamelist,dosGame,game,genre):
    gamelist.write("    <game>\n")
    gamelist.write("        <path>./"+genre+"/"+game+".pc</path>\n")
    gamelist.write("        <name>"+dosGame.name+"</name>\n")
    gamelist.write("        <desc>"+dosGame.about+"</desc>\n")    
    gamelist.write("        <releasedate>"+dosGame.year+"0101T000000</releasedate>\n")
    gamelist.write("        <image>"+dosGame.frontPic+"</image>\n")
    gamelist.write("        <developer>"+dosGame.developer+"</developer>\n")
    gamelist.write("        <publisher>"+dosGame.publisher+"</publisher>\n")
    gamelist.write("        <genre>"+genre+"</genre>\n")
    gamelist.write("    </game>\n")

def buildGenre(dosGame):
    if dosGame.genre in ['Sports']:
        return dosGame.genre
    elif "Adventure" in dosGame.genre and "Action" in dosGame.subgenre :
        return "Action-Adventure"
    elif "Adventure" in dosGame.genre :
        return "Adventure"
    elif "Racing" in dosGame.genre :
        return "Race"
    elif dosGame.genre == 'Strategy' and "Board" in dosGame.subgenre:
        return 'Puzzle'
    elif dosGame.genre == 'Strategy' and not "Puzzle" in dosGame.subgenre:
        return 'Strategy-Gestion'
    elif dosGame.genre == 'Strategy' and "Puzzle" in dosGame.subgenre:
        return "Puzzle"
    elif dosGame.genre == 'Simulation' and 'Managerial' in dosGame.subgenre :
        return 'Strategy-Gestion'
    elif dosGame.genre == 'Simulation' and 'Sports' in dosGame.subgenre :
        return 'Sports'
    elif dosGame.genre == 'Simulation' and 'Pinball' in dosGame.subgenre :
        return 'Pinball'
    elif dosGame.genre == 'Simulation' :
        return 'Simulation'
    elif dosGame.genre == 'RPG':
        return 'RPG'
    elif dosGame.genre == 'Action' and 'Pinball' in dosGame.subgenre :
        return 'Pinball'
    elif dosGame.genre == 'Action' and "Puzzle" in dosGame.subgenre:
        return "Puzzle"
    elif dosGame.genre == 'Action' and 'Shooter' in dosGame.subgenre :
        return 'ShootEmUp'
    elif dosGame.genre == 'Action' and 'Platform' in dosGame.subgenre :
        return 'Platform'
    elif dosGame.genre == 'Action' and 'FPS' in dosGame.subgenre :
        return 'Gun-FPS'
    elif dosGame.genre == 'Action' and 'Fighting' in dosGame.subgenre :
        return 'BeatEmUp'
    elif dosGame.genre == 'Action' :
        return 'Action-Adventure'
    else :
        return 'Unknown'

def convert(nbGames):
    gamesDir = os.path.join(exoDosDir,"Games")
    gamesDosDir = os.path.join(gamesDir,"!dos")
    
    if not os.path.isdir(gamesDir) or not os.path.isdir(gamesDosDir) :
        print("%s doesn't seem to be a valid ExoDOSCollection folder" %exoDosDir)
        exit    
    
    gamelist = open(os.path.join(outputDir,"gamelist.xml"),'w')
    gamelist.write('<?xml version="1.0"?>\n')
    gamelist.write("<gameList>\n")
    
    
    games = [filename for filename in os.listdir(gamesDosDir)][:nbGames]
    
    for game in games :
        print("----------- Starting conversion for %s -----------" %game)
        
        if not os.path.exists(os.path.join(exoDosDir,"Games",game)):
            print("%s needs installation" %game)
            #automatic F and N
            subprocess.call("cmd /C (echo F&echo N) | Install.bat", cwd=os.path.join(gamesDosDir,game), shell=False)
#            subprocess.call("cmd /C Install.bat", cwd=os.path.join(gamesDosDir,game), shell=False)
            print("installed %s" %game)
        else :
            print("%s is already installed" %game)
        
        dosGame = handleMetadata(game,gamesDosDir)
        genre = buildGenre(dosGame)
        print("stuffed into genre %s" %genre)
        writeGamelistEntry(gamelist,dosGame,game,genre)
        
        if not os.path.exists(os.path.join(outputDir,genre,game+".pc")):
            copyGameFiles(game,genre)        
            convertConfiguration(game,genre)
            copyMapper(game,genre)
        
        print("----------- Finished conversion for %s -----------" %game)
        print("")
    
    gamelist.write("</gameList>\n")
    gamelist.close()

if __name__ == "__main__":
    nbGames = int(input("How many games do you want to convert ? : ").lower())
#    startGame = input("At which game do you want to start ")
    print("Convert %i games" %(nbGames))
    
    if not os.path.isdir(exoDosDir) :
        print("%s is not a directory or doesn't exist" %exoDosDir)
        exit
    
    if not os.path.isdir(outputDir) :
        print("%s is not a directory or doesn't exist" %outputDir)
        exit
        
    convert(nbGames)
        