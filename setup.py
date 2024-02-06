'''
Some users have experienced issues with the MySQLdb package. As per
the authors instructions, the MySQL development libraries may
need to be installed manually:

- Debian / Ubuntu : sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
- Red Hat / CentOS: sudo yum install python3-devel mysql-devel

*** From my understanding, it is also because of this that enumdb ***
*** does not run well in virtual environments such as pipenv      ***

Resources:
https://github.com/PyMySQL/mysqlclient-python
https://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface
'''
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='enumdb',
    version='2.2.0',
    author = 'm8sec',
    description = 'Relational database brute force and post exploitation tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/m8r0wn/enumdb',
    license='GPLv3',
    platforms = ["Unix"],
    packages=find_packages(include=["enumdb", "enumdb.*"]),
    install_requires=[
                    'openpyxl',
                    'pymssql',
                    'mysqlclient',
                    'ipparser>=0.3.6',
    ],
    classifiers = [
                    "Environment :: Console",
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                    "Operating System :: Unix",
                    "Topic :: Security"
    ],
    entry_points= {
                    'console_scripts': ['enumdb=enumdb:main']
    }
)
