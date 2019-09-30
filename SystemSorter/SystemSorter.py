#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys, collections

inDir = '/recalbox/share_init/system/.emulationstation/es_systems.cfg'
outDir = '/recalbox/share/system/.emulationstation/es_systems.cfg'

# new static sort data
System =  collections.namedtuple('System', 'name fullname manufacturer type releasedate')

def buildSystems() :
    systems = []
    systems.append(System('3do','3DO','Panasonic','1-console',1993))
    systems.append(System('amstradcpc','Amstrad CPC','Amstrad','4-computer',1984))
    systems.append(System('amiga600','Amiga 600','Commodore','4-computer',1991))
    systems.append(System('amiga1200','Amiga 1200','Commodore','4-computer',1992))
    systems.append(System('amigacd32','Amiga CD32','Commodore','1-console',1994))
    systems.append(System('apple2','Apple II','Apple','4-computer',1977))
    systems.append(System('apple2gs','Apple IIGS ','Apple','4-computer',1986))
    systems.append(System('atari2600','Atari 2600','Atari','1-console',1977))
    systems.append(System('atari5200','Atari 5200','Atari','1-console',1982))
    systems.append(System('atari7800','Atari 7800','Atari','1-console',1986))
    systems.append(System('atari800','Atari 800','Atari','4-computer',1979))
    systems.append(System('atarist','Atari ST','Atari','4-computer',1985))
    systems.append(System('atomiswave','Atomiswave','Sega','3-arcade',3680))
    systems.append(System('c64','Commodore 64','Commodore','4-computer',1982))
    systems.append(System('cavestory','Cave Story','Pixel','5-ports',3730))
    systems.append(System('channelf','Fairchild Channel F','Fairchild Semiconductor','1-console',1976))
    systems.append(System('colecovision','ColecoVision','Coleco','1-console',1982))
    systems.append(System('daphne','Daphne','Miscellaneous','3-arcade',3000))
    systems.append(System('dos','DOS','Microsoft','4-computer',3680))
    systems.append(System('dreamcast','Dreamcast','Sega','1-console',1998))
    systems.append(System('fba','Final Burn Alpha','Miscellaneous','3-arcade',3650))
    systems.append(System('fba_libretro','Final Burn Alpha Libretro','Miscellaneous','3-arcade',3660))
    systems.append(System('fds','Famicom Disk System','Nintendo','1-console',1986))
    systems.append(System('gb','Gameboy','Nintendo','2-portable',1989))
    systems.append(System('gba','Gameboy Advance','Nintendo','2-portable',2001))
    systems.append(System('gbc','Gameboy Color','Nintendo','2-portable',1998))
    systems.append(System('gamecube','Gamecube','Nintendo','1-console',2001))
    systems.append(System('gamegear','Game Gear','Sega','2-portable',1990))
    systems.append(System('gw','Game & Watch','Nintendo','2-portable',1980))
    systems.append(System('gx4000','GX4000','Amstrad','1-console',1991))
    systems.append(System('intellivision','Intellivision','Mattel','1-console',1979))
    systems.append(System('jaguar','Jaguar','Atari','1-console',1993))
    systems.append(System('lutro','Lutro','Miscellaneous','5-ports',3722))
    systems.append(System('lynx','Lynx','Atari','2-portable',1989))
    systems.append(System('mame','Mame','Miscellaneous','3-arcade',3670))
    systems.append(System('mastersystem','Master System','Sega','1-console',1985))
    systems.append(System('megadrive','Megadrive','Sega','1-console',1988))
    systems.append(System('moonlight','Moonlight','Miscellaneous','5-ports',3740))
    systems.append(System('msx','MSX','Microsoft','4-computer',1983))
    systems.append(System('msx1','MSX1','Microsoft','4-computer',1983))
    systems.append(System('msx2','MSX2','Microsoft','4-computer',1985))
    systems.append(System('msxturbor','MSX TurboR','Microsoft','4-computer',1990))
    systems.append(System('multivision','Othello Multivision','Tsukuda Original','1-console',1983))
    systems.append(System('naomi','Naomi','Sega','3-arcade',3690))
    systems.append(System('neogeo','Neo Geo','SNK','1-console',1990))
    systems.append(System('neogeocd','Neo Geo CD','SNK','1-console',1994))
    systems.append(System('ngp','Neo Geo Pocket','SNK','2-portable',1998))
    systems.append(System('ngpc','Neo Geo Pocket Color','SNK','2-portable',1999))
    systems.append(System('n64','Nintendo 64','Nintendo','1-console',1996))
    systems.append(System('nds','Nintendo DS','Nintendo','2-portable',2004))
    systems.append(System('nes','Nintendo Entertainment System','Nintendo','1-console',1983))
    systems.append(System('o2em','Odyssey 2 / Videopac','Magnavox / Philips','1-console',1978))
    systems.append(System('oricatmos','Oric Atmos','Tangerine Computer Systems','4-computer',1984))
    systems.append(System('palm','Palm','Palm','4-computer',1996))
    systems.append(System('pc88','PC88','NEC','4-computer',1981))
    systems.append(System('pc98','PC98','NEC','4-computer',1982))
    systems.append(System('pcengine','PC Engine','NEC','1-console',1987))
    systems.append(System('pcenginecd','PC Engine CD','NEC','1-console',1988))
    systems.append(System('pcfx','PC-FX','NEC','1-console',1994))
    systems.append(System('pokemini','Pokemini','Nintendo','2-portable',2001))
    systems.append(System('ports','Ports','Miscellaneous','5-ports',3700))
    systems.append(System('prboom','PrDoom','Miscellaneous','5-ports',3710))
    systems.append(System('psx','Playstation','Sony','1-console',1994))
    systems.append(System('psp','PSP','Sony','2-portable',2004))
    systems.append(System('samcoupe','Sam Coupe','Miles Gordon Technology','4-computer',1989))
    systems.append(System('satellaview','Satellaview','Nintendo','1-console',1995))
    systems.append(System('saturn','Saturn','Sega','1-console',1994))
    systems.append(System('scummvm','ScummVM','Miscellaneous','4-computer',3690))
    systems.append(System('sega32x','Sega 32x','Sega','1-console',1994))
    systems.append(System('segacd','Mega-CD','Sega','1-console',1991))
    systems.append(System('sg1000','SG-1000','Sega','1-console',1983))
    systems.append(System('spectravideo','SV-318','SpectraVision','4-computer',1983))
    systems.append(System('sufami','Sufami turbo','Bandai','1-console',1996))
    systems.append(System('supergrafx','SuperGrafx ','NEC','1-console',1989))
    systems.append(System('snes','Super Nintendo','Nintendo','1-console',1990))
    systems.append(System('thomson','MO5','Thomson','4-computer',1984))
    systems.append(System('tic80','TIC80','Nesbox','4-computer',2017))
    systems.append(System('uzebox','Uzebox','Atmel','1-console',2008))
    systems.append(System('vectrex','Vectrex','MB','1-console',1982))
    systems.append(System('virtualboy','Virtual Boy','Nintendo','2-portable',1995))
    systems.append(System('wii','Wii','Nintendo','1-console',2006))
    systems.append(System('wswan','WonderSwan ','Bandai','2-portable',1999))
    systems.append(System('wswanc','WonderSwan Color','Bandai','2-portable',2000))
    systems.append(System('x1','X1','Sharp','4-computer',1982))
    systems.append(System('x68000','X68000','Sharp','4-computer',1987))
    systems.append(System('zx81','ZX81','Sinclair','4-computer',1981))
    systems.append(System('zxspectrum','ZX Spectrum','Sinclair','4-computer',1982))
    systems.append(System('imageviewer','Image Viewer','Miscellaneous','6-system',4000))
    systems.append(System('random','Random','Miscellaneous','6-system',4100))
    systems.append(System('favorites','Favorites','Miscellaneous','6-system',4200))
    return systems

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
            print("Not found in ordered list : %s , appending at the end" %name)
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
        sortType = raw_input("Please choose your system order : (A)lphabetical, (H)ardwareType, (C)hronological, (R)etrochronological, (M)anufacturer, or Mi(x)ed : ").lower()
    
    systems = buildSystems()   
    if sortType in ['a','alphabetical'] :
        print ("Alphabetical Sort")
        head = headByType(systems,'6-system')
        head.sort(key=lambda s: (s.fullname))
        systems = head + fixedTailByType(systems,'6-system')
        return systems
    elif sortType in ['h','hardwaretype'] :
        print ("Hardware Type Sort")
        systems.sort(key=lambda s: (s.type,s.releasedate))
        return systems
    elif sortType in ['c','chronological'] :
        print ("Chronological Sort")
        systems.sort(key=lambda s: (s.releasedate))
        return systems
    elif sortType in ['r','retrochronological'] :
        print ("Retrochronological Sort")        
        head = headByYear(systems,3000)
        head.sort(key=lambda s: (-s.releasedate))
        systems = head + fixedTailByYear(systems,3000)
        return systems
    elif sortType in ['m','manufacturer'] :
        print ("Manufacturer Sort")        
        head = headByType(systems,'6-system')
        head.sort(key=lambda s: (s.manufacturer, s.releasedate))
        systems = head + fixedTailByType(systems,'6-system')
        return systems
    elif sortType in ['x','mixed'] :
        print ("Mixed (H/M/C)")        
        head = headByType(systems,'6-system')
        head.sort(key=lambda s: (s.type,s.manufacturer, s.releasedate))
        systems = head + fixedTailByType(systems,'6-system')
        return systems    
    else :
        return None

# Systems which must go at the end
def fixedTailByType(systems, limit) :
    tail = list(filter(lambda f: f.type >= limit, systems))
    tail.sort(key=lambda s: (s.type,s.releasedate))
    return tail

#Systems to be sorted in most case
def headByType(systems, limit) :
    return list(filter(lambda f: f.type < limit, systems))

# Systems which must go at the end
def fixedTailByYear(systems, limit) :
    tail = list(filter(lambda f: f.releasedate >= limit, systems))
    tail.sort(key=lambda s: (s.type,s.releasedate))
    return tail

#Systems to be sorted in most case
def headByYear(systems, limit) :
    return list(filter(lambda f: f.releasedate < limit, systems))


if __name__ == "__main__":
    sortType = buildSortType(sys.argv[1].lower() if len(sys.argv) > 1 else None)
    sortedSys = [s.name for s in sortType]
    print("New sort :")
    print(sortedSys)
    if sortType is not None :
        ll=listsystems(inDir)
        writesystems(ll,outDir,sortedSys)        
    else :
        print("No valid order selected")
 