#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import sys, collections
import os.path
import shutil
import subprocess

def cleanString(string) :
    return string.rstrip('\n\r ').lstrip()

def loadConf(confFile) :
    conf = dict()
    
    file = open(confFile,'r')
    for line in file.readlines() :
        if not line.startswith('#') :
            confLine = line.split("=")
            if len(confLine) == 2 :
                conf[cleanString(confLine[0])] = cleanString(confLine[1])
    
    file.close()        
    return conf

