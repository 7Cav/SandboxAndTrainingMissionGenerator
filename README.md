This is a script that create a bunch of missions changes parameters for all 7th Cavalry Supported Arma3 island.

# How to run
- Edit the Globals in the header of make.py
- Run the script

# Setting up a mission template
- Mission most be unbinirized
- Respawn must be on the following coardinates to be moved by the script: `position[]={20.200001,25.200001,20.200001};` Respawn  will not be moved if this is not defined.
- Place units on short ingame grid 00 00

# To do
- Define globals via ini file instead of header
  - Set mission name
  - Set author
  - Island array
  - Spawn array
  - Define mission framework zip
  - Change CBA settings
- Allow sqf bases and map adjustments
  - setup_sandbox_base.altis.sqf
- Zip missions created.
