# Chobits-Translation-Project
A project aimed at translating the game Chobits: Chiidake no Hito for the PS2 into English. Predominately AI translated with manual edits. Currently, 99% of the ingame text is translated and all video cutscenes are subtitled. The audio is still in Japanese, and some UI elements are not translated.

### How to Install:

1. Obtain a copy of 'Chobits - Chiidake no Hito [NTSC-J] [SLPM-65255]' for the PS2. For copyright reasons this cannot be distributed here.
2. Download your preferred copy of the mod from the [Releases](https://github.com/sam8457/Chobits-Translation-Project/releases) section. I recommend the 'With Video' option.
3. Download a program to patch the game, such as DeltaPatcher ([Romhacking.net](https://www.romhacking.net/utilities/704/), [GitHub](https://github.com/marco-calautti/DeltaPatcher)) though any that can handle .xdelta files will work.
4. Run the program and select your original disk image under 'Original file'. Select the .xdelta file under 'XDelta patch'.
5. Click 'Apply Patch', it should take 5-10 seconds to modify the file. By default DeltaPatcher will overwrite the original.

Once that's done, boot up the game and have fun!

### How to Update:

When future versions come out, download the most recent patch and use it on the ***original*** Japanese version via the instructions in the previous section, then run the new version. Saves are compatible between versions and with the original.

### Common Issues:
* Spelling mistakes and occasional missed textboxes are present. Missed textboxes just look like gibberish English. If you find one, feel free to submit a screenshot under the Issues tab.
* The section where Chi goes out to buy underwear will frequently reset the player's progress. This seems to occur in the original game also. Just keep hitting Square and after a few ingame days it will eventually progress.
* Chi does not change clothes permanently when you select it from the menu. This is present in the original game.
* If DeltaPatcher gives the error 'The patch could not be applied: The file you are trying to patch is not the right one.', it means the original game file isn't correct. Try verifying the file signature. 89ad4ccf90ac7481bbf8502f417a0eef57733204 is the correct hash from [Redump.org](http://redump.org/disc/29067/). On Windows this can be done with the following PowerShell command (replace filename.iso with your game file's name): 
```
Get-Filehash '.\filename.iso' -Algorithm SHA1 | Format-List
```
