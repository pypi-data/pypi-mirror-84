#!/bin/bash

# umount.davfs.thegmu.sh
# 2020/09/23
# BUG: umount is not working, umount.davfs core dumps
# 1. Kill mount.davfs process
# 2. Delete pid.
#
# WARNING: this may not flush writes.

user=`whoami`
script=`basename $0`

if [ "$1" == "" ]; then
    echo "Usage: $script /path/to/umount"
    exit 0
fi

if [ "$user" != "root" ]; then
    echo "$script $1: $script failed: Operation not permitted."
    exit -1
fi

DAVFS_PID_DIR=/var/run/mount.davfs/


#sudo mount -t davfs https://www.thegmu.com/oc/remote.php/dav/files/gmucorp/ /media/davfs/gmucorp
#/sbin/mount.davfs: found PID file /var/run/mount.davfs/media-davfs-gmucorp.pid.
#Either /media/davfs/gmucorp is used by another process,
# or another mount process ended irregular
mount_pid_file=${1//[\/]/-}
mount_pid_file=${mount_pid_file:1}
mount_pid_file=${mount_pid_file%-}
mount_pid_file="${mount_pid_file}.pid"
mount_pid_file=${DAVFS_PID_DIR}$mount_pid_file

echo "mount_pid_file: $mount_pid_file"

umount "$1"

if [ -f "$mount_pid_file" ]; then
    echo "umount failed, pid file found."
    mount_pid=$(head -n 1 "$mount_pid_file")
    echo "PID file found: $mount_pid_file, PID $mount_pid"
    echo "Killing process and removing pid file."
    kill -9 $mount_pid
    sleep 1
    umount -f "$1" 2>/dev/null
    /bin/rm -f "$mount_pid_file"
    exit 0
else
    exit 0
fi

exit -1
