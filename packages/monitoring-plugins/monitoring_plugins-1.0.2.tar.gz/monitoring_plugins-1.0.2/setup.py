#!/usr/bin/python3
# -*- coding: utf-8

#  monitoring-plugins
#
#  monitoring-plugins are the check plugins for monitoring
#
#  Copyright (c) 2020 Fabian Fröhlich <mail@confgen.org> https://icinga2.confgen.org
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  For all license terms see README.md and LICENSE Files in root directory of this Project.


import os
from distutils import log

from setuptools import setup, find_packages
from setuptools.command.install import install

from shutil import copyfile

class OverrideInstall(install):
    def run(self):
        mode = 0o755
        install.run(self)

        # here we start with doing our overriding and private magic ..
        log.info("Overriding setuptools mode of scripts ...")
        os.makedirs('/usr/local/monitoring/plugins/', exist_ok=True)
        for filepath in self.get_outputs():
            filename = os.path.basename(filepath)
            new_filename = '/usr/local/monitoring/plugins/' + filename
            if os.path.splitext(new_filename)[1] in ['.py', '.sh']:
                log.info("Copy file from %s to %s" % (filepath, new_filename))
                copyfile(filepath, new_filename)
                log.info("Changing permissions of %s to %s" % (new_filename, oct(mode)))
                os.chmod(new_filename, mode)

with open('README.md') as readme_file:
    README = readme_file.read()

additional_files = [
    'README.md',
    'LICENSE',
]
setup_args = dict(
    name='monitoring_plugins',
    version='1.0.2',
    description='Plugins for monitoring',
    long_description_content_type="text/markdown",
    long_description=README,
    license='AGPLv3',
    packages=find_packages(),
    author='Fabian Fröhlich',
    author_email='mail@confgen.org',
    keywords=['icinga', 'icinga2', 'icinga2-plugin', 'monitoring', 'check', 'nagios', 'nagios-plugin', 'nrpe',
              'healthcheck', 'serverstatus', 'security', 'security-tools'],
    url='https://github.com/f-froehlich/monitoring-plugins',
    download_url='https://pypi.org/project/monitoring-plugins/',
    package_data={'monitoring_plugins': ['*.sh']},
    data_files=[('//usr/local/monitoring/plugins/', additional_files)]
)

install_requires = [
    'monitoring-utils~=1.0.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, cmdclass={'install': OverrideInstall})
