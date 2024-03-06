#!/bin/sh

set -e

VERSION_TAG=$*

echo "Checking and downloading latest version of cScripts..." 
PACKAGE_TAG=$(curl -fs "https://api.github.com/repos/7Cav/cScripts/releases/latest" | \
    grep '"tag_name":' | \
    sed -E 's/.*"([^"]+)".*/\1/')

for i in 1 2 3 4 5; do
    curl -sOL "https://github.com/7Cav/cScripts/releases/download/$PACKAGE_TAG/cScripts-$PACKAGE_TAG.zip"
    sleep 3
    if [ -f "cScripts-$PACKAGE_TAG.zip" ]; then
        echo cScripts-$PACKAGE_TAG.zip successfully downloaded...
        break
    else
        echo Failed to download cScripts-$PACKAGE_TAG.zip trying again...
    fi
    sleep 15
done

#echo Downloading training missions...
#git clone https://github.com/7Cav/7thCavalry_Training_Missions.git template/training/

python3 build.py sandbox -p cScripts-$PACKAGE_TAG.zip -pv $PACKAGE_TAG -v ${VERSION_TAG} -y
python3 build.py sandbox -s setup_NoRadios.json -o noradio -p cScripts-$PACKAGE_TAG.zip -pv $PACKAGE_TAG -v ${VERSION_TAG} -y

#python3 build.py training -p cScripts-$PACKAGE_TAG.zip -pv $PACKAGE_TAG -v ${VERSION_TAG} -y

mkdir -p server_missions
unzip release/Mission_sandbox_v$VERSION_TAG.zip -d server_missions
unzip release/Mission_sandbox_noradio_v$VERSION_TAG.zip -d server_missions
