## SystemSorter
*Compatible with Recalbox 6.1*


A script permitting the modifying of display order of systems.

The script is using the original es_systems.cfg file situated in */recalbox/share_init/system/.emulationstation*, modify its content order and the copy it to */recalbox/share/system/.emulationstation*

***Be aware that this file will take precedence over the original one so you should regenerate the file after each update to be sure to keep an up-to-date file***


Script usage is simple : copy it where you like in the share partition then execute it with *python SystemSorter.py*

Additionaly you can specify the type of order you want to use directly on the command line i.e. *python SystemSorter.py m*

Orders for now are :
* **Alphabetical** : alphabetical order of systems by their usage name  
* **Hardware Type** : ordered by chronological hardware type : home consoles, portable consoles, arcade, computers
* **Chronological** : ordered by release date
* **Retrochronological** : ordered by inversed release date (newer systems appear first)
* **Manufacturer** : ordered alphabetically by manufacturer's name of the system
* **Mixed** : ordered by hardware type, then manufacturer, then chronological

You can use as command line or input parameter the first letter of the order (except for Mixed use x) or its full name
