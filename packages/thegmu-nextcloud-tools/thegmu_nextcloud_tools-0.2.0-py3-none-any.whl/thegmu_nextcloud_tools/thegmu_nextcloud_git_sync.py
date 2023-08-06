#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    thegmu_nextcloud_git_sync.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~-

    Mirror a git repository as a system for record to dedicated Next Cloud
    account.

    #. Files are virtually read only in that any Next Cloud uploads are
       reverted back to the git versions.
    #. Transfer directory will accept uploads. It is expected that
       Transfer files will be eventually added to the git repository. The
       Transfer directory is designed with a daily or weekly removal of all
       uploads.

"""

import argparse
import csv
import datetime
import getpass
import inspect
import os
import pprint
import re
import shutil
import sys
import yaml

import thegmu_nextcloud_tools
from thegmu_nextcloud_tools import thegmu_log
from thegmu_nextcloud_tools import script
from thegmu_nextcloud_tools.git_sync_data import GitSyncData
from thegmu_nextcloud_tools.thegmu_davfs import TheGMUDavFS


class TheGMUNextCloudGitSyncException:
    "Exceptions specific to this module."""


# pylint: disable=locally-disabled, too-many-public-methods
class TheGMUNextCloudGitSync():
    """Command line script for syncing a Git repo with Next Cloud."""

    TEMPLATE_YAML = 'data/thegmu_nextcloud_git_sync.template.yaml'

    TLA = 'ngs'  # TheGMULog TLA

    USAGE = """
    thegmu_nextcloud_git_sync [-t,--today_report, -y,--yesterday_report, -v,--verbose] thegmu_nextcloud_git_sync.yaml

      Synchronize files between a git repository and an NextCloud installation.
      The git repository and NextCloud directories are specified in a YAML configuration file.

"""

    def __init__(self):

        self.args = None
        self.cfg = None
        self.davfs = None
        self.log = thegmu_log.TheGMULog(self.TLA)
        self.sync_data = None
        self.test_host = False

    def _init_error_file_create(self):
        """Initialize the CSV file with just the headers."""
        with open(self.cfg['report']['file']['error'], 'w') as error_fh:
            error_csv = csv.writer(error_fh)
            error_csv.writerow(self.cfg['report']['error']['columns'])

    def _init_error_file(self):
        """The error file tracks ongoing errors across invocations as this
        script is to be run from cron every minute with thirty second
        time outs.
        """
        if (not os.path.isfile(self.cfg['report']['file']['error'])):
            self._init_error_file_create()

        self.sync_data['errors'] = dict()
        with open(self.cfg['report']['file']['error'], 'r') as error_fh:
            error_csv = csv.DictReader(error_fh)
            for row in error_csv:
                self.sync_data['errors'][row['File']] = row

    def _init_process_file_create(self):
        """Initialize the CSV file with just the headers."""
        with open(self.cfg['report']['file']['process'], 'w') as process_fh:
            process_csv = csv.writer(process_fh)
            process_csv.writerow(self.cfg['report']['error']['columns'])

    def _init_process_file(self):
        """The process file tracks all files processed across invocations as this
        script is to be run from cron every minute with thirty second
        time outs.
        """
        if (not os.path.isfile(self.cfg['report']['file']['process'])):
            self._init_process_file_create()

    def copy_git_files(self, local_test_dir=None):
        """Copy git files to the NextCloud mounted DavFS directory."""

        for file_to_copy in self.sync_data['files_to_copy']:
            if (local_test_dir is None):
                dav_root = self.get_davfs_mount_dir()
            else:
                dav_root = local_test_dir
            git_dir = self.cfg['git']['directory']['root']
            self.davfs.davfs_copy(dav_root, git_dir, file_to_copy)
            if (local_test_dir is None):
                self.sync_data['files_processed'].append(file_to_copy)
            if (self.sync_data.get_sync_elapsed_seconds() >
                    self.cfg['davfs']['mount']['max_active_seconds']):
                if self.args.verbose:
                    self.log.prog("Copy time expired, stopping.")
                break

    def create_template_file(self, file_name_only=False):
        """Copy data/thegmu_nextcloud_git_sync.template.yaml to
        the current directory.

        :param file_name_only: If True return the file name only and do not
            create the file.
        """

        module_dir = os.path.dirname(inspect.getfile(thegmu_nextcloud_tools))

        template_path = os.path.join(module_dir, self.TEMPLATE_YAML)
        host_name = script.get_hostname(host_name_only=True)
        splits = os.path.basename(self.TEMPLATE_YAML).split('.')
        host_path = "%s.%s.%s" % (splits[0], host_name, splits[2])
        if (file_name_only):
            return host_path
        shutil.copy(template_path, host_path)
        self.log.prog("%s file created." % host_path)
        return None

    def _get_empty_dirs(self, dav_root,
                        include_dirs=None, exclude_dirs=None):
        """Intneral function speecific to delete_nextcloud_empty_dirs"""
        delete_dirs = []

        git_dirs = self.sync_data.get_directories(
            self.cfg['git']['directory']['root'],
            include_dirs=include_dirs, exclude_dirs=exclude_dirs)

        dav_dirs = self.sync_data.get_directories(
            dav_root, include_dirs=include_dirs, exclude_dirs=exclude_dirs,
            empty_only=True)
        if (exclude_dirs is not None):
            exclude_re = self.sync_data.get_files_exclude_regex(exclude_dirs)
            dav_dirs = [
                x for x in dav_dirs if (
                    x and not exclude_re.search(
                        os.path.join(
                            dav_root, x)))]
        if (include_dirs is not None):
            include_re = self.sync_data.get_files_include_regex(
                dav_root, include_dirs)
            dav_dirs = [
                x for x in dav_dirs if (
                    x and include_re.search(
                        os.path.join(
                            dav_root, x)))]
        delete_dirs += [x for x in dav_dirs if x not in git_dirs]

        return delete_dirs

    def delete_nextcloud_empty_dirs(
            self,
            dav_root,
            include_dirs=None,
            exclude_dirs=None):
        """delete any empty Next Cloud directories created.
        Returns the number directories deleted.

        :param include_dirs: filter based on a list of dirs to include.
        :param exclude_dirs: filter based on a list of dirs to exclude.

        """
        delete_dirs = \
            self._get_empty_dirs(dav_root, include_dirs,
                                 exclude_dirs)

        if ((len(delete_dirs) > 0) and self.args.verbose):
            self.log.prog("EMPTY directory count: %s" % (len(delete_dirs), ))
            self.log.prog((pprint.pformat(delete_dirs)))

        for dav_dir in delete_dirs:
            self.davfs.davfs_delete(dav_root, dav_dir)

        return len(delete_dirs)

    def delete_nextcloud_files(self, dav_root):
        """Delete any new files from Next Cloud uploads."""
        for file_to_delete in self.sync_data['files_to_delete']:
            self.davfs.davfs_delete(dav_root, file_to_delete)

    def get_davfs_mount_dir(self):
        """
        get_davfs_mount_dir: configuration determined davfs mount directory.
        Test uses a different directory than production.
        """
        dav_dir = self.cfg['davfs']['mount']['target_dir']
        return dav_dir

    def get_ubuntu_version(self):
        """Ubuntu 20 work around for umount seg fault requires version check."""
        result = script.runcmd(
            self.cfg['internal_use_only']['ubuntu_version_cmd'],
            console=False,
            encoding='utf-8',
            exception_continue=True)
        return result.strip(os.linesep)

    @staticmethod
    def _get_mail_report_process_day(process_day=None, previous_day=False):
        """
        day = YYYYMMDD, typically from some existing log or file timestamp.
        1. Today: day=None, previous_day=False
        2. Yesterday: day=None, previous_day=True
        3. Specify day: day='20181231', previous_day=False
        4. Specify day before: day='20181231', previous_day=True
        """
        assert ((process_day is None) or
                ((len(process_day) == 8) and
                 re.match(r'''\d{8}$''', process_day))),\
            ("%s: invalid day format, expecting day format 'YYYYMMDD'." %
             (process_day, ))

        if (process_day is None):
            process_date = datetime.date.today()
        else:
            process_date = datetime.date(int(process_day[:4]), int(
                process_day[4:6]), int(process_day[6:]))

        if (previous_day is True):
            previous_day_delta = datetime.timedelta(days=1)
            process_date = process_date - previous_day_delta

        return str(process_date).replace('-', '')

    def get_mail_report(self, day=None, previous_day=False, config_file=None):
        """This will create a text buffer listing all the errors and
        processed files for a day. Specify previous_day as True to
        run after midnight for the previous day.
        1. Report all errors first.
        2. Report processed files of specified day only.
        3. 20190308 is date format.
        """
        if (self.args is None):
            if (config_file is None):
                self.init_args()
            else:
                self.init_args([config_file, ])

        self.init_cfg()

        process_day = self._get_mail_report_process_day(day, previous_day)

        with open(self.cfg['report']['file']['error'], 'r') as pe_fh:
            report_errors = pe_fh.readlines()[1:]
        with open(self.cfg['report']['file']['process'], 'r') as pp_fh:
            report_processed = [
                x for x in pp_fh.readlines() if (
                    x.find(
                        process_day + ':') > -1)]

        if self.args.verbose:
            self.log.prog("report_processed: %s" % (report_processed, ))
        report = "No file errors and no files processed."
        if ((not report_errors) and (not report_processed)):
            return report

        report = ""
        if (report_errors):
            report += os.linesep + "Errors:" + os.linesep
            report += ''.join(report_errors)

        if (report_processed):
            report += os.linesep + "Processed:" + os.linesep
            report += ''.join(report_processed)

        return report

    def _git_pull_upstream_test(self):
        """Ensure the git repo has an upstream before pulling."""
        upstream_key = self.cfg['git']['config']['upstream_test_key']
        git_cmd = self.cfg['git']['config']['upstream_test_cmd']
        git_cmd = git_cmd % (self.cfg['git']['account']['linux'],
                             self.cfg['git']['directory']['root'],
                             upstream_key,)
        result = script.runcmd(git_cmd, console=False,
                               exception_continue=True,
                               encoding='utf-8')
        return(len(result) > 1)

    def git_pull_nextcloud(self):
        """ use sudo -c and execute the command as the designated user."""
        if (not self._git_pull_upstream_test()):
            self.log.warn("%s git repo has no upstream to pull." %
                          (self.cfg['git']['directory']['root'], ))
            return

        git_pull_cmd = self.cfg['git']['pull_cmd'] % (
            self.cfg['git']['account']['linux'], self.cfg['git']['directory']['root'])
        script.runcmd(git_pull_cmd, console=self.args.verbose)

    def init_args(self, argv=None):
        """argparse.ArgumentParser

        :param argv: If None then sys.argv is used.
            Passing this parameter is for testing purposes.

        """
        if (argv is None):
            argv = sys.argv
        parser = argparse.ArgumentParser(
            description=TheGMUNextCloudGitSync.USAGE,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            '-c',
            '--create_template',
            action='store_true',
            help="""Create a YAML configuration file in the current directory.""")
        parser.add_argument(
            '-t',
            '--today_report',
            action='store_true',
            help="""Do not sync, instead output a report of today's sync. """)
        parser.add_argument(
            '-y',
            '--yesterday_report',
            action='store_true',
            help="""Do not sync, instead output a report of yesterday's sync. """)
        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help="""Output status messages.""")

        if (not re.search(r'''[ -]?-c''', ' '.join(argv))):
            parser.add_argument(
                'yaml',
                type=str,
                help="thegmu_nextcloud_git_sync.yaml configuration file.")

        self.args = parser.parse_args(args=argv)

    def _init_cfg_defaults(self):
        """Default values supplied when an expected value is null."""
        if (self.cfg['git']['account']['linux'] is None):
            self.cfg['git']['account']['linux'] = getpass.getuser()

        self.cfg['git']['directory']['root'] = \
            os.path.realpath(self.cfg['git']['directory']['root'])

    def init_cfg(self, program_config_file=None):
        """init_cfg: load the YAML configuration file or die trying."""
        if (program_config_file is None):
            program_config_file = self.args.yaml
        if os.path.isfile(program_config_file):
            with open(self.args.yaml, 'r', encoding='utf8') as cfg_fh:
                self.cfg = yaml.load(cfg_fh, Loader=yaml.SafeLoader)
        else:
            raise IOError(
                "%s: configuration file not found." %
                (program_config_file, ))

        self._init_cfg_defaults()
        hostname = script.get_hostname(host_name_only=True)
        if (self.cfg['run']['production_host'] != hostname):
            self.test_host = True

    def init_davfs(self):
        """Init DavFS with command line args."""
        self.davfs = TheGMUDavFS(self.cfg['davfs']['mount']['source_url'],
                                 self.cfg['davfs']['mount']['target_dir'],
                                 thegmu_log=self.log,
                                 verbose=self.args.verbose)

        if (('internal_use_only' in self.cfg) and
            ('mount_cmd' in self.cfg['internal_use_only']) and
                self.cfg['internal_use_only']['mount_cmd']):
            self.davfs.mount_cmd = self.cfg['internal_use_only']['mount_cmd']

        ubuntu_version = self.get_ubuntu_version()
        fail_versions = self.cfg['internal_use_only']['umount_ubuntu_version_fails']

        if (str(ubuntu_version) in fail_versions):
            self.davfs.umount_cmd = self.cfg['internal_use_only']['umount_cmd_ubuntu20']
            self.log.warn(
                "Ubuntu %s umount.davfs seg fault workarouond applied." %
                self.davfs.umount_cmd)

    def init_sync(self):
        """init_sync_data and output files."""
        self.sync_data = GitSyncData()
        self.sync_data.init_sync_data()
        self._init_error_file()
        self._init_process_file()

    def init(self, argv):
        """init_args, init_davfs, init_cfg, init_sync"""
        self.init_args(argv)
        self.init_cfg()
        self.init_davfs()
        self.init_sync()

    def run_step_copy_files(self):
        """Step 7: Copy files with a 30 second time check."""
        self.copy_git_files()

        # Test step: if not the production host then copy to the
        # test cirectory.
        hostname = script.get_hostname(host_name_only=True)
        if (self.cfg['run']['production_host'] != hostname):
            self.copy_git_files(self.cfg['nextcloud']['directory']['root'])

    def run_step_delete(self):
        """Step 6: Delete files and dirs in NextCloud without any time limit."""

        dav_root = self.get_davfs_mount_dir()
        self.delete_nextcloud_files(dav_root)
        self.sync_data['files_processed'] += self.sync_data['files_to_delete']

        # Test step: if not the production host then copy to the
        # test cirectory.

        if self.args.verbose:
            self.log.prog("GIT doesn't allow empty directories.")
            self.log.prog("Delete empty NextCloud directories. ")

        delete_count = self.delete_nextcloud_empty_dirs(
            dav_root,
            include_dirs=self.cfg['git']['directory']['include'],
            exclude_dirs=self.cfg['git']['directory']['exclude'])

        while(delete_count > 0):
            delete_count = self.delete_nextcloud_empty_dirs(
                dav_root,
                include_dirs=self.cfg['git']['directory']['include'],
                exclude_dirs=self.cfg['git']['directory']['exclude'])

        if (self.test_host):
            self.delete_nextcloud_files(
                self.cfg['nextcloud']['directory']['root'])
            delete_count = self.delete_nextcloud_empty_dirs(
                self.cfg['nextcloud']['directory']['root'],
                include_dirs=self.cfg['git']['directory']['include'],
                exclude_dirs=self.cfg['git']['directory']['exclude'])
            while(delete_count > 0):
                delete_count = self.delete_nextcloud_empty_dirs(
                    self.cfg['nextcloud']['directory']['root'],
                    include_dirs=self.cfg['git']['directory']['include'],
                    exclude_dirs=self.cfg['git']['directory']['exclude'])

    def run_step_git_pull(self):
        """Step 1. GIT pull source directory."""

        self.git_pull_nextcloud()

    def run_step_init(self, argv):
        """Start a new synchronization run."""
        self.init(argv)

        script.initlock(self.cfg['run']['lockpath'])

        if self.args.verbose:
            self.log.prog("%s configuration:" % (self.__module__))
            self.log.prog(pprint.pformat(self.cfg))
            script.print_dashes(
                "Server UP check using DavFS mount/umount check of NextCloud server.")

        """Ensure DavFS is working and the cloud server is up."""
        self.davfs.up_check_or_exit()

    def run_step_set_copy_files(self):
        """
        Step 5. Set the git files to copy either because
        they are new or the md5sums are different.
        """
        self.sync_data.set_files_to_copy(
            self.cfg['nextcloud']['directory']['root'],
            self.cfg['git']['directory']['root'])

        if self.args.verbose:
            copy_list = ["COPY %s: %s" % (
                self.sync_data['file_sync_reason'][x], x)
                for x in self.sync_data['files_to_copy']]
            self.log.prog("COPY   file count: %s" % (len(copy_list), ))
            if (len(copy_list) > 0):
                self.log.prog(pprint.pformat(copy_list))

    def run_step_set_delete_files(self):
        """Step 4. Set the NextCloud files for delete that are not found in git."""
        self.sync_data.set_files_to_delete()
        if self.args.verbose:
            delete_list = ["DELETE %s: %s" % (
                self.sync_data['file_sync_reason'][x], x)
                for x in self.sync_data['files_to_delete']]
            self.log.prog("DELETE file count: %s" % (len(delete_list), ))
            if (len(delete_list) > 0):
                self.log.prog(pprint.pformat(delete_list))

    def run_step_set_git_files(self):
        """Step 2. Set sync files using white list of top level directories
        and black list of exclusion directories like ".git". Then set the md5sums.
        """
        self.sync_data.set_files_sync(self.cfg['git']['directory']['root'],
                                      self.cfg['git']['directory']['include'],
                                      self.cfg['git']['directory']['exclude'])
        if self.args.verbose:
            if (len(self.sync_data['files_sync']) > 0):
                self.log.prog("%s source files to sync." %
                              (len(self.sync_data['files_sync']), ))
                self.log.prog(pprint.pformat(self.sync_data['files_sync']))
            else:
                self.log.prog("%s no files found to sync." %
                              (self.cfg['git']['directory']['root'], ))

        self.sync_data.set_file_md5sum(
            'sync', self.cfg['git']['directory']['root'])

    def run_step_set_nextcloud_files(self):
        """
        Step 3. Set existing NextCloud files to all
        the files except those excluded.
        """
        self.sync_data.set_files_nextcloud(
            self.cfg['nextcloud']['directory']['root'],
            self.cfg['nextcloud']['directory']['include'],
            self.cfg['nextcloud']['directory']['exclude'])
        self.sync_data.set_file_md5sum(
            'nextcloud', self.cfg['nextcloud']['directory']['root'])

    def run_step_validate_files(self):
        """Step 8: Validate, need to flush the DavFS cache first."""
        self.davfs.davfs_unmount(fail_okay=True, console=self.args.verbose)
        self.davfs.davfs_mount()
        self.validate_nextcloud_files()

    def run_step_write_files(self):
        """Step 9: write output files."""
        self.write_errors()
        self.write_processed_files()

    def run(self, argv=None):
        """run: sync Next Cloud with Git step by step."""

        self.run_step_init(argv)

        if self.args.verbose:
            script.begin()

        """Step 1. GIT pull source directory."""
        self.run_step_git_pull()

        """Step 2. Set sync files using white list of top level directories
        and black list of exclusion directories like ".git". Then set the md5sums.
        """
        self.run_step_set_git_files()

        """Step 3. Set existing NextCloud files except those excluded, git is the sytem of record"""
        self.run_step_set_nextcloud_files()

        """Step 4. Set the NextCloud files for delete that are not found in git."""
        self.run_step_set_delete_files()

        """Step 5. Set the git files to copy either because they are new or the md5sums are different."""
        self.run_step_set_copy_files()

        """Start to process files."""
        self.sync_data.set_start_seconds()
        self.sync_data['files_processed'] = []
        self.davfs.davfs_mount()

        """Step 6: Delete files and dirs in NextCloud with no time check."""
        self.run_step_delete()

        """Step 7: Copy files with a 30 second time check."""
        self.run_step_copy_files()

        """Step 8: Validate, need to flush the DavFS cache first."""
        self.run_step_validate_files()

        """ End of processing files."""
        self.davfs.davfs_unmount(fail_okay=True, console=self.args.verbose)

        """Step 9: write output files."""
        self.run_step_write_files()

        if self.args.verbose:
            script.end()

    def validate_nextcloud_files(self):
        """
        1. Time out files.
        2. md5sum erorrs.
        3. missing files (delete worked but copy failed).
        """
        dav_dir = self.get_davfs_mount_dir()
        oc_dir = self.cfg['nextcloud']['directory']['root']
        git_dir = self.cfg['git']['directory']['root']

        for file_to_delete in self.sync_data['files_to_delete']:
            if (os.path.isfile(os.path.join(dav_dir, file_to_delete))):
                if (file_to_delete not in self.sync_data['errors']):
                    error_row = [
                        file_to_delete,
                        script.getnow(),
                        'DELETE FAILED']
                    self.sync_data['errors'][file_to_delete] = dict(
                        zip(self.cfg['report']['error']['columns'], error_row))
            elif (file_to_delete in self.sync_data['errors']):
                del(self.sync_data['errors'][file_to_delete])

        copy_okay = True
        for file_to_copy in self.sync_data['files_to_copy']:
            if (not os.path.isfile(os.path.join(dav_dir, file_to_copy))):
                """Missing file"""
                copy_okay = False
                if (file_to_copy not in self.sync_data['errors']):
                    error_row = [file_to_copy, script.getnow(), 'COPY FAILED']
                    self.sync_data['errors'][file_to_copy] = dict(
                        zip(self.cfg['report']['error']['columns'], error_row))
            else:
                """Copy error."""
                davfs_md5sum = self.sync_data.get_md5sum(
                    os.path.join(oc_dir, file_to_copy))
                if (davfs_md5sum !=
                        self.sync_data['file_sync_md5sum'][file_to_copy]):
                    copy_okay = False
                    if (file_to_copy not in self.sync_data['errors']):
                        nextcloud_size = os.stat(
                            os.path.join(oc_dir, file_to_copy)).st_size
                        git_size = os.stat(os.path.join(
                            git_dir, file_to_copy)).st_size
                        reason = "DIFF(%s!=%s)" % (nextcloud_size, git_size)
                        error_row = [file_to_copy, script.getnow(), reason]
                        self.sync_data['errors'][file_to_copy] = dict(
                            zip(self.cfg['report']['error']['columns'], error_row))
            if (copy_okay and (file_to_copy in self.sync_data['errors'])):
                del(self.sync_data['errors'][file_to_copy])

    def write_errors(self):
        """Write errors out in sorted timestamp order."""
        col = self.cfg['report']['error']['column']['timestamp']
        if self.args.verbose:
            self.log.prog("errors: %s" %
                          (list(self.sync_data['errors'].values())))
        error_rows = sorted(
            list(
                self.sync_data['errors'].values()),
            key=lambda a: a[col])
        with open(self.cfg['report']['file']['error'], 'w') as error_fh:
            error_csv = csv.DictWriter(
                error_fh, fieldnames=self.cfg['report']['error']['columns'])
            error_csv.writeheader()
            for error_row in error_rows:
                error_csv.writerow(error_row)

    def write_processed_files(self):
        """Write files processed out in sorted timestamp order."""
        with open(self.cfg['report']['file']['process'], 'a') as process_fh:
            process_csv = csv.writer(process_fh)
            for file_to_delete in [
                    x for x in self.sync_data['files_to_delete'] if x not in self.sync_data['errors']]:
                process_csv.writerow(
                    [file_to_delete, script.getnow(), 'DELETE'])
            for file_to_copy in [
                    x for x in self.sync_data['files_to_copy'] if x not in self.sync_data['errors']]:
                process_csv.writerow([file_to_copy, script.getnow(), 'COPY'])

# -----------------------------------------------------------------------------
#
#  main
# -----------------------------------------------------------------------------


def main(argv):
    """main: system test method with new object, use run() on same object."""

    nextcloudgitsync = TheGMUNextCloudGitSync()

    nextcloudgitsync.init_args(argv)

    if (nextcloudgitsync.args.create_template):
        nextcloudgitsync.create_template_file()
    else:
        nextcloudgitsync.init_cfg()

        if (nextcloudgitsync.args.today_report):
            print(nextcloudgitsync.get_mail_report())
        elif (nextcloudgitsync.args.yesterday_report):
            print(nextcloudgitsync.get_mail_report(previous_day=True))
        elif (nextcloudgitsync.args.create_template):
            nextcloudgitsync.create_template_file()
        else:
            nextcloudgitsync.run(argv)

# end main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main(sys.argv[1:])

# -----------------------------------------------------------------------------
#                              EOF
# -----------------------------------------------------------------------------
