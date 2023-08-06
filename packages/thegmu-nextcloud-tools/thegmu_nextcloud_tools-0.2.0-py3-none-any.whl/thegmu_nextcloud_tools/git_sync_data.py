#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    git_sync_data.py
    ~~~~~~~~~~~~~~~~

    Class designed specific for TheGMUNextCloudGitSync.

    #. Tracks the files and directories to sync.
    #. File and directory methods such as md5sum calculations.

"""


import hashlib
import os
import re
import time


class GitSyncDataException:
    "GitSyncData: exceptions specific to the GitSyncData module."""


class GitSyncData():
    """GitSyncData: files, directories and methods to sync git and nextcloud data."""

    def __init__(self):
        """self.sync_data initialize as None.

        sync_data is a dictionary holding file and directory listings.

        """

        self.sync_data = None

    def __getitem__(self, key):
        """Convenience for dereferencing the class as the data itself."""
        if ((not self.sync_data) or (key not in self.sync_data)):
            raise KeyError(key)
        return self.sync_data[key]

    def __setitem__(self, key, value):
        """Convenience for dereferencing the class as the data itself."""
        if ((not self.sync_data) or (key not in self.sync_data)):
            raise KeyError(key)
        self.sync_data[key] = value

    @staticmethod
    def get_current_seconds():
        """The epoch seconds returned as integer value."""
        return int(time.time())

    @staticmethod
    def get_files_exclude_regex(exclude_dirs):
        """regex: compile list of exclude dirs to one expression to match."""
        if (exclude_dirs is None):
            return None
        exclude_dirs = [r'''/%s(/|$)''' % x for x in exclude_dirs]
        exclude_match_str = '|'.join(exclude_dirs)
        exclude_match_str = "(%s)" % exclude_match_str
        exclude_re = re.compile(exclude_match_str)
        return exclude_re

    @staticmethod
    def get_files_include_regex(root_dir, include_dirs):
        """regex: compile list of include dirs to one expression to match."""
        if (include_dirs is None):
            return None
        include_dirs = [os.path.join(root_dir, x) for x in include_dirs + []]
        include_match_str = '|'.join(include_dirs)
        include_re = re.compile(include_match_str)
        return include_re

    def get_directory_files(
            self,
            root_dir,
            include_dirs=None,
            exclude_dirs=None):
        """Use os.walk to recursively get all directory files using include/exclude lists"""
        dir_files = []
        exclude_re = self.get_files_exclude_regex(exclude_dirs)
        include_re = self.get_files_include_regex(
            root_dir, include_dirs)

        for dir_data in os.walk(root_dir):
            if (((include_dirs is None) or
                 (include_re.match(dir_data[0]))) and
                    ((exclude_re is None) or
                     (not exclude_re.search(dir_data[0])))):
                dirpath = dir_data[0][len(root_dir) + 1:]
                for filename in dir_data[2]:
                    # BUG: symlinks pointing to removed files.
                    # NextCloud will not host sym links.
                    relative_path = os.path.join(dirpath, filename)
                    full_path = os.path.join(root_dir, relative_path)
                    if not os.path.islink(full_path):
                        dir_files.append(relative_path)
        return list(dir_files)

    def get_directories(self, root_dir, include_dirs=None, exclude_dirs=None,
                        empty_only=False):
        """os.walk with filter to only return directories.

        :param empty_only: filter that specifies to only return empty directories.
            The empty_only use case represents removal of directories in
            NextCloud not found in Git.
        """
        dirs = []
        empty_file_dirs = []
        exclude_re = self.get_files_exclude_regex(exclude_dirs)
        include_re = self.get_files_include_regex(
            root_dir, include_dirs)

        for dir_data in list(os.walk(root_dir))[1:]:
            if (((include_dirs is None) or
                 (include_re.match(dir_data[0]))) and
                    ((exclude_re is None) or
                     (not exclude_re.search(dir_data[0])))):
                dirpath = dir_data[0][len(root_dir) + 1:]
                empty_test = dir_data[1] + dir_data[2]
                if ((empty_only is False) or
                        (len(empty_test) == 0)):
                    dirs.append(dirpath)
                if (len(dir_data[2]) == 0):
                    empty_file_dirs.append(dirpath)

        return dirs

    @staticmethod
    def get_md5sum(md5sum_file):
        """Python md5sum checksum for file similarity comparison.

        .. admonition:: Keep In Mind

            GIT repositories are not designed for large binary files.
            Audio, video, and images are generally not suitable for GIT.
            Therefore files are slurped into main memory.

        :param md5sum_file: any file that fits in memory.

        """
        with open(md5sum_file, 'rb',) as md5sum_fh:
            return hashlib.md5(md5sum_fh.read()).hexdigest()

    def get_sync_elapsed_seconds(self):
        """Elapsed seconds since setting self.sync_data['start_seconds']"""
        return self.get_current_seconds() - self.sync_data['start_seconds']

    def init_sync_data(self):
        """init_sync_data when processing data only.

        sync_data is a dictionary holding file and directory listings.

        """
        self.sync_data = {
            'errors': None,
            'file_nextcloud_md5sum': None,
            'file_sync_md5sum': None,
            'file_sync_reason': None,
            'files_davfs_errors': None,
            'files_nextcloud': None,
            'files_processed': None,
            'files_sync': None,
            'files_to_delete': None,
            'files_to_copy': None,
            'start_seconds': None,
        }

    def set_file_md5sum(self, dir_class, root_dir):
        """set_file_md5sum: set the md5sum for all files in root_dir.

        Only call this after all the files for the class of directory
        have been set, either all the nextcloud or git files.

        Files for both classes are filtered based upon the include
        and exclude lists of each class.

        :param dir_class: One of (nextcloud, sync).
        :param root_dir: os.path.join(root_dir, file path) == absolute path.

        """

        assert (dir_class in ('nextcloud', 'sync'))
        file_list_attr_name = 'files_' + dir_class
        file_md5sum_attr_name = 'file_' + dir_class + '_md5sum'

        self.sync_data[file_md5sum_attr_name] = dict()

        for md5sum_file in self.sync_data[file_list_attr_name]:
            self.sync_data[file_md5sum_attr_name][md5sum_file] = self.get_md5sum(
                os.path.join(root_dir, md5sum_file))

    def set_files_nextcloud(self, nextcloud_dir, include_dirs, exclude_dirs):
        """Call get_directory_files() on the configured NextCloud dir."""
        self.sync_data['files_nextcloud'] = self.get_directory_files(
            nextcloud_dir, include_dirs, exclude_dirs)

    def set_files_sync(self, sync_dir, include_dirs, exclude_dirs):
        """Call get_directory_files() on the configured git sync dir."""
        self.sync_data['files_sync'] = self.get_directory_files(
            sync_dir, include_dirs, exclude_dirs)

    def set_files_to_copy(self, nextcloud_dir, git_dir):
        """Determine files in GIT that have been added or changed
        relative to nextcloud.

        #: If the file in git has changed (md5sum) then replace it.
        #: The Tranfer directory files were already excluded.
        #: Set a reason for any file processed as NEW or DIFF.
        #: TODO: put the reasons in the config file.

        :param nextcloud_dir: root nextcloud directory.
        :param git_dir: root git sync directory.

        """
        self.sync_data['files_to_copy'] = []
        if self.sync_data['file_sync_reason'] is None:
            self.sync_data['file_sync_reason'] = dict()

        for file_sync in self.sync_data['files_sync']:
            if ((file_sync not in self.sync_data['files_nextcloud']) or (
                    self.sync_data['file_sync_md5sum'][file_sync] != self.sync_data['file_nextcloud_md5sum'][file_sync])):
                if (file_sync not in self.sync_data['files_nextcloud']):
                    self.sync_data['file_sync_reason'][file_sync] = "NEW"
                else:
                    nextcloud_size = os.stat(
                        os.path.join(nextcloud_dir, file_sync)).st_size
                    git_size = os.stat(os.path.join(
                        git_dir, file_sync)).st_size
                    self.sync_data['file_sync_reason'][file_sync] = "DIFF(%s!=%s)" % (
                        nextcloud_size, git_size)
                self.sync_data['files_to_copy'].append(file_sync)

    def set_files_to_delete(self):
        """Determine files in nextcloud that have been addded
        relative to GIT and delete them.

        #: If the file is in NextCloud but not git, delete it.
        #: Set a reason for any file processed as CLOUD UPLOAD.
        #: TODO: put the reasons in the config file.

        """
        self.sync_data['files_to_delete'] = []
        if self.sync_data['file_sync_reason'] is None:
            self.sync_data['file_sync_reason'] = dict()
        for file_nextcloud in self.sync_data['files_nextcloud']:
            if (file_nextcloud not in self.sync_data['file_sync_md5sum']):
                self.sync_data['file_sync_reason'][file_nextcloud] = "CLOUD UPLOAD"
                self.sync_data['files_to_delete'].append(file_nextcloud)

    def set_start_seconds(self):
        """Set Linux epoch start seconds as integer value."""
        self.sync_data['start_seconds'] = self.get_current_seconds()
