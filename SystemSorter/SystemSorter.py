#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys

inDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
outDir = '/recalbox/share/system/.emulationstation/es_systems.cfg'

# Sort orders
standard = ['snes','nes','n64','gba','gbc','gb','fds','virtualboy','gw','megadrive','segacd','sega32x','mastersystem','gamegear','sg1000','psx','pcengine','pcenginecd','supergrafx','scummvm','fba','fba_libretro','mame','neogeo','atari2600','atari7800','lynx','ngp','ngpc','wswan','wswanc','prboom','vectrex','lutro','cavestory','atarist','amstradcpc','amiga600','amiga1200','msx','msx1','msx2','odyssey2','zx81','zxspectrum','moonlight','imageviewer','apple2','colecovision','c64','pc','dreamcast','gc','psp','wii','random','favorites']
hardwareType = ['atari2600','odyssey2','colecovision','vectrex','nes','sg1000','atari7800','mastersystem','fds','pcengine','megadrive','pcenginecd','supergrafx','snes','segacd','sega32x','psx','n64','dreamcast','gc','wii','gw','gb','lynx','gamegear','virtualboy','gbc','ngp','ngpc','wswan','wswanc','gba','psp','neogeo','fba','fba_libretro','mame','apple2','c64','zx81','zxspectrum','msx','msx1','amstradcpc','msx2','atarist','amiga600','amiga1200','pc','scummvm','prboom','lutro','cavestory','moonlight','imageviewer','random','favorites']
chronological=['apple2','atari2600','odyssey2','colecovision','c64','vectrex','gw','zx81','zxspectrum','nes','msx','msx1','sg1000','atari7800','amstradcpc','mastersystem','msx2','atarist','fds','pcengine','amiga600','megadrive','pcenginecd','supergrafx','gb','lynx','snes','gamegear','neogeo','segacd','sega32x','amiga1200','psx','virtualboy','n64','dreamcast','gbc','ngp','ngpc','wswan','wswanc','gba','gc','psp','wii','fba','fba_libretro','mame','pc','scummvm','prboom','lutro','cavestory','moonlight','imageviewer','random','favorites']
retrochrono = chronological[::-1][12::] + chronological[-12::]
manufacturer=['amstradcpc','apple2','atari2600','atari7800','atarist','lynx','wswan','wswanc','c64','amiga600','amiga1200','odyssey2','colecovision','vectrex','msx','msx1','msx2','pcengine','pcenginecd','supergrafx','neogeo','ngp','ngpc','gw','nes','fds','gb','snes','virtualboy','n64','gbc','gba','gc','wii','sg1000','mastersystem','megadrive','gamegear','segacd','sega32x','dreamcast','zx81','zxspectrum','psx','psp','fba','fba_libretro','mame','pc','scummvm','prboom','lutro','cavestory','moonlight','imageviewer','random','favorites']
hmc=['atari2600','atari7800','odyssey2','colecovision','vectrex','pcengine','pcenginecd','supergrafx','nes','fds','snes','n64','gc','wii','sg1000','mastersystem','megadrive','segacd','sega32x','dreamcast','psx','lynx','wswan','wswanc','ngp','ngpc','gw','gb','virtualboy','gbc','gba','gamegear','psp','neogeo','fba','fba_libretro','mame','amstradcpc','atarist','apple2','c64','amiga600','amiga1200','msx','msx1','msx2','zx81','zxspectrum','pc','scummvm','prboom','lutro','cavestory','moonlight','imageviewer','random','favorites']
user=['apple2','atari2600','odyssey2','colecovision','c64','vectrex','gw','zx81','zxspectrum','nes','msx','msx1','sg1000','atari7800','amstradcpc','mastersystem','msx2','atarist','fds','pcengine','amiga600','megadrive','pcenginecd','supergrafx','gb','lynx','snes','gamegear','neogeo','segacd','sega32x','amiga1200','psx','virtualboy','n64','dreamcast','gbc','ngp','ngpc','wswan','wswanc','gba','gc','psp','wii','fba','fba_libretro','mame','pc','scummvm','prboom','lutro','cavestory','moonlight','imageviewer','random','favorites']

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

def writesystems(ll,f,sortlist):       
    root = etree.Element("systemList")    
    print("Generating from a %i systems list" % len(sortlist))
    for i in sortlist:
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
        sortType = raw_input("Please choose your system order : (S)tandard, (H)ardwareType, (C)hronological, (R)etrochronological, (M)anufacturer, Mi(x)ed or (U)ser : ").lower()
    
    if sortType in ['s','standard'] :
        print ("Standard Sort")
        return standard
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
    sortType = buildSortType(sys.argv[1].lower() if len(sys.argv) > 1 else None)
    print(sortType)
    if sortType != None :
        ll=listsystems(inDir)
        writesystems(ll,outDir,sortType)        
    else :
        print("No valid order selected")
        

#the lxml folder with _init_ ie /usr/lib/python2.7/dist-packages/lxml/
#np.. you may have to change the "from lxml import xy" line in your project  