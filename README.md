# ROMs Helper
This is a CLI (command-line interface) tool, meaning it works within your terminal: *"the black magic box"*. 
But don’t worry: it’s fully interactive, and you won’t need to do anything technical.

#### Currently, the program provides the following tools:

- Detects duplicated or similar games between different consoles to help curate your collection.
- Generates a summary text file to browse your collection easily.
- Creates a statistics text file based on your games.
- Automatically cleans and renames game files.

Safety measures included, with the ability to reverse changes.


## How to start:
This application is what's called *portable*: no installation required, but execution varies between systems.
(i.e., Windows, Linux, or macOS). Once you are done, head to the next section.

### Windows:
  
1. Download the latest release of **ROMsHelper-windows-x86_64.zip** from [here](https://github.com/Malagel/ROMs-Helper/releases/).
2. Go to Downloads and extract it.
3. Go inside the folder and double-click ROMsHelper to open the tool.

### Linux:

1. Download the latest release of **ROMsHelper-linux-x86_64.zip** from [here](https://github.com/Malagel/ROMs-Helper/releases/).
2. Go to Downloads and extract it.
3. Open your terminal and run these commands:
```bash
cd ~/Downloads/ROMsHelper
chmod +x ROMsHelper
./ROMsHelper
```
### macOS:

1. Download the latest release of **ROMsHelper-macos-x86_64.zip** from [here](https://github.com/Malagel/ROMs-Helper/releases/).
2. Go to Downloads and extract it.
3. Go inside the folder and open ROMsHelper with **Right-click → Open → Open**. You may need to allow the app in Security settings the first time.

## Usage:

### 1) Structure of your ROMs folder:

When you open the program, it will ask for the location of your **ROMs folder**. You can either drag and drop the folder into the window, or manually paste the path.

The folder needs to follow this structure:
```
MyROMsFolder/              
├─ PlayStation 2/           
│ ├─ Game 1
│ └─ Game 2
├─ Nintendo Gamecube/       
│ ├─ Single Disk/
│ │ ├─ Game 1
│ │ └─ Game 2
│ └─ Multi Disk/
│ │ ├─ Game 1
│ │ └─ Game 2/
│ │ │ ├─ Disk 1
│ │ │ └─ Disk 2
```
This means: 

- Your **ROMs folder** is the main folder that contains everything.
- Each **console** must have its own folder inside the ROMs folder.
- Inside a **console folder**, every **file or folder** is treated as a **game**, unless it is a **valid subfolder**.
- A **valid subfolder** is by default named **Single Disk** or **Multi Disk** (this can be changed; see the [**Advanced Options**](#advanced-options) section).
-  **Single Disk** and **Multi Disk** must only contain **games** (files or folders).
- No additional subfolders are allowed inside **Single Disk** or **Multi Disk**.

### 2) Selecting the tool you want to use:
After choosing your ROMs folder, you will be shown a list of available tools to execute. To use one, simply type the number next to it and press Enter. You can select multiple if you want.

Some of the tools offer extra (advanced) options. These are optional and are explained in the [**Advanced Options**](#advanced-options) section.

Example: after just pasting your ROMs path, this will appear:
```
Select the actions to perform, separated with spaces (e.g.: 1 3 5):

[1] Detect duplicated games.
[2] Clean your game names (rename files).
[3] Generate statistics.
[4] Create a summary.
```
If you want to execute the 3rd and 4th tools, just type: 

- `3 4`

## Tools

**[IMPORTANT]:** Most of the tools rely on the [**folder structure**](#usage) described above, so make sure you are following it or modifying it correctly (check [**Advanced Options**](#advanced-options)). 
### [1] Detect duplicated games:

This tool will scan your entire ROMs folder, looking for similar games (based on their names) that you may have duplicated.

After that, it will show them to you. You can choose which ones get moved to a "DELETE" folder (placed just outside the program).

Useful for curating your games by finding duplicates or better versions of games.

Example of executing the tool:
```
• Found 3 games with the threshold as default:

[1] Aladdin → Nintendo - SNES
[2] Aladdin → Sega - Game Gear
[3] Aladdin → Sega - Genesis

Select the games you wish to move to a folder, separated with spaces (e.g.: 1 3 4).
(Leave it blank to skip or type 'quit' to exit):
```
If here we enter `1 3` , this will appear:
```
> 1 3

• These game paths will be moved to the 'DELETE' folder:
▶ /path/to/your/ROMs/Nintendo - SNES/Aladdin.sfc
▶ /path/to/your/ROMs/Sega - Genesis/Aladdin.md

Do you confirm? [y/N]
```
If we type `y` :
```
> y

• Moved 2 games to the DELETE folder.
```
This will repeat for all detected games within a certain similarity value called **threshold**, which can be customized with special commands. 

If you want to tinker with it and check more options, head to the [**Advanced Options**](#advanced-options) section. 

### [2] Clean your game names (rename files):
This tool will scan your ROMs folder looking for games, and rename them with the following rules:
- Removes all content inside parentheses:
`Resident Evil 4 (USA)(Undub)(Spanish Patch).iso` --> `Resident Evil 4.iso`

- Removes extra spaces (this `·` represents a space):
`Resident······Evil·4····.iso` --> `Resident·Evil·4.iso`

- Replaces `_` with spaces:
`Resident___Evil_4.iso` --> `Resident Evil 4.iso`

- Removes versioning:
`Resident Evil 4 v1.3.4.iso` --> `Resident Evil 4.iso`

All of these changes are applied automatically to every detected game. 

The tool also creates a backup so you can easily undo all changes. Check the [**Advanced Options**](#advanced-options) section. 

### [3] Generate statistics:

This tool will generate a text file with statistics based on your **ROMs folder**.   

It will include:
- When it was generated (date).
- A small summary with:
	- Total number of games.
	- Total number of consoles.
	- Total size of your collection.
- A list of your consoles indicating the number of games in decreasing order.
- A list of your consoles indicating their size in decreasing order, including:
	- Biggest size game.
	- Smallest size game. 

Example of the statistics file:
```
==========================================================================================
                                      ROMS STATISTICS
==========================================================================================

Generated on : 26/01/2026 at 18:56:30

SUMMARY
------------------------------------------------------------------------------------------
Total Games          : 75
Total Size           : 229.23 GB
Consoles Analyzed    : 2

GAMES PER CONSOLE
------------------------------------------------------------------------------------------
[01] Sony - PlayStation 2                :    58 games
[02] Nintendo - Switch                   :    17 games

STORAGE PER CONSOLE
------------------------------------------------------------------------------------------
[01] Nintendo - Switch                                                 :  123.54 GB
      Biggest game  : Persona 5 Royal                                         →   14.19 GB
      Smallest game : Corpse Party                                            →  962.75 MB

[02] Sony - PlayStation 2                                              :  105.69 GB
      Biggest game  : Yakuza 2                                                →    5.35 GB
      Smallest game : Rez                                                     →  118.37 MB
```


### [4] Create a summary:

This tool will generate a text file with a summary of your entire collection. This means that it will list every console with their respective games one by one. 

It will be organized alphabetically, exclude file extensions, and show subfolders.

Example of the generated summary:
```
==========================================================================================
                                        ROMS SUMMARY
==========================================================================================

Generated on: 26/01/2026 at 19:24:17

[ Atari - 2600 ]
------------------------------------------------------------------------------------------
• Adventures of TRON
• Air Raiders

[ Nintendo - 64 ]
------------------------------------------------------------------------------------------
• 007 - The World Is Not Enough
• 1080 Snowboarding - US

[ Sega - Dreamcast ]
------------------------------------------------------------------------------------------
▶ Subfolder : Multi-Disk
    • Resident Evil - Code - Veronica
    • Shenmue
    • Skies of Arcadia
▶ Subfolder : Single-Disk
    • Blue Submarine No.6
```

## Advanced Options

This section provides useful options for tinkering with configurations and executing specific actions within the program. For that, we will be using commands. 

To add a command, simply write it **in the same input** when we are selecting a tool, separated by a space:

For example:  
```
Select the actions to perform, separated with spaces (e.g.: 1 3 5):

[1] Detect duplicated games.
[2] Clean your game names (rename files).
[3] Generate statistics.
[4] Create a summary.
```
Here if we want to detect duplicates, but avoid confirmation prompts, we can type:

- `1 --no-confirmation`

This will execute the `[1] Detect duplicated games` tool , and also skip confirmation prompts as per the command `--no-confirmation`.

Some of the commands take values. This will be indicated with placeholders `[LIKE THIS]` that need to be replaced by you.


### General Commands:
These commands do not target a specific tool and are for general use. This means you can use them with every tool, even multiple at the same time.

- `--logs` : Generates a log file that tracks every interaction with the program. Useful if you want to know what's being done *"under the hoooood"*.
- `--debug` : Gives more context to errors. Useful for developers.
- `--custom-subfolders [SUBFOLDER-1,SUBFOLDER-2]` : Adds another **valid subfolder** to recognize games inside. To use it, type the command and then the subfolder names:
	- E.g.: `--custom-subfolders my-subfolder,my-other-subfolder`
	- This will add "my subfolder" and "my other subfolder".
	- Note that spaces are replaced with hyphens (`-`) . If yours have them already, still include them.       
	- Subfolders are separated **only** by a comma (`,`) . No spaces allowed >:(
	- Not case-sensitive. 
- `--no-confirmation`: The program will omit confirmation. It won't ask you "yes or no", it will just do it.


### Specific Commands:
These commands work **only** and **along**  their respective tools. Meaning you need to add the command when calling the tool you want. Using them with other tools won't do anything to them.

 `[1] Detect duplicated games` tool:
 
- `--duplicates-threshold [NUMBER]`: Uses a different floating point value for the similarity threshold. The default is set to `80.0`. To use it, type the command and then the desired value:
	- E.g.: `--duplicates-threshold 100`
	- This will use `100` as the threshold.
	- Similarity is based on cleaned game names (extensions, regions, versions removed) and compared **textually**.
	- The higher the number, the more similar the chosen games are (up to and including `100`).
	- The lower the number, the less similar the chosen games are (down to and including `1`).
 
- `--no-safe-deletion`: By default, the tool moves the games you select to a `DELETE` folder. You can include this command to delete them **permanently.**

`[2] Clean your game names (rename files)` tool:
- `--reverse-renaming`: If you want to undo the effects of the tool. Useful if you didn't like the way it renamed your games.
- `--no-renames-backup`: By default, the `clean your game names` tool saves a backup every time it is used. This disables that behaviour and doesn't save anything when used.