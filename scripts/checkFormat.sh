#!/bin/bash

SCRIPTPATH=`dirname $(readlink -f $0)`
cd $SCRIPTPATH/..

settings_files=$(find -name "*.json")
has_error=0
for file in $settings_files; do
    echo "CHECKING '$file'"
    jq -c . $file >/dev/null 2>&1
    if [[ $? != "0" ]]; then
        echo " > FAILED"
        has_error=1
    else
        echo " > SUCCESS"
    fi
done
exit $has_error