#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-

from Tkinter import *
import conf,ttk, collections
from operator import attrgetter

GUIString = collections.namedtuple('GUIString', 'id label help order')

class GUI():

    fbaKey = "fba_libretro"
    mame2010Key = "mame2010"
    mame2003Key = "mame2003"
    setKeys = [fbaKey,mame2003Key,mame2010Key]

    def __init__(self,configuration) :
        self.configuration = configuration
        self.window = Tk()
        self.window.resizable(False,False)
        self.window.title('BestArcade')
        self.guiVars = dict()
        self.loadStrings()

    def loadStrings(self) :
        self.guiStrings = dict()
        file = open(r"/home/thomas/code/perso/scripts4recalbox/BestArcade/GUI/gui-en.csv",'r')
        order = 0
        for line in file.readlines()[1:] :
            confLine = line.split(";")
            if len(confLine) == 3 :
                self.guiStrings[confLine[0]]=GUIString(confLine[0],confLine[1],confLine[2].rstrip('\n\r '), order)
                order = order + 1
        file.close()
        print(len(self.guiStrings))
        print(self.guiStrings['usePreferedSetForGenre'])

    def draw(self) :
        self.root = Frame(self.window,padx=15,pady=15,width=800,height=200)
        self.root.grid(column=0,row=0)
        self.drawRomsetFrame()
        self.drawImagesFrame()
        self.drawParametersFrame()
        self.drawButtonsFrame()
        self.drawConsole()
        self.window.mainloop()

    def drawRomsetFrame(self) :
        # Romsets frame
        self.romsetFrame = LabelFrame(self.root,text="Your Romsets",padx=15,pady=15)
        self.romsetFrame.grid(column=0,row=0,sticky="EW",pady=5)
        setRow = 0
        for key in self.setKeys :
            label = Label(self.romsetFrame, text=self.guiStrings[key].label)
            label.grid(column=0, row=setRow, padx=5,sticky="W")
            self.guiVars[key] = StringVar()
            self.guiVars[key].set(configuration[key])
            entry = Entry(self.romsetFrame, width=80, textvariable=self.guiVars[key])
            entry.grid(column=1, row=setRow, padx=5,sticky="E")
            setRow = setRow + 1

        ttk.Separator(self.romsetFrame, orient=HORIZONTAL).grid(column=0, row=setRow,columnspan=2, padx=5,pady=10,sticky="EW")
        setRow = setRow + 1
        outputDirLabel = Label(self.romsetFrame, text=self.guiStrings['exportDir'].label)
        outputDirLabel.grid(column=0, row=setRow, padx=5,sticky=(W))
        self.guiVars['exportDir'] = StringVar()
        self.guiVars['exportDir'].set(configuration['exportDir'])
        outputEntry = Entry(self.romsetFrame, width=80, textvariable=self.guiVars['exportDir'])
        outputEntry.grid(column=1, row=setRow, columnspan=5,padx=5,sticky="E")

    def drawImagesFrame(self) :
        #Images frame
        self.imagesFrame = LabelFrame(self.root,text="Images",padx=15,pady=15)
        self.imagesFrame.grid(column=0,row=1,sticky="EW",pady=5)
        setRow = 0
        for path in self.configuration['images'].split(';') :
            pathLabel = self.guiStrings['images'].label+' #'+ str(setRow+1)
            label = Label(self.imagesFrame, text=pathLabel)
            label.grid(column=0, row=setRow, padx=5,sticky="W")
            self.guiVars[pathLabel] = StringVar()
            self.guiVars[pathLabel].set(path.strip())
            entry = Entry(self.imagesFrame, width=80, textvariable=self.guiVars[pathLabel])
            entry.grid(column=1, row=setRow, padx=5,sticky="E")
            setRow = setRow + 1

        ttk.Separator(self.imagesFrame, orient=HORIZONTAL).grid(column=0, row=setRow,columnspan=2, padx=5,pady=10,sticky="EW")
        setRow = setRow + 1
        imgFormatLabel = Label(self.imagesFrame, text=self.guiStrings['imgNameFormat'].label)
        imgFormatLabel.grid(column=0, row=setRow, padx=5,sticky=(W))
        self.guiVars['imgNameFormat'] = StringVar()
        self.guiVars['imgNameFormat'].set(configuration['imgNameFormat'])
        # place entry in dict to retrieve later
        imgFormatEntry = Entry(self.imagesFrame, width=80, textvariable=self.guiVars['imgNameFormat'])
        imgFormatEntry.grid(column=1, row=setRow, columnspan=5,padx=5,sticky="E")

    def drawParametersFrame(self) :
        #Parameters frame
        self.parametersFrame = LabelFrame(self.root,text="Sorting Parameters",padx=15,pady=15)
        self.parametersFrame.grid(column=0,row=2,sticky="EW",pady=5)
        self.guiVars['dryRun'] = IntVar()
        self.guiVars['dryRun'].set(self.configuration['dryRun'])
        dryRunCheckButton = Checkbutton(self.parametersFrame,text=self.guiStrings['dryRun'].label, variable=self.guiVars['dryRun'], onvalue=1, offvalue = 0)
        dryRunCheckButton.grid(column=0,row=0,sticky="W")
        self.guiVars['genreSubFolders'] = IntVar()
        self.guiVars['genreSubFolders'].set(self.configuration['genreSubFolders'])
        useGenreSubFolderCheckButton = Checkbutton(self.parametersFrame,text=self.guiStrings['genreSubFolders'].label, variable=self.guiVars['genreSubFolders'], onvalue=1, offvalue = 0)
        useGenreSubFolderCheckButton.grid(column=3,row=0,sticky="W")
        self.guiVars['useImages'] = IntVar()
        self.guiVars['useImages'].set(self.configuration['useImages'])
        useImagesCheckButton = Checkbutton(self.parametersFrame,text=self.guiStrings['useImages'].label, variable=self.guiVars['useImages'], onvalue=1, offvalue = 0)
        useImagesCheckButton.grid(column=4,row=0,sticky="W")
        ttk.Separator(self.parametersFrame, orient=HORIZONTAL).grid(column=0, row=1,columnspan=4, padx=5,pady=10,sticky="EW")
        keepLevelLabel = Label(self.parametersFrame, text=self.guiStrings['keepLevel'].label)
        keepLevelLabel.grid(column=0, row=2,sticky="W")
        self.guiVars['keepLevel'] = StringVar()
        self.guiVars['keepLevel'].set('BADLY WORKING')
        keepLevelComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['keepLevel'])
        keepLevelComboBox.grid(column=1,row=2, sticky="W",pady=5,padx=5)
        keepLevelComboBox['values'] = ('WORKING','MOSTLY WORKING','BADLY WORKING','NON WORKING')
        self.guiVars['keepNotTested'] = IntVar()
        self.guiVars['keepNotTested'].set(self.configuration['keepNotTested'])
        keepNotTestedCheckButton = Checkbutton(self.parametersFrame,text=self.guiStrings['keepNotTested'].label, variable=self.guiVars['keepNotTested'], onvalue=1, offvalue = 0)
        keepNotTestedCheckButton.grid(column=3,row=2,sticky="W")
        ttk.Separator(self.parametersFrame, orient=HORIZONTAL).grid(column=0, row=3,columnspan=4, padx=5,pady=10,sticky="EW")
        exclusionTypeLabel = Label(self.parametersFrame, text=self.guiStrings['exclusionType'].label)
        exclusionTypeLabel.grid(column=0, row=4,sticky="W")
        self.guiVars['exclusionType'] = StringVar()
        self.guiVars['exclusionType'].set(self.configuration['exclusionType'])
        exclusionTypeComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['exclusionType'])
        exclusionTypeComboBox.grid(column=1,row=4, sticky="W",pady=5,padx=5)
        exclusionTypeComboBox['values'] = ('STRICT','EQUAL','NONE')
        exclusionTypeComboBox.bind('<<ComboboxSelected>>',self.changeExclusionType)
        self.preferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['preferedSet'].label)
        self.preferedSetLabel.grid(column=0, row=5,sticky="W",pady=5)
        self.guiVars['preferedSet'] = StringVar()
        self.guiVars['preferedSet'].set(self.configuration['preferedSet'])
        self.preferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['preferedSet'])
        self.preferedSetComboBox.grid(column=1,row=5, sticky="W",pady=5,padx=5)
        self.preferedSetComboBox['values'] = self.setKeys
        self.guiVars['usePreferedSetForGenre'] = IntVar()
        self.guiVars['usePreferedSetForGenre'].set(self.configuration['usePreferedSetForGenre'])
        self.usePreferedSetForGenreCheckButton = Checkbutton(self.parametersFrame,text=self.guiStrings['usePreferedSetForGenre'].label, variable=self.guiVars['usePreferedSetForGenre'], onvalue=1, offvalue = 0, command=self.changeUsePreferedSetForGenre)
        self.usePreferedSetForGenreCheckButton.grid(column=3,row=5,sticky="E")
        #usePreferedSetForGenre comboboxes
        self.beatEmUpPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['BeatEmUpPreferedSet'].label)
        self.beatEmUpPreferedSetLabel.grid(column=0, row=6,sticky="W",pady=5)
        self.guiVars['BeatEmUpPreferedSet'] = StringVar()
        self.guiVars['BeatEmUpPreferedSet'].set(self.configuration['BeatEmUpPreferedSet'])
        self.beatEmUpPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['BeatEmUpPreferedSet'])
        self.beatEmUpPreferedSetComboBox.grid(column=1,row=6, sticky="W",pady=5,padx=5)
        self.beatEmUpPreferedSetComboBox['values'] = self.setKeys
        self.gunPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['GunPreferedSet'].label)
        self.gunPreferedSetLabel.grid(column=2, row=6,sticky="W",pady=5)
        self.guiVars['GunPreferedSet'] = StringVar()
        self.guiVars['GunPreferedSet'].set(self.configuration['GunPreferedSet'])
        self.gunPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['GunPreferedSet'])
        self.gunPreferedSetComboBox.grid(column=3,row=6, sticky="W",pady=5,padx=5)
        self.gunPreferedSetComboBox['values'] = self.setKeys
        self.miscPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['MiscPreferedSet'].label)
        self.miscPreferedSetLabel.grid(column=4, row=6,sticky="W",pady=5)
        self.guiVars['MiscPreferedSet'] = StringVar()
        self.guiVars['MiscPreferedSet'].set(self.configuration['MiscPreferedSet'])
        self.miscPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['MiscPreferedSet'])
        self.miscPreferedSetComboBox.grid(column=5,row=6, sticky="W",pady=5,padx=5)
        self.miscPreferedSetComboBox['values'] = self.setKeys
        self.platformPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['PlatformPreferedSet'].label)
        self.platformPreferedSetLabel.grid(column=0, row=7,sticky="W",pady=5)
        self.guiVars['PlatformPreferedSet'] = StringVar()
        self.guiVars['PlatformPreferedSet'].set(self.configuration['PlatformPreferedSet'])
        self.platformPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['PlatformPreferedSet'])
        self.platformPreferedSetComboBox.grid(column=1,row=7, sticky="W",pady=5,padx=5)
        self.platformPreferedSetComboBox['values'] = self.setKeys
        self.puzzlePreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['PuzzlePreferedSet'].label)
        self.puzzlePreferedSetLabel.grid(column=2, row=7,sticky="W",pady=5)
        self.guiVars['PuzzlePreferedSet'] = StringVar()
        self.guiVars['PuzzlePreferedSet'].set(self.configuration['PuzzlePreferedSet'])
        self.puzzlePreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['PuzzlePreferedSet'])
        self.puzzlePreferedSetComboBox.grid(column=3,row=7, sticky="W",pady=5,padx=5)
        self.puzzlePreferedSetComboBox['values'] = self.setKeys
        self.racePreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['RacePreferedSet'].label)
        self.racePreferedSetLabel.grid(column=4, row=7,sticky="W",pady=5)
        self.guiVars['RacePreferedSet'] = StringVar()
        self.guiVars['RacePreferedSet'].set(self.configuration['RacePreferedSet'])
        self.racePreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['RacePreferedSet'])
        self.racePreferedSetComboBox.grid(column=5,row=7, sticky="W",pady=5,padx=5)
        self.racePreferedSetComboBox['values'] = self.setKeys
        self.runNGunPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['RunNGunPreferedSet'].label)
        self.runNGunPreferedSetLabel.grid(column=0, row=8,sticky="W",pady=5)
        self.guiVars['RunNGunPreferedSet'] = StringVar()
        self.guiVars['RunNGunPreferedSet'].set(self.configuration['RunNGunPreferedSet'])
        self.runNGunPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['RunNGunPreferedSet'])
        self.runNGunPreferedSetComboBox.grid(column=1,row=8, sticky="W",pady=5,padx=5)
        self.runNGunPreferedSetComboBox['values'] = self.setKeys
        self.shootEmUpPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['ShootEmUpPreferedSet'].label)
        self.shootEmUpPreferedSetLabel.grid(column=2, row=8,sticky="W",pady=5)
        self.guiVars['ShootEmUpPreferedSet'] = StringVar()
        self.guiVars['ShootEmUpPreferedSet'].set(self.configuration['ShootEmUpPreferedSet'])
        self.shootEmUpPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['ShootEmUpPreferedSet'])
        self.shootEmUpPreferedSetComboBox.grid(column=3,row=8, sticky="W",pady=5,padx=5)
        self.shootEmUpPreferedSetComboBox['values'] = self.setKeys
        self.sportPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['SportPreferedSet'].label)
        self.sportPreferedSetLabel.grid(column=4, row=8,sticky="W",pady=5)
        self.guiVars['SportPreferedSet'] = StringVar()
        self.guiVars['SportPreferedSet'].set(self.configuration['SportPreferedSet'])
        self.sportPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['SportPreferedSet'])
        self.sportPreferedSetComboBox.grid(column=5,row=8, sticky="W",pady=5,padx=5)
        self.sportPreferedSetComboBox['values'] = self.setKeys
        self.vsFightingPreferedSetLabel = Label(self.parametersFrame, text=self.guiStrings['VsFightingPreferedSet'].label)
        self.vsFightingPreferedSetLabel.grid(column=0, row=9,sticky="W",pady=5)
        self.guiVars['VsFightingPreferedSet'] = StringVar()
        self.guiVars['VsFightingPreferedSet'].set(self.configuration['VsFightingPreferedSet'])
        self.vsFightingPreferedSetComboBox = ttk.Combobox(self.parametersFrame, textvariable=self.guiVars['VsFightingPreferedSet'])
        self.vsFightingPreferedSetComboBox.grid(column=1,row=9, sticky="W",pady=5,padx=5)
        self.vsFightingPreferedSetComboBox['values'] = self.setKeys
        self.showHide()

    def changeExclusionType(self,event) :
        self.showHide()

    def changeUsePreferedSetForGenre(self) :
        self.showHide()

    def showHide(self) :
        if self.guiVars['exclusionType'].get() == 'STRICT' :
            self.preferedSetLabel['state'] = 'normal'
            self.preferedSetComboBox['state'] = 'normal'
            self.usePreferedSetForGenreCheckButton['state'] = 'normal'
            if self.guiVars['usePreferedSetForGenre'].get() == 1 :
                self.beatEmUpPreferedSetLabel['state'] = 'normal'
                self.beatEmUpPreferedSetComboBox['state'] = 'normal'
                self.gunPreferedSetLabel['state'] = 'normal'
                self.gunPreferedSetComboBox['state'] = 'normal'
                self.miscPreferedSetLabel['state'] = 'normal'
                self.miscPreferedSetComboBox['state'] = 'normal'
                self.platformPreferedSetLabel['state'] = 'normal'
                self.miscPreferedSetComboBox['state'] = 'normal'
                self.platformPreferedSetLabel['state'] = 'normal'
                self.platformPreferedSetComboBox['state'] = 'normal'
                self.puzzlePreferedSetLabel['state'] = 'normal'
                self.puzzlePreferedSetComboBox['state'] = 'normal'
                self.racePreferedSetLabel['state'] = 'normal'
                self.racePreferedSetComboBox['state'] = 'normal'
                self.runNGunPreferedSetLabel['state'] = 'normal'
                self.runNGunPreferedSetComboBox['state'] = 'normal'
                self.shootEmUpPreferedSetLabel['state'] = 'normal'
                self.shootEmUpPreferedSetComboBox['state'] = 'normal'
                self.sportPreferedSetLabel['state'] = 'normal'
                self.sportPreferedSetComboBox['state'] = 'normal'
                self.vsFightingPreferedSetLabel['state'] = 'normal'
                self.vsFightingPreferedSetComboBox['state'] = 'normal'
            else :
                self.beatEmUpPreferedSetLabel['state'] = 'disabled'
                self.beatEmUpPreferedSetComboBox['state'] = 'disabled'
                self.gunPreferedSetLabel['state'] = 'disabled'
                self.gunPreferedSetComboBox['state'] = 'disabled'
                self.miscPreferedSetLabel['state'] = 'disabled'
                self.miscPreferedSetComboBox['state'] = 'disabled'
                self.platformPreferedSetLabel['state'] = 'disabled'
                self.miscPreferedSetComboBox['state'] = 'disabled'
                self.platformPreferedSetLabel['state'] = 'disabled'
                self.platformPreferedSetComboBox['state'] = 'disabled'
                self.puzzlePreferedSetLabel['state'] = 'disabled'
                self.puzzlePreferedSetComboBox['state'] = 'disabled'
                self.racePreferedSetLabel['state'] = 'disabled'
                self.racePreferedSetComboBox['state'] = 'disabled'
                self.runNGunPreferedSetLabel['state'] = 'disabled'
                self.runNGunPreferedSetComboBox['state'] = 'disabled'
                self.shootEmUpPreferedSetLabel['state'] = 'disabled'
                self.shootEmUpPreferedSetComboBox['state'] = 'disabled'
                self.sportPreferedSetLabel['state'] = 'disabled'
                self.sportPreferedSetComboBox['state'] = 'disabled'
                self.vsFightingPreferedSetLabel['state'] = 'disabled'
                self.vsFightingPreferedSetComboBox['state'] = 'disabled'
        else :
            self.preferedSetLabel['state'] = 'disabled'
            self.preferedSetComboBox['state'] = 'disabled'
            self.usePreferedSetForGenreCheckButton['state'] = 'disabled'
            self.beatEmUpPreferedSetLabel['state'] = 'disabled'
            self.beatEmUpPreferedSetComboBox['state'] = 'disabled'
            self.gunPreferedSetLabel['state'] = 'disabled'
            self.gunPreferedSetComboBox['state'] = 'disabled'
            self.miscPreferedSetLabel['state'] = 'disabled'
            self.miscPreferedSetComboBox['state'] = 'disabled'
            self.platformPreferedSetLabel['state'] = 'disabled'
            self.miscPreferedSetComboBox['state'] = 'disabled'
            self.platformPreferedSetLabel['state'] = 'disabled'
            self.platformPreferedSetComboBox['state'] = 'disabled'
            self.puzzlePreferedSetLabel['state'] = 'disabled'
            self.puzzlePreferedSetComboBox['state'] = 'disabled'
            self.racePreferedSetLabel['state'] = 'disabled'
            self.racePreferedSetComboBox['state'] = 'disabled'
            self.runNGunPreferedSetLabel['state'] = 'disabled'
            self.runNGunPreferedSetComboBox['state'] = 'disabled'
            self.shootEmUpPreferedSetLabel['state'] = 'disabled'
            self.shootEmUpPreferedSetComboBox['state'] = 'disabled'
            self.sportPreferedSetLabel['state'] = 'disabled'
            self.sportPreferedSetComboBox['state'] = 'disabled'
            self.vsFightingPreferedSetLabel['state'] = 'disabled'
            self.vsFightingPreferedSetComboBox['state'] = 'disabled'

    def drawButtonsFrame(self) :
        self.buttonsFrame = Frame(self.root,padx=15)
        self.buttonsFrame.grid(column=0,row=3,sticky="EW",pady=10)
        emptyFrame = Frame(self.buttonsFrame,width=750,padx=15)
        emptyFrame.grid(column=0,row=0,columnspan=3,sticky="EW",pady=10)
        verifyButton = Button(self.buttonsFrame,text=self.guiStrings['verify'].label, command=self.clickVerify)
        verifyButton.grid(column=3,row=0,sticky="E")
        saveButton = Button(self.buttonsFrame,text=self.guiStrings['save'].label, command=self.clickSave)
        saveButton.grid(column=4,row=0,sticky="E")
        saveButton = Button(self.buttonsFrame,text=self.guiStrings['proceed'].label, command=self.clickProceed)
        saveButton.grid(column=5,row=0,sticky="E")

    def clickSave(self) :
        print ('Save!')
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys :
            print(str(key.order) + "\t"+ key.id + "\t" + key.help)

    def clickVerify(self) :
        print ('Verify!')

    def clickProceed(self) :
        print ('Proceed!')
        print(self.guiStrings['confirm'].label)
        print(self.guiVars['exportDir'].get())
        message=self.guiStrings['confirm'].label.replace('{outputDir}',self.guiVars['exportDir'].get())
        messagebox.askyesno(self.window,message=message,icon='question',title=self.guiStrings['confirm'].help,type=okcancel)

    def drawConsole(self) :
        self.consoleFrame = Frame(self.root, padx=15)
        self.consoleFrame.grid(column=0,row=4,sticky="EW",pady=10)
        self.logTest = Text(self.consoleFrame, height=15, state='disabled', wrap='word',background='black',foreground='yellow')
        self.logTest.grid(column=0,row=0,sticky="EW")
        self.scrollbar = Scrollbar(self.consoleFrame, orient=VERTICAL,command=self.logTest.yview)
        self.scrollbar.grid(column=1,row=0,sticky=(N,S))
        self.logTest['yscrollcommand'] = self.scrollbar.set
        for var in self.guiVars :
            self.writeToLog(var + " : " + str(self.guiVars[var].get()))

    def writeToLog(self, msg):
        print(msg+'\n')
        numlines = self.logTest.index('end - 1 line').split('.')[0]
        self.logTest['state'] = 'normal'
        if numlines==24:
            self.logTest.delete(1.0, 2.0)
        if self.logTest.index('end-1c')!='1.0':
            self.logTest.insert('end', '\n')
        self.logTest.insert('end', msg)
        self.logTest.see(END)
        self.logTest['state'] = 'disabled'

if __name__ == "__main__":
    configuration = conf.loadConf(r"/home/thomas/code/perso/python/conf.conf")
    gui = GUI(configuration)
    gui.draw()

# Change ; as separator for imagePath, use |, check imagePath in guiStrings file
# Handle keepLevel and images path vars in/out values correctly
# Add correct help in gui conf file
# Save to memory and to conf file (using order)
# Change '#n' to '\n# ' on loading of guiStrings and/or saving
# Fully integrate logging
# Fully integrate with sorter
# Fix all layout shit
# Display folders status with icon
