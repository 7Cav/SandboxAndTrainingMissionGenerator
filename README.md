This is a mission generator script built to quickly and reliable build sandbox and training missions for the 7th Cavalry Gaming.

# Requirements
* Python3

# How to run
- (Soon) Modfify the `properties.ini` if if needed.
- Modify the script Globals in ``build.py`` if needed.
- Modify the Templates if change is needed.
- Run the script<br />
  Windows: `py build.py -b sandbox` or ` py build.py -b training`<br />
  Linux: `python3 build.py -b sandbox` or ` python3 build.py -b training`

# Setting up a sandbox template
- Mission file most be unbinirized.
- Script will primarily use the Generic template.<br />
  A custom template can be used to create one the folowing name is required:<br />
  `Template_Altis.Altis` or `Template_MyIsland.MyIsland`<br />
  The island need to be placed in the `./Template/sandbox/` directory.
- To allow the script to set the Respawn use the following coordinates:<br />
  `position[]={20.200001,25.200001,20.200001};` 
- Unit placement is recommended to be set in the lower left corner on short grid `00 00`.

# Setting up a training mission
- Mission file most be unbinirized.
- Training missions need to placed in `./template/training/`.
- Add additional mission scripts in `./scripts/` folder.
- Adjustments to `init.sqf` is required to be inside  `init.txt`. 
- Adjustments to `description.ext` is require to be inside `description.ext`. 
