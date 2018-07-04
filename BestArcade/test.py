# -*- coding: utf-8 -*-
import collections
import os

Test = collections.namedtuple('Test', 'status genre name rom year manufacturer hardware comments notes') 

def cleanString(string) :
    return string.rstrip('\n\r ').lstrip()
    
def loadTest(testFile,key,allTests) :
    tests = dict()    
    file = open(testFile,'r', encoding="utf-8")
    
    countLine = 0;
    
    for line in file.readlines()[1:] :
        countLine = countLine +1;
        testLine = line.split(";")
        #print(testLine)
        rom = cleanString(testLine[3])        
        status = int(cleanString(testLine[0])) if cleanString(testLine[0]) != '' else -1
        #print(rom,status)
        test = Test(status,cleanString(testLine[1]),cleanString(testLine[2]),
                    rom,cleanString(testLine[4]),cleanString(testLine[5]),
                    cleanString(testLine[6]),cleanString(testLine[7]),cleanString(testLine[8]))
        if rom not in allTests :
            allTests[rom] = dict()
        allTests[rom][key] = test
        tests[rom] = test
    
#    print("debug loadTest %s lines %i -> dict %i" %(key,countLine,len(tests)))
        
    file.close()
    return tests

def loadTests(fbaKey,mame2003Key,mame2010Key,sourceDir,usingSystems) :
    allTests = dict()
    if fbaKey in usingSystems :
        fbaTests = loadTest(os.path.join(sourceDir,fbaKey+'.csv'), fbaKey, allTests)
        print("    Found %i fba tests" %len(fbaTests))
    if mame2003Key in usingSystems :
        mame2003Tests = loadTest(os.path.join(sourceDir,mame2003Key+'.csv'), mame2003Key, allTests)
        print("    Found %i mame2003 tests" %len(mame2003Tests))
    if mame2010Key in usingSystems :
        mame2010Tests = loadTest(os.path.join(sourceDir,mame2010Key+'.csv'), mame2010Key, allTests)
        print("    Found %i mame2010 tests" %len(mame2010Tests))
    print("    Found %i cumulated tests" %len(allTests))
    return allTests