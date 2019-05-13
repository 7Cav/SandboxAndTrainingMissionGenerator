#!/bin/bash

set -e

echo "Checking for latest version of cScripts..." 
TAG=$(curl --silent "https://api.github.com/repos/7Cav/cScripts/releases/latest" | \
    grep '"tag_name":' | \
    sed -E 's/.*"([^"]+)".*/\1/')
curl -sOL "https://github.com/7Cav/cScripts/releases/download/$TAG/cScripts-$TAG.zip"

if [ -z "$TAG" ]; then
    echo "\$TAG is empty this will cause error soon..."
fi

echo 'Downloaded v$TAG of cScripts (cScripts-$TAG.zip)'

python3 build.py -b sandbox -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y
python3 build.py -b training -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y
