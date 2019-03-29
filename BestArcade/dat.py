# -*- coding: utf-8 -*-
import collections, os
import xml.etree.ElementTree as etree

Dat = collections.namedtuple('Dat', 'name description manufacturer year cloneof isbios node')

def get(i,e):
    ll=i.find(e)        
    return ll.text if ll != None else None

def parseDat(file):
    dats = dict()
    parser = etree.XMLParser(encoding="utf-8")    
    games = etree.parse(file, parser=parser).findall(".//game")        
    if (len(games) > 0) : # remove systems with no games 
        for g in games:            
            isbios = True if 'isbios' in g.attrib and g.attrib['isbios'] == 'yes' else False
            cloneof = g.attrib['cloneof'] if 'cloneof' in g.attrib else None            
            datEntry = Dat(g.attrib['name'],get(g,'description'),get(g,'manufacturer'),get(g,'year'),
                           cloneof,isbios,g)
            dats[g.attrib['name']] = datEntry
    
    print('Dat %s : %i entries' %(file,len(dats)))
    return dats

def parseDats(scriptDir,dataDir,setDats,usingSystems) :
    dats = dict()    
    for setKey in usingSystems :        
        header = etree.parse(os.path.join(scriptDir,dataDir,setDats[setKey]),etree.XMLParser(encoding="utf-8")).findall(".//header")
        dats[setKey] = parseDat(os.path.join(scriptDir,dataDir,setDats[setKey]))
        dats[setKey+"Header"] = header[0]        
    return dats
  