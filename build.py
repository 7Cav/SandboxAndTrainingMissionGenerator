#!/usr/bin/env python3
import sys, os, shutil, subprocess, time
import argparse, tempfile, zipfile, fileinput, json
startTime = time.time()

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

parser.add_argument('buildtype',
    choices=['sandbox', 'training'],
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
PACKAGE = args.package
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
    print('Building and compiling {}...'.format(color_string('{}.pbo'.format(pbo_name),'\033[96m',use_color)))
    subprocess.call('armake build -f -p "{}" "output/{}.pbo"'.format(temp_folder,pbo_name), shell=True)


def build_archive(archive_name='unnamed', archive_type='zip', archive_input='', use_color=False):
    print('Archiving all generated mission files...')
    archive_output = '{}/{}'.format(releaseDir,archive_name)
    shutil.make_archive(archive_output, archive_type, archive_input)
    fullarchname = color_string('{}.{}'.format(archive_name,archive_type),'\033[96m',use_color)
    print('{} have been created...'.format(fullarchname))


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
    print('Installing script package {}...'.format(color_string(script_package,'\033[96m',use_color)))
    script_package_full_path = '{}/{}'.format(scriptDir,script_package)
    try:
        scriptsArchive = zipfile.ZipFile(script_package_full_path, 'r')
    except:
        sys.exit("Could not locate script package in the root directory...")
    scriptsArchive.extractall(temp_path)
    scriptsArchive.close()


def replace(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def additions(file, additions=[]):
    with open(file, 'a') as add:
        add.write('\n')
        for line in additions:
            add.write('\n{}'.format(line))
    add.close()


def json_macro_replace(obj):
    if type(obj) == str:
        if '$0' in obj:
            return obj.replace('$0', '{}'.format(VERSION))
        if '$1' in obj:
            return obj.replace('$1', '{}'.format(PACKAGE))
    elif type(obj) == list:
        new_list = []
        for line in obj:
            line = line.replace('$0', '{}'.format(VERSION))
            line = line.replace('$1', '{}'.format(PACKAGE))
            new_list.append(line)
        return new_list
    else:
        sys.exit('ERROR: JSON macro function can\'t handle input...')

def clean_mission_folder(temp_folder=''):
    os.chdir(temp_folder)
    remove_list = ['README.md', 'setup.json', 'Data/MissionLogo.psd']
    for f in remove_list:
        try:
            os.remove(f)
        except:
            pass

def cleanup_output():
    print('Cleaning up output folder...')
    output_list = os.listdir(outputDir)
    os.chdir(outputDir)
    for f in output_list:
        os.remove(f)
    os.chdir(scriptDir)


def setup_missions(temp_folder='', sandbox_json_data={}, count=0, use_color=False):
    os.chdir(temp_folder)

    if args.buildtype == 'sandbox':
        world_spawn_list = []
        for world in sandbox_json_data['worlds']:
            world_spawn_list.append(sandbox_json_data['worlds'][world])

        spawn = world_spawn_list[count]

    # Reset common variable
    changes = ''
    filename = 'mission.sqm'
    file = '{}/{}'.format(temp_folder,filename)
    if filename in sandbox_json_data and os.path.isfile(file):
        print('Applying adjustmetns to {}...'.format(color_string(filename,'\033[96m',use_color)))
        
        # Spawn
        if args.buildtype == 'sandbox':
            print('Spawn set to {}, {}, {} on {}.'.format(color_string(spawn[0],'\033[92m',use_color), color_string(spawn[1],'\033[92m',use_color), color_string(spawn[2],'\033[92m',use_color), color_string(world,'\033[92m',args.color)))
            replace(file,
                'position[]={20.200001,25.200001,20.200001};',
                'position[]={{{},{},{}}};'.format(spawn[0],spawn[1],spawn[2]))
        
        for changes in sandbox_json_data[filename]:
            string = sandbox_json_data[filename][changes] 
            string = json_macro_replace(string)

            if 'briefingName' == changes:
                replace(file,
                'briefingName="Zeus Sandbox Template Mission";',
                'briefingName="{}";'.format(string))

                replace(file,
                'briefingName="Training Template Mission";',
                'briefingName="{}";'.format(string))
                continue

            if 'overviewText' == changes:
                replace(file,
                'overviewText="OverviewText Template Text";',
                'overviewText="{}";'.format(string))
                continue

    else:
        '' if os.path.isfile(file) else sys.exit('ERROR: No {} discoverd something is terrible wrong'.format(color_string(filename,'\033[96m',use_color)))
        print('No changes to {} is defined skipping this step...'.format(color_string(filename,'\033[96m',use_color)))


    # Reset common variable
    changes = ''
    filename = 'description.ext'
    file = '{}/{}'.format(temp_folder,filename)
    if os.path.isfile(file):
        print('Applying adjustmetns to {}...'.format(color_string(filename,'\033[96m',use_color)))
       
        for changes in sandbox_json_data[filename]:
            string = sandbox_json_data[filename][changes] 
            string = json_macro_replace(string)
            
            if changes == 'author':
                replace(file,
                    'dev                 = "1SG Tully.B";',
                    'dev                 = "{}";'.format(string))
                replace(file,
                    'author              = "1SG Tully.B";',
                    'author              = "{}";'.format(string))
                continue

            if changes == 'onLoadName':
                replace(file,
                    'onLoadName          = "MyMissionName";',
                    'onLoadName          = "{}";'.format(string))
                continue

            if changes == 'onLoadMission':
                replace(file,
                    'onLoadMission       = "7th Cavalry - S3 1BN Battle Staff Operation";',
                    'onLoadMission       = "{}";'.format(string))
                continue

            if changes == 'onLoadIntro':
                replace(file,
                    'onLoadIntro         = "S3 1BN Battle Staff Operation";',
                    'onLoadIntro         = "{}";'.format(string))
                continue

            if changes == 'loadScreen':
                replace(file,
                    'loadScreen          = "Data\MissionLogo.paa";',
                    'loadScreen         = "{}";'.format(string))
                continue

            if changes == 'overviewPicture':
                replace(file,
                    'overviewPicture     = "Data\MissionLogo.paa";',
                    'overviewPicture     = "{}";'.format(string))
                continue

            if 'cba_settings_hasSettingsFile':
                replace(file,
                    'cba_settings_hasSettingsFile = 1;',
                    'cba_settings_hasSettingsFile = {};'.format(string))
                continue

            if changes == 'disabledAI':
                replace(file,
                    'disabledAI              = true;',
                    'disabledAI              = {};'.format(string))
                continue

            if changes == 'forceRotorLibSimulation':
                replace(file,
                    'forceRotorLibSimulation = 1;',
                    'forceRotorLibSimulation = {};'.format(string))
                continue

            if changes == 'respawn':
                replace(file,
                    'respawn                = BASE;',
                    'respawn                = {};'.format(string))
                continue

            if changes == 'respawnDelay':
                replace(file,
                    'respawnDelay           = 4;',
                    'respawnDelay           = {};'.format(string))
                continue

            if changes == 'respawnOnStart':
                replace(file,
                    'respawnOnStart         = -1;',
                    'respawnOnStart         = {};'.format(string))
                continue

            if changes == 'add':
                additions(file, string)
                continue

    else:
        print('No changes to {} is defined skipping this step...'.format(color_string(filename,'\033[96m',use_color)))


    # Reset common variable
    changes = ''
    filename = 'init.sqf'
    file = '{}/{}'.format(temp_folder,filename)
    if os.path.isfile(file):
        print('Applying adjustmetns to {}...'.format(color_string(filename,'\033[96m',use_color)))
       
        for changes in sandbox_json_data[filename]:
            string = sandbox_json_data[filename][changes] 
            string = json_macro_replace(string)
            
            if changes == 'add':
                additions(file, string)
                continue

    else:
        print('No changes to {} is defined skipping this step...'.format(color_string(filename,'\033[96m',use_color)))


    # Reset common variable
    changes = ''
    filename = 'cba_settings.sqf'
    file = '{}/{}'.format(temp_folder,filename)
    if os.path.isfile(file):
        print('Applying adjustmetns to {}...'.format(color_string(filename,'\033[96m',use_color)))
       
        for changes in sandbox_json_data[filename]:
            string = sandbox_json_data[filename][changes] 
            string = json_macro_replace(string)

            if changes == 'add':
                additions(file, string)
                continue

    else:
        print('No changes to {} is defined skipping this step...'.format(color_string(filename,'\033[96m',use_color)))


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
            install_script_package(PACKAGE, temp_path, args.color)

            # Setup mission file
            print('Setting up and adjusting sandbox mission file...')
            setup_missions(temp_path, sandbox_data, count, args.color)

            # Cleaning mission from readme and template files.
            clean_mission_folder(temp_path)
            
            # Building PBO
            build_pbo(temp_path, mission_name, args.color)


    if args.buildtype == 'training':
        all_templates = get_templates('training')
        all_templates.remove('setup_template.json')

        sys.exit('No training missions found in "./template/training/"...') if (len(all_templates) == 0) else ''

        for count, world in enumerate(all_templates):
            temp_path = tempfile.mkdtemp()
            
            mission_name = world
            if 'DEVBUILD' in mission_name:
                mission_name = mission_name.replace('DEVBUILD',VERSION)

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
            install_script_package(PACKAGE, temp_path, args.color)

            # get json data
            training_json = '{}/template/training/{}/setup.json'.format(scriptDir,world)
            with open(training_json) as json_file:
                training_json = json.load(json_file)
            
            # Setup mission file
            print('Setting up and adjusting training mission file...')
            setup_missions(temp_path, training_json, count, args.color)

            # Cleaning mission from readme and template files.
            clean_mission_folder(temp_path)

            # Building PBO
            build_pbo(temp_path, mission_name, args.color)

    build_archive('Mission_{}_v{}'.format(args.buildtype, VERSION), 'zip', outputDir, args.color)
    cleanup_output()

    print('Builds complete. ({} seconds)'.format(round(time.time() - startTime, 3)))

if __name__ == "__main__":
    sys.exit(main())

