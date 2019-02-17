#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys

inDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
outDir = '/recalbox/share/system/.emulationstation/es_systems.cfg'

# Sort orders
alphabetical = ['3do','amstradcpc','amiga600','amiga1200','amigacd32','apple2','atari2600','atari5200','atari7800','atari800','atarist','c64','cavestory','channelf','colecovision','daphne','dos','dreamcast','fba','fba_libretro','fds','gb','gba','gbc','gamecube','gamegear','gw','intellivision','jaguar','lutro','lynx','mame','mastersystem','megadrive','moonlight','msx','msx1','msx2','neogeo','neogeocd','ngp','ngpc','n64','nds','nes','o2em','oricatmos','pc98','pcengine','pcenginecd','pcfx','pokemini','ports','prboom','psx','psp','samcoupe','satellaview','saturn','scummvm','sega32x','segacd','sg1000','sufami','supergrafx','snes','thomson','vectrex','virtualboy','wii','wswan','wswanc','x68000','zx81','zxspectrum','imageviewer','random','favorites']
hardwareType = ['channelf','atari2600','o2em','intellivision','colecovision','vectrex','atari5200','nes','sg1000','atari7800','mastersystem','fds','pcengine','megadrive','pcenginecd','supergrafx','snes','neogeo','segacd','sega32x','3do','jaguar','saturn','neogeocd','psx','pcfx','satellaview','sufami','n64','dreamcast','gamecube','wii','gw','gb','lynx','gamegear','virtualboy','gbc','ngp','ngpc','wswan','wswanc','gba','pokemini','nds','psp','fba','fba_libretro','mame','daphne','apple2','atari800','c64','zx81','pc98','zxspectrum','msx','msx1','amstradcpc','oricatmos','thomson','msx2','atarist','x68000','amiga600','samcoupe','amiga1200','dos','scummvm','prboom','ports','lutro','cavestory','moonlight','imageviewer','random','favorites']
chronological =['channelf','apple2','atari2600','o2em','intellivision','atari800','colecovision','c64','vectrex','atari5200','gw','zx81','pc98','zxspectrum','nes','msx','msx1','sg1000','atari7800','amstradcpc','oricatmos','mastersystem','thomson','msx2','atarist','fds','x68000','pcengine','amiga600','megadrive','pcenginecd','supergrafx','samcoupe','gb','lynx','snes','gamegear','neogeo','segacd','sega32x','amiga1200','3do','jaguar','saturn','neogeocd','psx','pcfx','virtualboy','satellaview','sufami','n64','dreamcast','gbc','ngp','ngpc','wswan','wswanc','gba','pokemini','gamecube','nds','psp','wii','daphne','fba','fba_libretro','mame','dos','scummvm','prboom','ports','lutro','cavestory','moonlight','imageviewer','random','favorites']
retrochrono = chronological[::-1][14::] + chronological[-14::] #14 last systems not ordered chronologically
manufacturer =['amstradcpc','apple2','atari2600','atari800','atari5200','atari7800','atarist','lynx','jaguar','wswan','wswanc','c64','amiga600','amiga1200','o2em','colecovision','channelf','vectrex','intellivision','msx','msx1','msx2','samcoupe','pc98','pcengine','pcenginecd','supergrafx','pcfx','gw','nes','fds','gb','snes','virtualboy','satellaview','sufami','n64','gbc','gba','pokemini','gamecube','nds','wii','3do','sg1000','mastersystem','megadrive','gamegear','segacd','sega32x','saturn','dreamcast','x68000','zx81','zxspectrum','neogeo','neogeocd','ngp','ngpc','psx','psp','oricatmos','thomson','daphne','fba','fba_libretro','mame','dos','scummvm','prboom','ports','lutro','cavestory','moonlight','imageviewer','random','favorites']
hmc =['atari2600','atari5200','atari7800','jaguar','o2em','colecovision','channelf','vectrex','intellivision','pcengine','pcenginecd','supergrafx','pcfx','nes','fds','snes','satellaview','sufami','n64','gamecube','wii','3do','sg1000','mastersystem','megadrive','segacd','sega32x','saturn','dreamcast','neogeo','neogeocd','psx','lynx','wswan','wswanc','ngp','ngpc','gw','gb','virtualboy','gbc','gba','pokemini','nds','gamegear','psp','daphne','fba','fba_libretro','mame','amstradcpc','atari800','atarist','apple2','c64','amiga600','amiga1200','msx','msx1','msx2','samcoupe','pc98','x68000','zx81','zxspectrum','oricatmos','thomson','dos','scummvm','prboom','ports','lutro','cavestory','moonlight','imageviewer','random','favorites']
user =['satellaview','sufami','pokemini','pcfx','neogeocd','samcoupe','oricatmos','atari800','channelf','pc98','thomson','x68000','intellivision','atari5200','jaguar','nds','saturn','daphne','3do','apple2','atari2600','o2em','colecovision','c64','vectrex','gw','zx81','zxspectrum','nes','msx','msx1','sg1000','atari7800','amstradcpc','mastersystem','msx2','atarist','fds','pcengine','amiga600','megadrive','pcenginecd','supergrafx','gb','lynx','snes','gamegear','neogeo','segacd','sega32x','amiga1200','psx','virtualboy','n64','dreamcast','gbc','ngp','ngpc','wswan','wswanc','gba','gamecube','psp','wii','fba','fba_libretro','mame','dos','scummvm','prboom','ports','lutro','cavestory','moonlight','imageviewer','random','favorites']


def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

def writesystems(ll,f,sortlist):       
    root = etree.Element("systemList")    
    print("Generating from a %i ordered systems list" % len(sortlist))
    print("Nb of systems found in your share_init es_systems.cfg : %i" % len(ll))
    
    # everything expect last 3 (imageviewer, random, favorite)
    for i in sortlist[:-3]:
        for system in ll:
            name = get(system,"name")
            if( name == i):
                root.append(system)
    
    # check for custom user systems not in order list
    for system in ll:
        name = get(system,"name")
        found = False
        for i in sortlist:
            if( name == i) :
                found = True
        
        if not found :
            print("Not found in ordered list : %s , adding at the end" %name)
            root.append(system)
    
    # last 3 (imageviewer, random, favorites)
    for i in sortlist[-3:]:
        for system in ll:
            name = get(system,"name")
            if( name == i):
                root.append(system)
    
    print ("Generated a new list of %i systems" %len(root.getchildren()))
    
    tree = etree.ElementTree(root)
    tree.write(f, xml_declaration=True, encoding="utf-8")

def listsystems(p):    
    ll=[]
    for i in etree.parse(p).findall(".//system"):      
      ll.append(i)               
               
    return ll

def buildSortType(sortType):
    if sortType == None :
        sortType = raw_input("Please choose your system order : (A)lphabetical, (H)ardwareType, (C)hronological, (R)etrochronological, (M)anufacturer, Mi(x)ed or (U)ser : ").lower()
    
    if sortType in ['a','alphabetical'] :
        print ("Standard Sort")
        return alphabetical
    elif sortType in ['h','hardwaretype'] :
        print ("Hardware Type Sort")
        return hardwareType
    elif sortType in ['c','chronological'] :
        print ("Chronological Sort")
        return chronological
    elif sortType in ['r','retrochronological'] :
        print ("Retrochronological Sort")
        return retrochrono
    elif sortType in ['m','manufacturer'] :
        print ("Manufacturer Sort")
        return manufacturer
    elif sortType in ['x','mixed'] :
        print ("Mixed (H/M/C)")
        return hmc
    elif sortType in ['u','user'] :
        print ("User Custom Sort")
        return user
    else :
        return None

if __name__ == "__main__":
    print ("Diag test %i %i %i %i %i %i %i " %(len(alphabetical),len(hardwareType),len(chronological),len(retrochrono),len(manufacturer),len(hmc),len(user)))
    sortType = buildSortType(sys.argv[1].lower() if len(sys.argv) > 1 else None)
    print(sortType)
    if sortType != None :
        ll=listsystems(inDir)
        writesystems(ll,outDir,sortType)        
    else :
        print("No valid order selected")
        

#the lxml folder with _init_ ie /usr/lib/python2.7/dist-packages/lxml/
#np.. you may have to change the "from lxml import xy" line in your project  