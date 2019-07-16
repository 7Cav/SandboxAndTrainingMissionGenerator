#!/bin/bash

set -e

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

python3 build.py sandbox -p cScripts-$PACKAGE_TAG.zip -pv $PACKAGE_TAG -v ${TRAVIS_TAG} -y
python3 build.py training -p cScripts-$PACKAGE_TAG.zip -pv $PACKAGE_TAG -v ${TRAVIS_TAG} -y
