# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nenucal', 'nenucal.tests', 'nenucal.tools']

package_data = \
{'': ['*'], 'nenucal': ['cal_config/*', 'templates/*']}

install_requires = \
['GPy>=1.9.9,<2.0.0',
 'astropy>=4.0,<5.0',
 'astroquery>=0.4,<0.5',
 'click>=7.0,<8.0',
 'keyring>=20.0,<21.0',
 'libpipe>=0.1.1,<0.2.0',
 'matplotlib>=3.0,<4.0',
 'nenupy>=1.0,<2.0',
 'python-casacore>=3.0,<4.0',
 'requests>=2.0,<3.0',
 'scipy>=1.4,<2.0',
 'tables>=3.2,<4.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['calpipe = nenucal.tools.calpipe:main',
                     'flagtool = nenucal.tools.flagtool:main',
                     'modeltool = nenucal.tools.modeltool:main',
                     'nenudata = nenucal.tools.nenudata:main',
                     'soltool = nenucal.tools.soltool:main']}

setup_kwargs = {
    'name': 'nenucal',
    'version': '0.1.5',
    'description': 'Calibration pipeline for the NenuFAR Cosmic Dawn project',
    'long_description': 'NenuCAL CD\n==========\n\nCalibration pipeline for the NenuFAR Cosmic Dawn project\n\nInstallation\n------------\n\nnenucal-cd can be installed via pip:\n\n    $ pip install nenucal-cd\n\nand requires Python 3.7.0 or higher. For most tasks, you will also need [DPPP](https://github.com/lofar-astron/DP3/tree/master/DPPP), [LSMTool](https://www.astron.nl/citt/lsmtool/overview.html) that you can install with the command:\n\n    $ pip install git+https://github.com/darafferty/LSMTool.git\n\nand [LoSoTo](https://revoltek.github.io/losoto/) that you can install with the command:\n\n    $ pip install git+https://github.com/revoltek/losoto\n\n',
    'author': '"Florent Mertens"',
    'author_email': '"florent.mertens@gmail.com"',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/flomertens/nenucal-cd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
