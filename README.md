<p align="center">
<a href="https://github.com/7Cav/SandboxAndTrainingMissionGenerator/releases/latest"><img src="https://img.shields.io/github/release/7Cav/SandboxAndTrainingMissionGenerator.svg?style=for-the-badge&label=Release%20Build" alt="Release Build Version"></a>
<a href="https://github.com/7Cav/SandboxAndTrainingMissionGenerator/releases/latest"><img src="https://img.shields.io/github/downloads/7cav/SandboxAndTrainingMissionGenerator/total.svg?style=for-the-badge&label=Downloads" alt="Downloads"></a>
<a href="https://travis-ci.org/7Cav/SandboxAndTrainingMissionGenerator"><img src="https://img.shields.io/travis/7Cav/SandboxAndTrainingMissionGenerator.svg?style=for-the-badge&logo=Travis-CI" alt="Build"></a>
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
usage: build [-h] -p PACKAGE -pv PACKAGEVERSION -v VERSIONTAG [-y] [--color]
             [--version]
             {sandbox,training}

This script generates missions.

positional arguments:
  {sandbox,training}    This defines what kind of generation the script should
                        commit.

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        This defines what script package to install.
  -pv PACKAGEVERSION, --packageVersion PACKAGEVERSION
                        This define a version number of a given package to be
                        used in the script.
  -v VERSIONTAG, --versionTag VERSIONTAG
                        This define what version name you whant the file to
                        have.
  -y, --fastbuild       Will instantly run untill done.
  --color               Enable colors in the script.
  --version             show program's version number and exit

This build script generates sandboxes or training mapes bases on avalible templates.
The tool should be cross platform and can be used for other packages as well.
```
<!--- (Soon) Modfify the `properties.ini` if needed.-->
- Modify the `setup.json` if needed.
- Modify the Templates if needed. (See below for requirements.) 
- Run the script<br />
  Windows: `py build.py sandbox -v 1.0 -p cScripts.zip` or
           `py build.py training -v 1.0 -p cScripts.zip`<br />
  Linux: `python3 build.py sandbox -v 1.0 -p cScripts.zip` or
         ` python3 build.py training -v 1.0 -p cScripts.zip`

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
- Training missions name need to be in the following format `[Company]_CO_Trg_[My_Training_Mission_Name-Map]_DEVBUILD.[Island_Name]`<br />Example: `7cav_Charlie_CO_Trg_Map_DEVBUILD.Stratis` or `7cav_Charlie_CO_Trg_Ambush_DEVBUILD.Altis` 
- Training missions need to placed in `./template/training/`.
- Additional training mission scripts images or other material need to be placed in the mission root folder. 
- Adjust or add a `setup.json`<br />__NOTE!__ Do not add your own `init.sqf` of `description.ext` they will be overwritten. instead add changes or adjustmetns instead to the `add : []` array of the json file.

## Custom build
The custom mission build is preformed when you use the `training` and `-mission [mission]` parameters.
To run this you need to be placed the mission in; `./template/training/`. The build follows the training mission build system. But instead of building all missions it only build for one. Exsample:<br />
`$ build.py training -v 1.0 -p cScripts.zip -m My_Mission_Name.Island`

## String hooks
String hooks refere to names that the script look for in order to replace a Line. If it can't fine the string it will skip the change.

### mission.sqm
- **briefingName:** `$briefingName`, `Zeus Sandbox Template Mission`, `Training Template Mission` (string)
- **overviewText:** `$overviewText`, `OverviewText Template Text` (string)
- **Spawn point move pos:** `position[]={20.200001,25.200001,20.200001};`

### description.ext
<!--
- **author:** `$author`, `1SG Tully.B`
- **onLoadName** `MyMissionName`
- **onLoadMission** `7th Cavalry - S3 1BN Battle Staff Operation`
- **onLoadIntro** `S3 1BN Battle Staff Operation`
- **loadScreen** `Data\MissionLogo.paa`
- **overviewPicture** `Data\MissionLogo.paa`
- **cba_settings_hasSettingsFile** `cba_settings_hasSettingsFile = 1;`
- **disabledAI** `disabledAI              = true;`
-->

### Magicwords
- `$1`: Print version number provided by `--versionTag` parameter.
- `$2`: Print name of the installed package selected by `--packageVersion` parameter.
