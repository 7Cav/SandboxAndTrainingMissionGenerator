#!/bin/bash

set -e

echo "Checking and downloading latest version of cScripts..." 
TAG=$(curl -fs "https://api.github.com/repos/7Cav/cScripts/releases/latest" | \
    grep '"tag_name":' | \
    sed -E 's/.*"([^"]+)".*/\1/')

for i in 1 2 3 4 5; do
    curl -sOL "https://github.com/7Cav/cScripts/releases/download/$TAG/cScripts-$TAG.zip" && break || sleep 15
done



python3 build.py -b sandbox -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y --color
# python3 build.py -b training -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y --color
