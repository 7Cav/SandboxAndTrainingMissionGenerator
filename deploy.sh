#!/bin/bash

set -e

echo "Checking and downloading latest version of cScripts..." 
TAG=$(curl -fs "https://api.github.com/repos/7Cav/cScripts/releases/latest" | \
    grep '"tag_name":' | \
    sed -E 's/.*"([^"]+)".*/\1/')

for i in 1 2 3 4 5; do
    curl -sOL "https://github.com/7Cav/cScripts/releases/download/$TAG/cScripts-$TAG.zip"
    sleep 3
    if [ -f "cScripts-$TAG.zip" ]; then
        echo cScripts-$TAG.zip successfully downloaded...
        break
    else
        echo Failed to download cScripts-$TAG.zip trying again...
    fi
    sleep 15
done

python3 build.py sandbox -p cScripts-$TAG.zip -v ${TRAVIS_TAG} -y
python3 build.py training -p cScripts-$TAG.zip -v ${TRAVIS_TAG} -y
