## Randomizer

This script allow you to launch randomly a game from any system or from a given system


### How it works

When choosing the 'all' options in the random system, the scripts uses the */recalbox/share_init/system/.emulationstation/es_systems.cfg* to get the list of systems and their command line.
It then selects one of the non-excluded system on random.
After that it selects one non-hidden game from the system's *gamelist.xml*, verify the file exists and launch it.

***Yes this means that only scrapped games and systems will be used***

Alternatively you can select one option like snes from the random system and only games from that system will be selected.

If some game didn't launch you can look at the log */recalbox/share/randomlog.csv* to see what happened

### Installation

* First copy the script in the */recalbox/share* folder
* Edit the */recalbox/share_init/system/.emulationstation/es_systems.cfg* file to add the new random system (don't forget first to remount with `mount -o remount,rw /`  )
	```xml
	<system>
        <fullname>Random</fullname>
        <name>random</name>
		<path>/recalbox/share/roms/random</path>
		<extension>.rdm</extension>
        <command>python /recalbox/share/randomizer.py %CONTROLLERSCONFIG% -rom %ROM%</command>
        <theme>random</theme>
		<platform>random</platform>
	</system>
	```
* If you used my SystemSorter script or duplicated your se_systems file there, you also need to modify */recalbox/share/system/.emulationstation/es_systems.cfg*
* Kill EmulationStation with `/etc/init.d/S31emulationstation` stop (wait for it)
* Copy the random folder into  */recalbox/share/roms* directory
* Copy theme/random directory in /recalbox/share_init/system/.emulationstation/themes/recalbox-next
* Now just reboot and it should work flawlessly :)
