#!/usr/bin/env python3
import sys, os, shutil, subprocess
import argparse, tempfile, zipfile, fileinput, json

__version__ = 3.0

scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)
outputDir = '{}/output'.format(scriptDir)
releaseDir = '{}/release'.format(scriptDir)
templateDir = '{}/template'.format(scriptDir)

# #########################################################################################

parser = argparse.ArgumentParser(
    prog='build',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='This script generates missions.',
    epilog='This build script generates sandboxes or training mapes bases on avalible templates.\nThe tool should be cross platform and can be used for other packages as well.'
)

parser.add_argument('-b', '--buildtype',
    required=False,
    choices=['sandbox', 'training'],
    default='sandbox',
    help='This defines what kind of generation the script should commit.'
)

parser.add_argument('-p', '--package',
    required=True,
    help='This defines what script package to install.'
)

parser.add_argument('-v', '--versionTag',
    required=True,
    help='This define what version name you whant the file to have.'
)

parser.add_argument("-y", "--fastbuild",
    help="Will instantly run untill done.",
    action="store_false"
)
parser.add_argument('--color',
    help='Enable colors in the script.',
    action='store_true'
)

parser.add_argument('--version', action='version', version='Author: Andreas Broström <andreas.brostrom.ce@gmail.com>\nScript version: {}'.format(__version__))

args = parser.parse_args()

# handle arguments

SCRIPT_PACKAGE = args.package

if args.versionTag:
    VERSION = args.versionTag
    VERSION_DIR = args.versionTag.replace('.','_')

# #########################################################################################

def color_string(string='', color='\033[0m', use_color=False):
    if use_color:
        return '\033[0m{}{}\033[0m'.format(color,string)
    else:
        return string


def build_pbo(temp_folder='', pbo_name='unnamed', use_color=False):
    os.chdir(scriptDir)
    print('Compiling {}...'.format(color_string('{}.pbo'.format(pbo_name),'\033[96m',use_color)))
    subprocess.call('armake build -f -p "{}" "output/{}.pbo"'.format(temp_folder,pbo_name), shell=True)


def build_archive(archive_name='unnamed', archive_type='zip', archive_input=''):
    print('Building archive...')
    archive_output = '{}/{}'.format(releaseDir,archive_name)
    shutil.make_archive(archive_output, archive_type, archive_input)
    print('Archive created you can find it in the release folder.')


def check_or_create_folder(dir=''):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_templates(template_type='', world=''):
    if template_type == 'sandbox':
        if os.path.exists('{0}/sandbox/Template_{1}.{1}'.format(templateDir,world)):
            print('Mission files found for {} using them instead of generic...'.format(world))
            return '{0}/sandbox/Template_{1}.{1}'.format(templateDir,world)
        print('Creating mission file with generic template...'.format(world))
        return '{0}/sandbox/Template_Generic.VR'.format(templateDir)
    elif template_type == 'training':
        return os.listdir('{0}/training/'.format(templateDir))
    else:
        sys.exit('ERROR: No valid template defined')


def fetch_objects(template_path=''):
    os.chdir(template_path)
    content = os.listdir(template_path)
    
    objectList = []

    folderList = [] # Collect directories
    fileList = []   # Collect files

    for obj in content:
        if os.path.isfile(obj):
            fileList.append(obj)
        elif os.path.isdir(obj):
            folderList.append(obj)
        else:
            sys.exit('\nIssues occured when listing files.')

    objectList.append(folderList)
    objectList.append(fileList)

    os.chdir(scriptDir)

    return objectList


def install_script_package(script_package, temp_path, use_color=False):
    print('Installing script package {}...'.format(color_string(SCRIPT_PACKAGE,'\033[96m',use_color)))
    script_package_full_path = '{}/{}'.format(scriptDir,script_package)
    try:
        scriptsArchive = zipfile.ZipFile(script_package_full_path, 'r')
    except:
        sys.exit("Could not locate script package in the root directory...".format(SCRIPT_PACKAGE))
    scriptsArchive.extractall(temp_path)
    scriptsArchive.close()


def replace(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def setup_sandbox_missions(temp_folder='', sandbox_json_data={}, count=0, use_color=False):
    print('Setting up and adjusting sandbox mission file...')
    os.chdir(temp_folder)
    if os.path.isfile('{}/description.ext'.format(temp_folder)):
        pass
    else:
        print('No {} detected skipping changes...'.format(color_string('description.ext','\033[96m',use_color)))

    # if os.path.isfile('{}/description.ext'.format(temp_folder)):
    #     print('Applying adjustmetns to {}...'.format(color_string('description.ext','\033[96m',use_color)))
    #     file = '{}/description.ext'.format(temp_folder)
    #     replace(file,
    #         '    dev                 = "1SG Tully.B";',
    #         '    dev                 = "CPL Brostrom.A";')
    #     replace(file,
    #         '    author              = "1SG Tully.B";',
    #         '    author              = "CPL Brostrom.A";')
    #     replace(file,
    #         '    onLoadName          = "MyMissionName";',
    #         '    onLoadName          = "Zeus Sandbox v{}";'.format(VERSION))
    #     replace(file,
    #         '    onLoadMission       = "7th Cavalry - S3 1BN Battle Staff Operation";',
    #         '    onLoadMission       = "7th Cavalry - S3 1BN Battle Staff Sandbox";')
    #     replace(file,
    #         '    onLoadIntro         = "S3 1BN Battle Staff Operation";',
    #         '    onLoadIntro         = "S3 1BN Battle Staff Sandbox";'.format(VERSION))
    #     replace(file,
    #         '    respawnOnStart         = -1;',
    #         '    respawnOnStart         = 1;')

    #     print('Adding new settings to {}...'.format(color_string('cba_settings.sqf','\033[96m',use_color)))
    #     add_new_settings = [
    #         '// cScripts Mission Settings',
    #         'force force cScripts_Settings_allowCustomInit = true;',
    #         'force force cScripts_Settings_allowCustomTagging = true;',
    #         'force force cScripts_Settings_allowInsigniaApplication = true;',
    #         'force force cScripts_Settings_enable7cavZeusModules = true;',
    #         'force force cScripts_Settings_enableStartHint = false;',
    #         'force force cScripts_Settings_enforceEyewereBlacklist = true;',
    #         'force force cScripts_Settings_jumpSimulation = 1;',
    #         'force force cScripts_Settings_jumpSimulationGlasses = true;',
    #         'force force cScripts_Settings_jumpSimulationHat = true;',
    #         'force force cScripts_Settings_jumpSimulationNVG = true;',
    #         'force force cScripts_Settings_setAiSystemDifficulty = 0;',
    #         'force force cScripts_Settings_setCustomHintText = "Be creative!";',
    #         'force force cScripts_Settings_setCustomHintTopic = "Zeus Sandbox v{}";'.format(VERSION),
    #         'force force cScripts_Settings_setMissionType = 3;',
    #         'force force cScripts_Settings_setPlayerRank = true;',
    #         'force force cScripts_Settings_setRadio = true;',
    #         'force force cScripts_Settings_setStartupDelay = 30;',
    #         'force force cScripts_Settings_showDiaryRecords = true;',
    #         'force force cScripts_Settings_useCustomSupplyInventory = false;',
    #         'force force cScripts_Settings_useCustomVehicleInventory = true;',
    #         'force force cScripts_Settings_useCustomVehicleSettings = true;'
    #     ]
    #     with open('{}/cba_settings.sqf'.format(temp_folder), 'a') as settings_file:
    #         settings_file.write('\n')
    #         for line in add_new_settings:
    #             settings_file.write('\n{}'.format(line))
    #     settings_file.close()

    #     print('Removing immortality from S3 loadout {}...'.format(color_string('CfgLoadouts_S3.hpp','\033[96m',use_color)))
    #     file = '{}/cScripts/Loadouts/CfgLoadouts_S3.hpp'.format(temp_folder)
    #     replace(file,
    #         '    (_this select 0) allowDamage false;";',
    #         '    (_this select 0) allowDamage true;";')

    #     print('Adjusting {}...'.format(color_string('mission.sqm','\033[96m',use_color)))
    #     file = '{}/mission.sqm'.format(temp_folder)
    #     print('Adjusting {} and {}...'.format(color_string('overviewText','\033[92m',use_color), color_string('briefingName','\033[92m',use_color)))
    #     replace(file,
    #         '		briefingName="Zeus Sandbox Template Mission";',
    #         '		briefingName="Zeus Sandbox v{}";'.format(VERSION))
    #     replace(file,
    #         '	overviewText="This is the 7th Cavalry Zeus mission template built to be used for user made custom scenarios." \n "Have fun!";',
    #         '	overviewText="This is the 7th Cavalry Zeus Sandbox mission." \n "Have fun!";')
    #     spawn = world_list_XYZ[count]
    #     print('Spawn set to {}, {}, {}.'.format(color_string(spawn[0],'\033[92m',use_color), color_string(spawn[1],'\033[92m',use_color), color_string(spawn[2],'\033[92m',use_color)))
    #     replace(file,
    #         '				position[]={20.200001,25.200001,20.200001};',
    #         '				position[]={{{},{},{}}};'.format(spawn[0],spawn[1],spawn[2]))

    # else:
    #     print('No {} detected skipping changes...'.format(color_string('description.ext','\033[96m',use_color)))


def setup_training_missions():
    print('Setting up and adjusting training mission file...')


def cleanup_output():
    print('Cleaning up output folder...')
    output_list = os.listdir(outputDir)
    os.chdir(outputDir)
    for f in output_list:
        os.remove(f)
    os.chdir(scriptDir)

# #########################################################################################


def main():
    # setup directories if non exist
    check_or_create_folder('release')
    check_or_create_folder('output')
    check_or_create_folder('template/sandbox')
    check_or_create_folder('template/training')

    if args.buildtype == 'sandbox':
        
        # get json data
        sandbox_json = '{}/setup.json'.format(scriptDir)
        with open(sandbox_json) as json_file:  
            sandbox_data = json.load(json_file)

        # get mission name
        sandbox_mission_name = sandbox_data['sandboxMissionName']

        # set up world list
        world_list = []
        for world in sandbox_data['worlds']:
            world_list.append(world)


        for count, world in enumerate(world_list):
            temp_path = tempfile.mkdtemp()
            mission_name = '{}_v{}.{}'.format(sandbox_mission_name, VERSION_DIR, world)

            print('Creating sandbox mission on {}... ({}/{})'.format(color_string(world,'\033[92m',args.color), count+1, len(world_list)))

            template_path = get_templates('sandbox', world)
            content_list = fetch_objects(template_path)
            folder_list = content_list[0]
            file_list = content_list[1]

            os.chdir(template_path)

            for obj in folder_list:
                shutil.copytree(obj, '{}/{}'.format(temp_path, obj))
            for obj in file_list:
                shutil.copy2(obj, temp_path)

            # Unzip and install script package
            install_script_package(SCRIPT_PACKAGE, temp_path, args.color)

            # Setup mission file
            setup_sandbox_missions(temp_path, sandbox_data, count, args.color)

            # Building PBO
            build_pbo(temp_path, mission_name, args.color)


    if args.buildtype == 'training':
        all_templates = get_templates('training')
        sys.exit('No training missions found in "./template/training/"...') if (len(all_templates) == 0) else ''

        for count, world in enumerate(all_templates):
            temp_path = tempfile.mkdtemp()
            mission_name = world
            print('Creating training mission {}... ({}/{})'.format(color_string(world,'\033[92m',args.color), count+1, len(all_templates)))

            template_path = '{}/training/{}'.format(templateDir, world)
            content_list = fetch_objects(template_path)
            folder_list = content_list[0]
            file_list = content_list[1]

            os.chdir(template_path)

            for obj in folder_list:
                shutil.copytree(obj, '{}/{}'.format(temp_path, obj))
            for obj in file_list:
                shutil.copy2(obj, temp_path)

            # Unzip and install script package
            install_script_package(SCRIPT_PACKAGE, temp_path, args.color)

            # Setup mission file
            setup_training_missions(temp_path, count, args.color)

            # Building PBO
            build_pbo(temp_path, mission_name, args.color)

    build_archive('Mission_{}_v{}'.format(args.buildtype, VERSION), 'zip', outputDir)
    cleanup_output()

    print('Builds complete.')

if __name__ == "__main__":
    sys.exit(main())

