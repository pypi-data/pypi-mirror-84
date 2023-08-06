# -*- coding: utf-8 -*-import os
import os
import re
import setuptools

NAME = "thegmu-nextcloud-tools"
AUTHOR = "Mybrid Wonderful, The GMU"
AUTHOR_EMAIL = "mybrid@thegmu.com"
DESCRIPTION = "The GMU NextCloud Tools"
LICENSE = "MIT"
KEYWORDS = [NAME, 'nextcloud', 'git']
URL = "https://bitbucket.org/thegmu/thegmu-nextcloud-tools"
README = "README.rst"
CLASSIFIERS = [
  "Environment :: Console",
  "Development Status :: 3 - Alpha",
  "Intended Audience :: System Administrators",
  "Topic :: Utilities",
  "Operating System :: Unix",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Unix Shell",
]
INSTALL_REQUIRES = ['PyYAML',  ]
ENTRY_POINTS = {}
SCRIPTS = [ 'thegmu_nextcloud_tools/thegmu_nextcloud_git_sync.py', 
           'bin/thegmu_nextcloud_git_sync.sh',
           'bin/umount.davfs.thegmu.sh', ]
VERSION_FILE='VERSION'
DATA={'thegmu_nextcloud_tools': ['data/thegmu_nextcloud_git_sync.template.yaml',] }

HERE = os.path.dirname(__file__)

def read(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()

def first_line(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.readline().strip(os.linesep)

def slurp_file(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()


VERSION = re.search(
    r'__version__ = [\'"]([^\'"]*)[\'"]',
    read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = slurp_file(README)

if __name__ == "__main__":
    setuptools.setup(name=NAME,
                     version=VERSION,
                     packages=setuptools.find_packages(),
                     author=AUTHOR,
                     description=DESCRIPTION,
                     long_description=LONG_DESCRIPTION,
                     long_description_content_type="text/markdown",
                     package_data=DATA,
                     license=LICENSE,
                     keywords=KEYWORDS,
                     url=URL,
                     classifiers=CLASSIFIERS,
                     install_requires=INSTALL_REQUIRES,
                     entry_points=ENTRY_POINTS,
                     scripts=SCRIPTS)
