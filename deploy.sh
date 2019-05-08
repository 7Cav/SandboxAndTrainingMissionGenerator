#!/bin/bash

set -e

TAG=$(curl --silent "https://api.github.com/repos/7Cav/cScripts/releases/latest" | \
    grep '"tag_name":' | \
    sed -E 's/.*"([^"]+)".*/\1/')
curl -sOL "https://github.com/7Cav/cScripts/releases/download/$TAG/cScripts-$TAG.zip"

python3 build.py -b sandbox -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y
python3 build.py -b training -p cScripts-$TAG.zip -vu ${TRAVIS_TAG} -y
