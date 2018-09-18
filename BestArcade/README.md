## Best Arcade Tool

Use this tool to generate sorted romsets keeping only the games referenced in the [BestArcade4Recalbox list](https://docs.google.com/spreadsheets/d/1F5tBguhRxpj1AQcnDWF6AVSx4av_Gm3cDQedQB7IECk/edit?usp=sharing), above and equal to the working state level you choose.


### WHAT THIS TOOL DOESN'T DO :
- It's not clrmamepro and will not check that your romsets are in the right version number
- It only works with non-merged sets, split and merged sets are not supported, use clrmamepro to generate non-merged sets if needed
- It's not a scrapper per se, it will generate gamelists though, so be aware to remove them if you don't want to use them
- It doesn't handle CHD
- It only works on Windows

### WHAT THIS TOOL DO :
- Generate BestArcade romsets by using your fba_libretro, mame2003 and mame2010 non-merged sets, your original sets will be kept intact
- Generate csv files documenting the generated sets
- Generate a scoresheet comparing working level in generated sets
- Generate dat files for the generated romsets

### USAGE :
First modify the `conf.conf` file with your own parameters :
- `exportDir` : the target directory for generation, warning its whole content will be erased (you will be prompted) at the begining of the script
- `fbaSet`, `mame2003Set`, `mame2010Set` : the path to your original sets, this will be left untouched by the script
- `keepLevel`: the working state level at which you will keep the roms in the generated romset (i.e keepLevel 2 will keep only MOSTLY_WORKING and WORKING roms)
- `keepNotTested`: determines if untested roms will be kept or not
- `exclusionType`: determines how roms will be kept (based on their working state level) if you use several romsets
- `genreSubFolders`: determines if your romset will use sub folders for genre or not

Then just execute `BestArcade.exe`
After execution your will find your generated romsets in your `exportDir`

Build instructions are in `build.txt`
