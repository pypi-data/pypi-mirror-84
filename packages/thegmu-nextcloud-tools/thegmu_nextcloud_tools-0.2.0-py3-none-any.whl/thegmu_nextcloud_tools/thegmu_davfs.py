#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    thegmu_davfs.py
    ~~~~~~~~~~~~~~~

    The TheGMUNextCloudGitSync davfs object.

    #. Mount as root only for security purposes.
       Directory is not accessible by anyone other than root.
    #. Accomodate quirks with davfs.
    #. Primary usage is to sync files between a remote server and local
       server. Therefore the APIs copy and delete using root directories
       being sync'ed.

    .. note::

        Don't use Linux rsync with davfs for gigabyte or larger copies.
        This object times out after 30 seconds due to vagaries of DavFS
        and nextCloud processing speeds.

"""

import os

from thegmu_nextcloud_tools import script


class TheGMUDavFS():
    """DavFS mount/umount and copy."""

    MOUNT_CMD = """mount -t davfs %s %s < /dev/null"""
    UMOUNT_CMD = """umount %s"""
    SUDO = True

    def __init__(self, url, mount_dir, thegmu_log=None, verbose=False):
        """All configuration of DavFS exists in the TheGMUNextCloudGitSync Object.
        This is all we need.

        :param url: The DavFS URL.
        :param dir: The mount point for url.
        :param sudo: run commands as sudo.
        :param thegmu_log: a class THEGMULog logger.
        :param verbose: if thegmu_log is passed and verbose is True then log.

        """

        self.mount_dir = mount_dir
        self.mount_cmd = self.MOUNT_CMD
        self.sudo = self.SUDO
        self.thegmu_log = thegmu_log
        self.umount_cmd = self.UMOUNT_CMD
        self.url = url
        self.verbose = (thegmu_log is not None) and verbose

    def davfs_copy(self, dav_root, copy_dir, copy_path):
        """Copy file 'copy_dir/copy_path' from local disk to a mounted DavFS directory.
        The file in DavFS will have the same relative path as copy_path.
        We rely on Linux commands because we haven't tested the reliablity of the Pyhthon libraries
        and this needs to be done by root.
        """

        dav_copy_dir = os.path.join(dav_root, os.path.dirname(copy_path))
        if (not os.path.exists(dav_copy_dir)):
            cmd = self.make_sudo("mkdir -p '%s'" % dav_copy_dir)
            script.runcmd(cmd, console=self.verbose)
        cmd = self.make_sudo("/bin/cp -f '%s' '%s' " % (os.path.join(
            copy_dir, copy_path), os.path.join(dav_root, copy_path)))
        script.runcmd(cmd, console=self.verbose)

    def davfs_delete(self, dav_root, delete_path):
        """Delete a file 'dav_root/delete_path' from a mounted DavFS directory.
        We rely onLinux commands because we haven't tested the reliablity of the Pyhthon libraries
        and this needs to be done by root. """

        delete_path = os.path.join(dav_root, delete_path)
        if (os.path.isdir(delete_path)):
            rm_cmd = "/bin/rmdir"
        else:
            rm_cmd = '/bin/rm -f'
        cmd = self.make_sudo("""%s '%s' """ % (rm_cmd, delete_path, ))
        script.runcmd(cmd, console=self.verbose)

    def davfs_mount(self):
        """
        root mount a davfs mount point.

        .. note::

            Credentials need to be set already in /etc/davfs/secrets.
        """

        cmd = self.make_sudo(self.mount_cmd % (self.url, self.mount_dir))

        script.runcmd(cmd, console=self.verbose)

    def davfs_unmount(self, fail_okay=False, console=True):
        """umount a davfs mount point."""

        cmd = self.make_sudo(self.umount_cmd % self.mount_dir)

        script.runcmd(
            cmd,
            console=console,
            exception_continue=fail_okay)

    def delete_files(self, dav_root, files_to_delete):
        """Delete files in 'files_to_delete', paths must be relative to dav_root."""
        for file_to_delete in files_to_delete:
            self.davfs_delete(dav_root, file_to_delete)

    def make_sudo(self, cmd):
        """Append sudo to a string."""
        if (self.sudo):
            return "sudo " + cmd
        return cmd

    def up_check_or_exit(self):
        """
        Ensure the nextCloud DavFS service is available.
        The program exits if the server is not up.
        """
        self.davfs_unmount(fail_okay=True, console=self.verbose)
        self.davfs_mount()
        self.davfs_unmount(fail_okay=False, console=self.verbose)
