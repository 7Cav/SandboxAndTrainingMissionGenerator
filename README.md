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
usage: build [-h] -p PACKAGE -v VERSIONTAG [-y] [--color] [--version]
             {sandbox,training}

This script generates missions.

positional arguments:
  {sandbox,training}    This defines what kind of generation the script should
                        commit.

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        This defines what script package to install.
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

## Setting up a training mission (WIP)
- Training missions name need to be in the following format `7cav_[Company]_CO_Trg_[My_Training_Mission_Name-Map]_DEVBUILD.[Island_Name]`<br />Example: `7cav_Charlie_CO_Trg_Map_DEVBUILD.Stratis` or `7cav_Charlie_CO_Trg_Ambush_DEVBUILD.Altis`
- Training missions need to placed in `./template/training/`.
- Additional training mission scripts need to be placed in the mission folder in `./scripts/` or `./` folder.
- Adjust or add a `setup.json`<br />__NOTE!__ Do not add your own `init.sqf` of `description.ext` Add changes or adjustmetns instead to the `add : []` array of the json file.