#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import sys
import os.path
import conf, fav, test, dat
from gui import GUI
from logger import Logger

scriptDir = r""

outputDir = r"output"
confFile = r"conf.conf"
scriptDir=r""

favorites = dict()
configuration = dict()
usingSystems = []
    
#def checkErrors(inputTests,keepLevel) :        
#    print("Input Tests")
#    test.loadTests(Sorter.setKeys,os.path.join(scriptDir,dataDir),usingSystems)
#    print("Output Tests")
#    outputTests = test.loadTests(Sorter.setKeys,os.path.join(configuration['exportDir']),usingSystems)
#    print("Possible errors")
#    for rom in inputTests.keys() :
#        
#        # new names : bbakraid,snowbro3,fantzn2x,dynwar,rbisland,sf,moomesa,leds2011,batrider,sbomber
#        #changedName = ['bkraidu','snowbros3','fantzn2','dw','rainbow','sf1','moo','ledstorm2','batrid','sbomberb']
#        
#        romNotInFav = True;
#        for genre in favorites :
#            for name in favorites[genre] :
#                if name == rom :
#                    romNotInFav = False
#        
#        if romNotInFav :                    
#            print("    Orphan rom %s not in favs" %rom)            
#        
#        # at least higher than keepLevel in one set
#        higherThanKeepLevel = True
#        for key in inputTests[rom] :
#            higherThanKeepLevel = higherThanKeepLevel and inputTests[rom][key].status >= int(keepLevel)
#        
#        if higherThanKeepLevel :
#            if rom not in outputTests :
#                if not rom.startswith('mp_') and not rom.startswith('nss_') :
#                    print("    ERROR %s not found in ouput csvs, but in input " %rom, inputTests[rom].keys())
#            else :
#                for key in inputTests[rom] :
#                    if key not in outputTests[rom] :
#                        print("    ERROR %s should be exported for %s" %(rom,key))
    
if __name__ == "__main__":    
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    logger = Logger()    
    logger.log('Script path : '+scriptDir)
    # load conf.conf
    configuration = conf.loadConf(os.path.join(scriptDir,confFile))    
    gui = GUI(configuration,scriptDir,logger)
    logger.log('\n<--------- Load Configuration File --------->')
    logger.printDict(configuration)
    gui.draw()

# TODOS
# missing doctype on generated dat  ?
# if name from dat is empty, take one from test file
