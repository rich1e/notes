--- SOURCE: https://www.gamebrew.org/wiki/NeoDS ---
--- ARCHIVED: 2024-12-26 via web.archive.org (gamebrew 403 blocks live) ---
--- INFOBOX: Author Ben Ingram (Ingramb) | Version 0.2.1.b | Last Updated 2020-08-26 ---
--- original oldid: 186632 | Last modified 2024-08-21 ---

 
This is a NeoGeo AES/MVS emulator for the Nintendo DS. It can run all types of NeoGeo roms with some limitations.



## Features


- M68000 cpu (cyclone).

- Z80 cpu (DrZ80).

- All forms of NeoGeo protection/encryption.

- Graphics.

- ADPCM audio.

- PSG audio.


## Installation


Note: To use this emulator, you will need to prepare the compatible BIOS ROM (neogeo.zip).

Patch NeoDS.nds for your [DLDI](/web/20241226045410/https://www.gamebrew.org/wiki/DLDI) flash card (not all flashcards require patching).

Convert some NeoGeo roms (mslug.zip for example). NeoDS uses the same rom sets as MAME, make sure they work in MAME before proceeding. 

Put all the roms you want to convert along with the bios together in a folder. 

Copy NeoDSConvert.exe into the same folder. 

Run NeoDSConvert, and it will convert all the NeoGeo roms in that folder. The converted roms will have the *.neo extension.

Copy the [DLDI](/web/20241226045410/https://www.gamebrew.org/wiki/DLDI) patched NeoDS.nds, and all the *.neo roms into the root of your flashcard. 


## User guide


- Run NeoDS.nds, the main menu should load, showing you a list of all the roms on your card.

- Use the arrow keys to select, and press start to choose a rom to load. You can load a rom without audio which will improve frame rate, but you won't get any sound (obviously).

- Once a game is loaded without audio, the only way to get audio back is to reload the game. Some games will freeze with audio disabled, so be warned.

- If you have a supported flashcard with external ram in the GBA slot (optional), NeoDS will use the extra ram to cache more data. This will improve the speed of some games, but is never required. The main gui screen will display the test SLOT2 if this feature is active.

NeoDS GUI: 

- Video - Video can be normal or scaled. Normal is a cropped screen. Scaled shows the full screen, but scaled down to fit.

- CPU Clock - The NeoGeo cpu can be underclocked. Experiment and see (it is easier for NeoDS to emulate a slower cpu, and some NeoGeo games don't use the full cpu power anyway).

- Screen Off - The lower screen can be turned off. Touch anywhere to turn it back on.

- Load rom - Load a new game.

- Save - Write the current configuration and sram to the flashcard.

- Input - Remap the input.
The input configuraiton screen is a grid. DS buttons are down the right side of the screen. NeoGeo buttons are along the top of the screen.

- Each row of boxes coorisponds to one DS button. Putting a check in a box maps a NeoGeo button to a DS button.

- You can map multiple NeoGeo buttons to a single DS button this way, which can be useful for fighting games, or for other things.


### Compatibility list

A list of tested ROMS can be found in the [discussion thread](https://web.archive.org/web/20241226045410/https://groups.google.com/g/neods/c/yyZio11xtGE/m/PwHTTCiABkwJ).

### Forks

- NeoDS TWL - By Universal-Team. Integrated into Twilight Menu++ , update from 2.0 source.

- NeoDS GBMacro (wip) - By xonn83. Version to use in a GameBoy Macro, based on NeoDS 0.2.0. Read more .

- NeoDS 0.2.0 EZ flash 3in1 - By j03lpr86. Version for EZ Flash 3in1, based on NeoDS 0.2.0.

- NeoDS 0.21 & NeoDS 0.21.b - By nitendo. Changes include:
Maximum amount of roms in rom-Menu increased from 64 to 256.

- Left/Right on D-pad now corresponds to pageUp/pageDown in rom-Menu.

- All config-files are now stored in directory "fat:/data/neoDS/".

- All roms can be stored in separate directory according to "_NeoDs.ini"​.

- 021b_scaled will scale all game by default.

- NeoDS 0.21 mod - By indy13. Changes the path to the roms and added a translated readme (French/English).


## Controls


D-Pad - Arrow keys

A/B/X/Y - A/B/C/D

L - Pause

R - Select (acts as coin input using newer versions of universal bios)

Start - Start

Select - Coin

Stylus - NeoDS GUI


## Screenshots





## Media


NeoDS Tutorial Step by step ([Meanpooh](https://web.archive.org/web/20241226045410/https://www.youtube.com/watch?v=5yipAW796hM)) 




## Known issues


Not emulated - FM audio, Raster effects, Multiplayer.

Some timings are not that accurate.


## Changelog


v0.2.0 2008/06/19 

- Key configuration.

- Pause key.

- Put DS to sleep when lid is closed.

- Save SRAM and NeoDS configuration to flashcard.

- Fix crash when switching roms on certain flash cards.

- Fix palettte bank swap bug on tile layer (metal slug 1 hud).

- Improve accuracy of vcounter, and vposition interrupts (fix freeze in Samurai Showdown 3, fix graphics in Blazing Star level 2, probly others).

- Fix issues when using dldi and slot2 ram from same flashcard (like supercard lite).

- Fix graphical corruption that occurs after a while when using slot2 ram.

v0.1.1a 2008/05/06 

- Forgot to include updated NeoDSConvert is last version.

v0.1.1 2008/05/06 

- Added level2 sprite cache in slot2 ram (if installed).

- Increased rom page size (fix grenades Metal Slug 1).

- Fix interrupt acknowledge (fix Metal Slug 2).

- Fix tile layer palette update (Last Blade 2 gui).

- Update converter to use latest MAME data (fix issues with King of Fighters 98, etc).

- Thanks to FluBBa for a DAA Z80 instruction that doesnt need a stupid lookup table (saves ram).

- Fixed -bios options in NeoDSConvert.

v0.1.0 2008/04/29 

- Initial release.

Summer 2007 

- Project started.


## Credits


FinalDave, notaz, Reesy, Wintermute, chishm, MAME, Minizip, www.pocketheaven.com for hosting a NeoDS forum, FluBBa, GnGeo, FinalBurnAlpha, MVSPSP, Charles MacDonald, Alexander Stante, Brandon Long.

Everyone who answers questions on the gbadev.org forums.


## External links


- Google Groups - http://groups.google.com/group/neods

- GitHub - https://github.com/Yardape8000/NeoDS

- Notes on using the convertor - https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/post-10307753






Retrieved from ‘[https://www.gamebrew.org/index.php?title=NeoDS&oldid=186632](https://web.archive.org/web/20241226045410/https://www.gamebrew.org/index.php?title=NeoDS&oldid=186632)’ 





Last modified




- 21 August 2024









Contents 














GameBrew 

The goal of GameBrew is to provide information about homebrew for all old and latest consoles.

All credits go to all the homebrew creators and developers ♥




- Privacy policy

- About GameBrew

- Disclaimers





Powered by MediaWiki. 


- 











