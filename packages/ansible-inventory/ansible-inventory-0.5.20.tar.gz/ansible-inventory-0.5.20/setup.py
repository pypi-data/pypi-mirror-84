#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# vim: set ts=2 sw=2 sts=2 et:


from setuptools import setup
import os
import sys
import shutil
from subprocess import Popen
from ansible_inventory.globals import VERSION as AI_VERSION, AUTHOR_NAME as AI_AUTHOR, AUTHOR_MAIL as AI_AUTHOR_EMAIL, URL as AI_URL

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
#files = ["things/*"]

#####################################
#NOTE: Requires: fakeroot, alien, dpkg-buildpackage

#-- GOBAL VARS --
NAME         = "ansible-inventory"
VERSION      = AI_VERSION
AUTHOR       = AI_AUTHOR
AUTHOR_EMAIL = AI_AUTHOR_EMAIL
URL          = AI_URL
LICENSE      = "GPLv3"
DESCRIPTION  = 'Script to manage your Ansible Inventory and also can be used by ansible as a dynamic inventory source'
LONG_DESCRIPTION = """%s
Author: %s <%s>
Project: %s
""" % ( DESCRIPTION, AUTHOR, AUTHOR_EMAIL, URL )


SCRIPTS=['ansible-inv']
PACKAGES=['ansible_inventory',
          'ansible_inventory.backends',
          'ansible_inventory.frontends'
          ]
MANIFEST="""
include ansible-inv
"""
DATA_FILES={}

#-- PYPI VARS --
PYPI_DOWNLOAD_URL='https://github.com/diego-treitos/ansible-inventory/archive/v'+VERSION+'.tar.gz'
PYPI_DEPENDS=['redis', 'Pygments']
PYPI_KEYWORDS=['ansible', 'inventory', 'dynamic', 'management']

#-- DEB VARS --
DEB_DEPENDS=['python3', 'python3-pygments']
DEB_RECOMMENDS=['python3-redis']
DEB_SETUP_DIR='setup.files'


def sh_exec(cmdstr):
    return Popen(cmdstr, shell=True)


def presetup():
    """presetup"""
    # WRITE setup.cfg
    setupcfg = open('setup.cfg', 'w')
    setupcfg.write("""[bdist_rpm]\nbinary-only = 1""")
    setupcfg.close()

    # WRITE MANIFEST.in
    manifest = open('MANIFEST.in', 'w')
    manifest.write(MANIFEST)
    manifest.close()


def postsetup():
    """postsetup"""
    rpm_path=None
    for i in range( 1, 20 ):
        rpm_path='dist/'+NAME+'-'+VERSION+'-%d.noarch.rpm' % i
        if os.path.exists( rpm_path ):
            break

    cmd = sh_exec('fakeroot alien -gc %s' % rpm_path)
    if cmd.wait() == 0:
        pack_path=NAME+'-'+VERSION
        # Edit control file
        #
        control_lines = open(os.path.join(pack_path, 'debian/control')).readlines()
        control = open(os.path.join(pack_path, 'debian/control'), 'w')
        for line in control_lines:
            if line.lower().split(':')[0] == 'depends':
                # Add dependencies
                line= 'Depends: ' + ', '.join(DEB_DEPENDS) + '\n'
                # Add recommends
                line+='Recommends: ' + ', '.join(DEB_RECOMMENDS) + '\n'
            if line.lower().split(':')[0] == 'maintainer':
                line= 'Maintainer: ' + AUTHOR + ' <' + AUTHOR_EMAIL + '>\n'
            control.write(line)
        control.close()
        # Edit rules file
        #
        rules_lines = open(os.path.join(pack_path, 'debian/rules')).readlines()
        rules = open(os.path.join(pack_path, 'debian/rules'), 'w')
        for line in rules_lines:
            rules.write(line)
            if line.find('dh_installdirs') != -1:
                rules.write('\tdh_installinit\n')
                rules.write('\tdh_installcron\n')
                rules.write('\tdh_installifupdown\n')
                rules.write('\tdh_installlogrotate\n')
                rules.write('\tdh_installman\n')
        rules.close()
        # Add setup.files
        for sf in os.listdir( DEB_SETUP_DIR ):
            shutil.copyfile( os.path.join(DEB_SETUP_DIR, sf), os.path.join(pack_path, 'debian', sf) )
        cmd = sh_exec('cd %s; dpkg-buildpackage -us -uc -b' % pack_path)
        if cmd.wait() != 0:
            print("ERROR BUILDING .deb PACKAGE")


############################################################################
# PreSetup
if 'bdist_rpm' in sys.argv:
    presetup()

setup(
  name = NAME,
  version = VERSION,
  description = DESCRIPTION,
  long_description = LONG_DESCRIPTION,
  license = LICENSE,
  author = AUTHOR,
  author_email = AUTHOR_EMAIL,
  url = URL,
  # Name the folder where your packages live:
  # (If you have other packages (dirs) or modules (py files) then
  # put them into the package directory - they will be found
  # recursively.)
  packages = PACKAGES,
  # 'package' package must contain files (see list above)
  # I called the package 'package' thus cleverly confusing the whole issue...
  # This dict maps the package name =to=> directories
  # It says, package *needs* these files.
  package_data = DATA_FILES,
  # 'runner' is in the root.
  scripts = SCRIPTS,
  #
  # This next part it for the Cheese Shop, look a little down the page.
  # classifiers = []
  data_files = DATA_FILES,
  # Requirements
  python_requires = '>=3',
  install_requires = PYPI_DEPENDS
)

# PostSetup
if 'bdist_rpm' in sys.argv:
    postsetup()
