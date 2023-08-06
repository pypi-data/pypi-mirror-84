#!/usr/bin/env python
 
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

import asthook
 
#class pre_install(install):
#    def run(self):
#        if "bdist" in self.install_libbase:
#            apk2java.setup("build/lib/" + self.config_vars["dist_name"])
#        else:
#            apk2java.setup(self.install_libbase + "/" + \
#                    self.config_vars["dist_name"])
#        subprocess.run(["make", "-C", "apk2java/java"])
#        install.run(self)


setup(
    name='asthook',
    version='0.0.5',
    packages=['src'],
    #data_files=[('apk2java/java', ['java/Class2Java.jar'])],
    package_data={'asthook': ['bin/Frida.zip',]},
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="Analyse apk source code and make a dynamic analysis",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url="https://gitlab.com/MadSquirrels/mobile/asthook",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
        'console_scripts': [
            'asthook=asthook:main',
        ],
    },
    cmdclass={
    #    'install': pre_install
    },
    install_requires = [
    ],
    python_requires='>=3.5'
 
)
