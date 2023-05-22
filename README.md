<p align="center">
<a href="https://github.com/7Cav/SandboxAndTrainingMissionGenerator/releases/latest"><img src="https://img.shields.io/github/release/7Cav/SandboxAndTrainingMissionGenerator.svg?style=for-the-badge&label=Release%20Build" alt="Release Build Version"></a>
<a href="https://github.com/7Cav/SandboxAndTrainingMissionGenerator/releases/latest"><img src="https://img.shields.io/github/downloads/7cav/SandboxAndTrainingMissionGenerator/total.svg?style=for-the-badge&label=Downloads" alt="Downloads"></a>
<a href="https://github.com/7Cav/SandboxAndTrainingMissionGenerator/actions?query=workflow%3A%22Build+and+Deploy%22"><img src="https://img.shields.io/github/workflow/status/7Cav/SandboxAndTrainingMissionGenerator/Build%20and%20Deploy/master?logo=GitHub&style=for-the-badge" alt="Build"></a>
</p>

This is a mission generator script built to quickly and reliable build sandbox and training missions for the 7th Cavalry Gaming.

# Requirements
* [Python3](https://www.python.org)
* [armake](https://github.com/KoffeinFlummi/armake)

## Install
**Windows:** 
- [Download and install python3](https://www.python.org)
- [Download and install armake](https://github.com/KoffeinFlummi/armake/releases/latest)
  
**Linux:**
```
$ sudo apt-get install python3
```
```
$ sudo add-apt-repository ppa:koffeinflummi/armake
$ sudo apt-get update
$ sudo apt-get install armake
```

# How to run
```
usage: build [-h] -p PACKAGE [-pv PACKAGEVERSION] [-o OUTPUT] -v VERSIONTAG [-y] [--color]
             [-m MISSION] [-s SETTING] [--version]
             {sandbox,training}

This script generates sandbox or training missions.

positional arguments:
  {sandbox,training}    This defines what kind of generation the script should commit.

options:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        This defines what script package to install.
  -pv PACKAGEVERSION, --packageVersion PACKAGEVERSION
                        This define a version number of a given script installation package
                        to be used in the script. (Suggestively the release version name)
  -o OUTPUT, --output OUTPUT
                        This allow you to define a output suffix.
  -v VERSIONTAG, --versionTag VERSIONTAG
                        This define what version name you want the file to have.
  -y, --fastbuild       Will instantly run until done.
  --color               Enable color in the script.
  -m MISSION, --mission MISSION
                        Define a specific mission from path
  -s SETTING, --setting SETTING
                        Define a custom setup.json file
  --version             show program's version number and exit

This build script generates sandboxes or training maps bases on provided templates.
The tool should be cross platform and requires armake to function.
```
<!--- (Soon) Modfify the `properties.ini` if needed.-->
- Modify the `setup.json` if needed.
- Modify the Templates if needed. (See below for requirements.) 
- Run the script<br />
  Windows: `> py build.py sandbox -v 1.0 -p cScripts.zip` or
           `> py build.py training -v 1.0 -p cScripts.zip`<br />
  Linux: `$ ./build.py sandbox -v 1.0 -p cScripts.zip` or
         `$ ./build.py training -v 1.0 -p cScripts.zip`

## Setting up a sandbox template
- __Mission file most be unbinirized__.
- Script will primarily use the Generic template.<br />
  A custom template can be used to create one the folowing name is required:<br />
  `Template_Altis.Altis` or `Template_MyIsland.MyIsland`<br />
  The island need to be placed in the `./Template/sandbox/` directory.
- To allow the script to set the Respawn use the following coordinates:<br />
  `position[]={20.200001,25.200001,20.200001};` 
- Unit placement is recommended to be set in the lower left corner on short grid `00 00`.

## Setting up a training mission
- __Mission file most be unbinirized__.
- Set the `briefingName` name to `Training Template Mission`
- Training missions need to placed in `./template/training/`.
- Additional training mission scripts images or other material need to be placed in the mission root folder. 
- Adjust or add a `setup.json`<br />__NOTE!__ Do not add your own `init.sqf` of `description.ext` they will be overwritten. Instead add changes or adjustmetns settings by defining them in the json file. You can find a exsample [here](https://github.com/7Cav/SandboxAndTrainingMissionGenerator/blob/master/template/training/setup_template.json).

## Custom build
The custom mission build is preformed when you use the `training` parameter and define a `-mission [mission]` parameter.
The mission need to be placed in; `./template/custom/`. The build follows the training mission build system. But instead of building all missions it only build for one. Run exsample:<br />
`$ ./build.py training -v 1.0 -p cScripts.zip -m My_Mission_Name.Island`

## String hooks and magicwords
String hooks refere to names that the script look for in order to replace a Line. If it can't fine the string it will skip the change.

### Directoryname
- **DEVBUILD:** `DEVBUILD` will be replaced with `versionTag` (Exsample: `v1.2`)

### mission.sqm
- **authot** `$author` (string)
- **briefingName:** `$briefingName`, `Zeus Sandbox Template Mission`, `Training Template Mission` (string)
- **overviewText** `$overviewText`, `OverviewText Template Text` (string)
- **Spawn point move pos:** `position[]={20.200001,25.200001,20.200001};` (auto)

### description.ext
- **author/dev** `$author`, `1SG Tully.B` (string)
- **onLoadName** `$onLoadName`, `MyMissionName` (string)
- **onLoadMission** `$onLoadMission` `7th Cavalry - S3 1BN Battle Staff Operation` (string)
- **onLoadIntro** `$onLoadIntro`, `S3 1BN Battle Staff Operation` (string)
- **loadScreen** `Data\MissionLogo.paa` (string)
- **overviewPicture** `Data\MissionLogo.paa` (string)
- **cba_settings_hasSettingsFile** `cba_settings_hasSettingsFile = 1;` (number)
- **disabledAI** `disabledAI              = true;` (bool)
- **forceRotorLibSimulation** `forceRotorLibSimulation = 1;`
- **spawn** `respawn                = BASE;` (string)
- **respawnDelay** `respawnDelay           = 4;` (number)
- **respawnOnStart** `respawnOnStart         = -1;` (number)

### Magicwords
- `$0`: Print version number provided by `--versionTag` parameter.
- `$1`: Print name of the installed package selected by `--packageVersion` parameter.
