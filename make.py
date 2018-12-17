#!/usr/bin/env python3
import sys, os, time, subprocess
import pathlib, shutil, tempfile, zipfile

############## GLOBALS ################

# Version number
MAJOR = '1'
MINOR = '0'
PATCH = '18'

SCRIPT_PACKAGE = 'cScripts_v4.2.15.zip'

WORLDLIST = [
    'Altis',
    'Bootcamp_ACR',
    'chernarus_summer',
    'chernarus',
    'Desert_E',
    'fallujah',
    'intro',
    'lythium',
    'Malden',
    'Mog',
    'Mountains_ACR',
    'pja319',
    'porto',
    #'prei_khmaoch_luong',
    'pja310',
    'pja307',
    'pja308',
    'pja306',
    'pja314',
    'ProvingGrounds_PMC',
    'sara_dbe1',
    'sara',
    'saralite',
    'Shapur_BAF',
    'Stratis',
    'takistan',
    'Tanoa',
    'utes',
    'VR',
    'Woodland_ACR',
    'zargabad'
]
WORLDLIST_XYZ = [
    [14180.181,19.533018,16286.612],    #Altis
    [1736.0146,339.00143,1821.2036],    #Bootcamp_ACR
    [4734.9082,339.00143,10321.878],    #chernarus_summer
    [4734.9082,339.00143,10321.878],    #chernarus
    [1356.26,40.934971,1456.3073],      #Desert_E
    [7798.8213,7.0014391,1834.03],      #fallujah
    [2599.9934,13.861439,2851.6333],    #intro
    [12284.305,32.930412,1994.9125],    #lythium
    [757.7951,28.921438,12122.284],     #Malden
    [8241.5498,3.2092922,5366.6777],    #Mog
    [4541.0576,145.40143,6041.1016],    #Mountains_ACR
    [1607.7159,637.45093,3306.1414],    #pja319
    [2572.7817,5.030777,2394.7749],     #porto
    #[5677.208,111.26981,4182.6396],    #prei_khmaoch_luong
    [1315.1356,15.050012,985.10767],    #pja310
    [5353.0347,273.7785,14497.363],     #pja307
    [7668.6006,7.7759309,10451.485],    #pja308
    [15625.017,398,12116.016],          #pja306
    [753.32843,143.50633,1481.077],     #pja314
    [710.72131,51.721439,1171.8711],    #ProvingGrounds_PMC
    [9561.6406,139.99643,9872.0205],    #sara_dbe1
    [9561.6406,139.99643,9872.0205],    #sara
    [4679.4258,139.98586,7108.8965],    #saralite
    [712.9986,35.381439,409.31555],     #Shapur_BAF
    [2159.5532,6.0014391,5690.1865],    #Stratis
    [6112.4971,83.041443,11524.703],    #takistan
    [11785.61,6.9514389,13067.984],     #Tanoa
    [1375.572,15.88654,962.66998],      #utes
    [7439.9927,5.0014391,7568.0435],    #VR
    [4692.2144,6.0036001,1175.9294],    #Woodland_ACR
    [4967.8613,29.545662,6143.1611]     #zargabad
]

VERSION = '{}.{}.{}'.format(MAJOR,MINOR,PATCH)
VERSION_DIR = '{}_{}_{}'.format(MAJOR,MINOR,PATCH)

# path: {0} filename: {1}
#PBOPACKINGTOOL = 'D:\\Tools\\Arma3\\PBO Manager v.1.4 beta\\PBOConsole.exe -pack "{0}\\{1}" "{0}\\release\\{1}.pbo"'

############## ####### ################

############## ####### ################

def getMissionData(file,string):
    try:
        os.stat('{}'.format(file))
    except:
        sys.exit('{} could not be found...'.format(file))

    fileObject = open('{}'.format(file), "r")
    for l in fileObject:
        if (string in l):
            missionData = l
    fileObject.close()
    return missionData

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = tempfile.mkstemp()
    with os.fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    os.remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)

def add(file, string):
    fileObject = open('{}'.format(file), "a")
    fileObject.write(string)

def main():
    projectPath = os.path.dirname(os.path.realpath(__file__))
    islandList = []

    for world in WORLDLIST:
        newWorld = '7cav_zeus_sandbox_v{}.{}'.format(VERSION_DIR,world)
        print('Creating {}. ({}/{})'.format(world,len(islandList)+1,len(WORLDLIST)))

        pathlib.Path(newWorld).mkdir(parents=True, exist_ok=True)
        shutil.copy2('Template_Sandbox.VR\\mission.sqm', newWorld)

        # Changing version in mission.sqm
        x = getMissionData('{}\\mission.sqm'.format(newWorld), 'briefingName=')
        replace('{}\\mission.sqm'.format(newWorld), x, '\t\tbriefingName="Zeus Sandbox v{}";\n'.format(VERSION))

        print('Installing script package...')
        try:
            scriptsArchive = zipfile.ZipFile(SCRIPT_PACKAGE, 'r')
        except:
            sys.exit("Could not locate \"{}\" package file in the root directory...".format(SCRIPT_PACKAGE))
        scriptsArchive.extractall(newWorld)
        scriptsArchive.close()


        print('Adjusting description.ext...')
        # find dev
        x = getMissionData('{}\\description.ext'.format(newWorld),'dev')
        replace('{}\\description.ext'.format(newWorld), x, '    dev                 = "CPL Brostrom.A";\n')
        # find authur
        x = getMissionData('{}\\description.ext'.format(newWorld),'author')
        replace('{}\\description.ext'.format(newWorld), x, '    author              = "CPL Brostrom.A";\n')
        # find onload lable
        x = getMissionData('{}\\description.ext'.format(newWorld),'onLoadName')
        replace('{}\\description.ext'.format(newWorld), x, '    onLoadName          = "Zeus Sandbox v{}";\n'.format(VERSION))
        # find onLoadMission lable
        x = getMissionData('{}\\description.ext'.format(newWorld),'onLoadMission')
        replace('{}\\description.ext'.format(newWorld), x, '    onLoadMission       = "7th Cavalry - S3 1BN Battle Staff Sandbox";\n')
        # find onLoadIntro lable
        x = getMissionData('{}\\description.ext'.format(newWorld),'onLoadIntro')
        replace('{}\\description.ext'.format(newWorld), x, '    onLoadIntro         = "S3 1BN Battle Staff Sandbox";\n')
        # find chaning respawn
        x = getMissionData('{}\\description.ext'.format(newWorld),'respawnOnStart')
        replace('{}\\description.ext'.format(newWorld), x, '    respawnOnStart         = 1;\n')


        print('Adjusting cba_settings.sqf...')
        x = '{}\\cba_settings.sqf'.format(newWorld)
        add(x, '\n')
        add(x, '// cScripts Mission Settings\n')
        add(x,'force force cScripts_Settings_allowCustomInit = true;\n')
        add(x,'force force cScripts_Settings_allowCustomTagging = true;\n')
        add(x,'force force cScripts_Settings_enable7cavZeusModules = true;\n')
        add(x,'force force cScripts_Settings_enableStartHint = true;\n')
        add(x,'force force cScripts_Settings_enforceEyewereBlacklist = false;\n')
        add(x,'force force cScripts_Settings_jumpSimulation = 1;\n')
        add(x,'force force cScripts_Settings_jumpSimulationGlasses = true;\n')
        add(x,'force force cScripts_Settings_jumpSimulationHat = true;\n')
        add(x,'force force cScripts_Settings_jumpSimulationNVG = true;\n')
        add(x,'force force cScripts_Settings_setAiSystemDifficulty = 0;\n')
        add(x,'force force cScripts_Settings_setCustomHintText = "Be creative!";\n')
        add(x,'force force cScripts_Settings_setCustomHintTopic = "Zeus Sandbox v{}";\n'.format(VERSION))
        add(x,'force force cScripts_Settings_setMissionType = 0;\n')
        add(x,'force force cScripts_Settings_setPlayerRank = true;\n')
        add(x,'force force cScripts_Settings_setRedLightTime = 30;\n')
        add(x,'force force cScripts_Settings_setTrainingHintTime = 20;\n')
        add(x,'force force cScripts_Settings_showDiaryRecords = true;\n')
        add(x,'force force cScripts_Settings_useCustomSupplyInventory = false;\n')
        add(x,'force force cScripts_Settings_useCustomVehicleInventory = true;\n')
        add(x,'force force cScripts_Settings_useCustomVehicleSettings = true;\n')


        print('Removing immortality from S3 loadout CfgLoadouts_S3.hpp...')
        # remove mission controller immortality
        x = getMissionData('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld),'    preLoadout = " \\')
        replace('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld), x, '')
        x = getMissionData('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld),'    [(_this select 0), \'s3\', 2, 2, true] call cScripts_fnc_setPreInitPlayerSettings;')
        replace('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld), x, '    preLoadout = "[(_this select 0), \'s3\', 2, 2, true] call cScripts_fnc_setPreInitPlayerSettings;";\n')
        x = getMissionData('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld),'    (_this select 0) allowDamage false;";')
        replace('{}\\cScripts\\Loadouts\\CfgLoadouts_S3.hpp'.format(newWorld), x, '')

        print('Setting world spawn in mission.sqm...')
        # set spawn postion
        x = getMissionData('{}\\mission.sqm'.format(newWorld), 'position[]={20.200001,25.200001,20.200001};')
        spawn = WORLDLIST_XYZ[len(islandList)]
        spawn_X = spawn[0]
        spawn_Y = spawn[1]
        spawn_Z = spawn[2]
        replace('{}\\mission.sqm'.format(newWorld), x, '\t\t\t\tposition[]={{{},{},{}}};\n'.format(spawn_X,spawn_Y,spawn_Z))
        print('Spawn is moved to {},{},{}'.format(spawn_X,spawn_Y,spawn_Z))

        # Pack missions to pbo
        print('Making 7cav_zeus_sandbox_v{}.{}.pbo'.format(VERSION_DIR,world))
        #subprocess.call(PBOPACKINGTOOL.format(projectPath,newWorld), stdout=open(os.devnull, 'wb'))
        subprocess.run('armake build -f -p {0} {0}.pbo"'.format(newWorld))
        islandList.append('{0}.pbo'.format(newWorld))

        #removing dir
        time.sleep(1)
        shutil.rmtree('{}'.format(newWorld))
        print('{} is done.'.format(world))

    print('All {} missions are created'.format(len(islandList)))

if __name__ == "__main__":
    sys.exit(main())
