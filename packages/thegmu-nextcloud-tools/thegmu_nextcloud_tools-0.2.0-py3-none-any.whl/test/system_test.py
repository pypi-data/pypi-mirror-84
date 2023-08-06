#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TheGMUNextCloudGitSyncSystemTest - System Tests that mount davfs."""

import csv
import os
import pprint
import shutil
import unittest
import yaml

import thegmu_nextcloud_tools
from thegmu_nextcloud_tools import script
from thegmu_nextcloud_tools.thegmu_nextcloud_git_sync import TheGMUNextCloudGitSync
from thegmu_nextcloud_tools.git_sync_data import GitSyncData
from thegmu_nextcloud_tools.thegmu_log import TheGMULog

TEST_DIR = os.path.abspath(os.path.dirname(thegmu_nextcloud_tools.__file__))
TEST_DIR = os.path.realpath(os.path.join(TEST_DIR, "../test"))

SYSTEM_TEST_FILE = os.path.join(TEST_DIR,
                                'data/thegmu_nextcloud_git_sync.test.yaml')


class TheGMUNextCloudGitSyncSystemTest(unittest.TestCase):
    """
    TEST_FILE should be by hostname to prevent running on unconfigured hosts.
    The system test requires davfs to be configured, including
    the credentials configured in /etc/davfs/secrets.
    """

    TEST_FILE = SYSTEM_TEST_FILE

    @staticmethod
    def _get_csv_dict_data(csv_file):
        """Slurp a CSV file in as an array of Dict objects."""

        slurp = []
        with open(csv_file, 'r') as csv_fh:
            csv_reader = csv.DictReader(csv_fh)
            for row in csv_reader:
                slurp.append(row)
        return slurp

    def _system_test_git_init(self):
        """Perform a git init or clean -f in the test repo."""

        print("Initializing git repo directory.")

        root_dir = self.test_yaml['git']['directory']['root']
        repo_dir = os.path.join(root_dir, '.git')
        if (not os.path.isdir(repo_dir)):
            cmd = "cd %s; git init" % (root_dir, )
            script.runcmd(cmd, console=True)
            cmd = "cd %s; git add --all ." % (root_dir, )
            script.runcmd(cmd, console=True)
            cmd = """cd %s; git commit -m"Initial test commit." -a""" % \
                (root_dir, )
            script.runcmd(cmd, console=True)
        else:
            cmd = "cd %s; git clean -f -d" % (root_dir, )
            script.runcmd(cmd, console=True)

    def _system_test_nextcloud_up(self):
        """Return false if the test nextcloud instance is unavailable"""
        print("Initializing sync object.")
        gsc = TheGMUNextCloudGitSync()
        gsc.init([self.test_yaml_file, ])
        gsc.davfs.up_check_or_exit()
        return True

    def _system_test_nextcloud_clean(self):
        """Perform rm -rf on the local, simulated NextCloud file
        system directory. Remove all files in the test NextCloud account.
        """
        """If the GIT repo has nothing in it then a simple sync will
        delete all GIT files in the NextCloud corresponding account."""
        self._system_test_git_init()

        print("Removing the simulated NextCloud file system files.")
        """rm -rf the simulated directory."""
        next_dir = self.test_yaml['nextcloud']['directory']['root']
        self.assertTrue(len(next_dir) > 10, "Sanity check on rm -rf")
        cmd = "/bin/rm -rf %s" % (next_dir)
        print("cmd: %s" % (cmd, ))
        script.runcmd(cmd, console=True)
        os.mkdir(next_dir)

        """Sync the empty GIT directory to clean."""
        print("Cleaning NextCloud account by sync'ing an empty GIT repo.")
        print("Initializing sync object.")
        gsc = TheGMUNextCloudGitSync()
        print("PWD: %s" % (os.getcwd()))
        gsc.run([self.test_yaml_file, ])

        dav_dir = gsc.get_davfs_mount_dir()
        gsc.davfs.davfs_mount()
        cloud_files = gsc.sync_data.get_directory_files(dav_dir)
        print("Removing files not in GIT: %s" % (cloud_files, ))
        print(pprint.pformat(cloud_files))
        for cloud_file in cloud_files:
            gsc.davfs.davfs_delete(dav_dir, cloud_file)
        gsc.davfs.davfs_unmount()
        print("Clean done.")

    def _system_test_compare_files(self, relative_path, equal_test=True):
        """Compare a GIT file with a NextCloud file that as been sync'ed."""
        print("Comparing GIT file with NextCloud file: %s" % (relative_path, ))
        print("Initializing sync object.")
        gsc = TheGMUNextCloudGitSync()
        gsc.init([self.test_yaml_file, ])

        gsc.davfs.davfs_mount()

        gsd = GitSyncData()
        git_path = os.path.join(self.test_yaml['git']['directory']['root'],
                                relative_path)
        nextcloud_path = os.path.join(
            self.test_yaml['davfs']['mount']['target_dir'],
            relative_path)
        git_md5sum = gsd.get_md5sum(git_path)
        nextcloud_md5sum = gsd.get_md5sum(nextcloud_path)
        gsc.davfs.davfs_unmount(fail_okay=True, console=False)

        if (equal_test):
            self.assertEqual(git_md5sum, nextcloud_md5sum,
                             "%s GIT/Nextcloud versions are not equal" %
                             relative_path)
        else:
            self.assertNotEqual(git_md5sum, nextcloud_md5sum,
                                "%s GIT/Nextcloud versions are equal" %
                                relative_path)

    @staticmethod
    def _system_test_report_clean():
        """Delete previous run reports. """

        print("Cleaning report  directory.")
        shutil.rmtree("report")
        os.mkdir("report")

    def _system_test_nextcloud_is_empty(self):
        """Ensure the Next Cloud test account has no files.
        If not fail."""

        print("Enpty check using find to find files in NextCloud account.")
        print("Initializing sync object.")
        gsc = TheGMUNextCloudGitSync()
        gsc.init([self.test_yaml_file, ])
        gsc.davfs.davfs_mount()
        dav_dir = gsc.get_davfs_mount_dir()
        print("dav_dir: %s" % (dav_dir, ))
        cmd = "find %s -type f 2>/dev/null | wc -l " % dav_dir
        print(cmd)
        empty_check = script.runcmd(cmd, encoding='utf-8', console=False)
        gsc.davfs.davfs_unmount(fail_okay=True, console=False)
        empty_check = int(empty_check.strip())
        return(empty_check == 0)

    def setUp(self):

        self.log = TheGMULog('tst')
        os.chdir(TEST_DIR)

        if not os.path.isdir('report'):
            os.mkdir('report')

        if (os.path.exists(TheGMUNextCloudGitSyncSystemTest.TEST_FILE)):
            self.test_yaml_file = TheGMUNextCloudGitSyncSystemTest.TEST_FILE
            with open(self.test_yaml_file, 'r') as test_yaml_fh:
                self.test_yaml = yaml.load(
                    test_yaml_fh, Loader=yaml.SafeLoader)
        print("SYSTEM_TEST_FILE %s" % (SYSTEM_TEST_FILE, ))
        if not os.path.isdir(self.test_yaml['nextcloud']['directory']['root']):
            os.makedirs(self.test_yaml['nextcloud']['directory']['root'])

    def tearDown(self):
        pass

    # @unittest.skip("Commented Out")
    def test01_system(self):
        """System test that recreates mounts dafvs and recreates the data per test."""
        """
        You don't need to be running NextCloud locally for these tests.
        You do however need to be able to mount a valid NextCloud account
        with no data.
        """
        process_file = self.test_yaml['report']['file']['process']
        error_file = self.test_yaml['report']['file']['error']

        script.print_dashes("""Step 1. START Ensure the test server is up.""")

        self.assertTrue(self._system_test_nextcloud_up(),
                        "NextCloud account is unavailable: %s " %
                        (self.test_yaml['nextcloud']['account']['nextcloud']))
        self.log.prog("""Step 1. END   Server is up.""")

        script.print_dashes(
            """Step 2. START Setup: Clean GIT repo & NextCloud account.""")
        self._system_test_nextcloud_clean()

        self.assertTrue(
            self._system_test_nextcloud_is_empty(),
            "NextCloud account has files, clean failed.")

        self.log.prog(
            """Step 2. END   Setup: Clean GIT repo & NextCloud account.""")
        script.print_dashes("Step 3. Copy one file.")
        self._system_test_report_clean()
        root_dir = self.test_yaml['git']['directory']['root']
        test_file = 'README.txt'
        copy_file = os.path.join(root_dir,
                                 'exclude_test', test_file)
        #cmd = "/bin/cp %s %s" % (copy_file, root_dir )
        shutil.copy(copy_file, root_dir)
        gsc = TheGMUNextCloudGitSync()
        gsc.run([self.test_yaml_file, ])
        self._system_test_compare_files(test_file)
        error_report = self._get_csv_dict_data(error_file)
        self.assertTrue(len(error_report) == 0,
                        "Sync errors: %s" % (error_report, ))
        process_report = self._get_csv_dict_data(process_file)
        self.assertTrue(len(process_report) == 1,
                        "COPY: too many files copied: %s" % (process_report, ))
        self.assertEqual(
            test_file,
            process_report[0]['File'], "COPY: %s unexpected file name." %
            (process_report[0]['File'], ))

        self.assertEqual('COPY', process_report[0]['Cause'],
                         "COPY: %s unexpected cause." %
                         (process_report[0]['Cause'], ))

        self.log.prog("""Step 3. END   Copy one file.""")
        script.print_dashes("Step 4. Modify one file.")

        src_test_file = os.path.join(root_dir,
                                     'exclude_test', 'hosts')
        tgt_test_file = os.path.join(root_dir, test_file)
        shutil.copyfile(src_test_file, tgt_test_file)
        gsc.run([self.test_yaml_file, ])
        self._system_test_compare_files(test_file)
        process_report = self._get_csv_dict_data(process_file)
        self.assertTrue(len(process_report) == 2,
                        "COPY: too many files copied: %s" % (process_report, ))
        self.assertEqual(
            test_file, process_report[1]['File'],
            "COPY: %s unexpected file name." %
            (process_report[1]['File'], ))
        self.assertEqual('COPY', process_report[1]['Cause'],
                         "COPY: %s unexpected cause." %
                         (process_report[1]['Cause'], ))
        self.log.prog("""Step 4. END   Modify one file.""")

    def test02_mail_report(self):
        """Test of mail report text."""
        print("")
        gsc = TheGMUNextCloudGitSync()
        script.print_dashes("MAIL REPORT TODAY")
        report = gsc.get_mail_report(config_file=self.test_yaml_file)
        print(report)
        print()
        script.print_dashes("MAIL REPORT YESTERDAY")
        report = gsc.get_mail_report(
            config_file=self.test_yaml_file,
            previous_day=True)
        print(report)

    def test03_get_directories(self):
        """Unit test to detect directories to delete in Nextcloud."""
        gsd = GitSyncData()
        test_dir = '/etc'
        test_dirs = gsd.get_directories(test_dir)
        print("%s dirs: %s" % (test_dir, test_dirs, ))
        empty_test_dirs = gsd.get_directories(test_dir, empty_only=True)
        empty_test_dirs = [os.path.join(test_dir, x) for x in empty_test_dirs]
        for empty_test_dir in empty_test_dirs:
            empty_test_dir = os.path.join(test_dir, empty_test_dir)
            self.assertTrue(len(os.listdir(empty_test_dir)) == 0,
                            "'%s' empty test of directory failed." %
                            empty_test_dir)
        print("%s empty dirs: %s" % (test_dir, empty_test_dirs, ))

    @staticmethod
    def test04_create_template_file():
        """create_template_file test."""

        host_name = script.get_hostname(host_name_only=False)
        print("host_name: %s" % (host_name,))
        gsc = TheGMUNextCloudGitSync()
        host_file = gsc.create_template_file(file_name_only=True)
        print("create_template_file name: %s" % (host_file, ))
        gsc.create_template_file()
        os.unlink(host_file)
        print("%s file deleted." % (host_file, ))

    # @unittest.skip("Commented Out")

    def test05_bug_directory_delete(self):
        """DavFS cannot delete directories with files in them.
        This means all files have to be deleted and then
        directories.
        """

        self._system_test_git_init()
        script.print_dashes("Step 1. START Copy directory to delete.")
        tgt_dir = 'data/git/nextcloud_testdata/delete'
        src_dir = 'data/git/nextcloud_testdata/exclude_test/delete'
        nextcloud_dir = self.test_yaml['nextcloud']['directory']['root']

        print("Copying directory %s -> %s" % (src_dir, tgt_dir))
        shutil.copytree(src_dir, tgt_dir)
        self.log.prog("Step 1. END   Copy directory to delete")

        script.print_dashes(
            "Step 2. START Sync directory to delete to NextCloud.")
        gsc = TheGMUNextCloudGitSync()
        gsc.run([self.test_yaml_file, ])
        dav_dir = gsc.get_davfs_mount_dir()

        gsc.davfs.davfs_mount()
        self.assertTrue(os.path.isdir(os.path.join(dav_dir, 'delete')))
        self.assertTrue(os.path.isdir(os.path.join(nextcloud_dir, 'delete')))
        empty_dir = os.path.join(dav_dir, "delete/1/2/3/4/5")
        print("Create an empty directory with no files: %s " % (empty_dir, ))
        cmd = "sudo mkdir -p %s " % (empty_dir, )
        script.runcmd(cmd, console=True)
        gsc.davfs.davfs_unmount()
        self.log.prog("Step 2. END   Sync directory to delete to NextCloud")
        script.print_dashes(
            "Step 3. START Delete GIT dierctory, test NextCloud sync.")
        self._system_test_git_init()
        self.assertTrue(os.path.isdir(os.path.join(nextcloud_dir, 'delete')))
        gsc.run(['-v', self.test_yaml_file, ])
        gsc.davfs.davfs_mount()
        self.assertFalse(os.path.isdir(os.path.join(nextcloud_dir, 'delete')))
        self.assertFalse(os.path.exists(os.path.join(dav_dir, 'delete')))
        gsc.davfs.davfs_unmount()
        self.log.prog(
            "Step 3. END   Delete GIT directrry, test NextCloud sync")
