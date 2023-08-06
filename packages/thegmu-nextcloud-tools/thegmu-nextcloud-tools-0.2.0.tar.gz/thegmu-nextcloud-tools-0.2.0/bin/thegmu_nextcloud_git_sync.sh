#!/bin/bash

#Ensure thegmu_nextcloud_git_sync.py is in PATH.

#PATH=$PATH:/usr/local/bin

#If running from a virtualenv then use activate.
# . /path/to/your/venv/bin/activate

# crontab:
# THEGMU_CONFIG_DIR="/etc/thegmu"
# THEGMU_OCGS_CONFIG_FILES=gitcloudsync.host.yaml gitcloudsync.youraccount.yaml 

if [ "$THEGMU_CONFIG_DIR" == "" ]; then
    echo ""
    echo "FATAL ERROR: $0 missing environment variable THEGMU_CONFIG_DIR."
    echo ""
    exit -1
fi

if [ "$THEGMU_NEXTCLOUD_CONFIG_FILES" == "" ]; then
    echo ""
    echo "FATAL ERROR $0: missing environment variable THEGMU_NEXTCLOUD_CONFIG_FILES."
    echo ""
    exit -1
fi

for configfile in $THEGMU_NEXTCLOUD_CONFIG_FILES; do
    sudo thegmu_nextcloud_git_sync.py $THEGMU_CONFIG_DIR/$configfile
done
