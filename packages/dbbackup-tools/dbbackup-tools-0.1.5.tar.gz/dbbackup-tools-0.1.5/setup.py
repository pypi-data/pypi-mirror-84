# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbbackup_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dbbackup-tools',
    'version': '0.1.5',
    'description': 'Package dbbackup to manage server database backups',
    'long_description': '# dbbackup-tools \nTool to create a new dbbackup folder\n\npip install dbbackup\n\ndbbackup-tools is instaled with dbbackup dependencies\n\nRun it:\n- python\n- import dbbackup_tools.util\n- Enter your folder name to hold dbbackup configuration\n- cd to your new dbbackup folder\n\nConfiguration:\n- ajust the file .env to match your local configration\n\n- To logging on smtp, rename and adjust:\n\nloggin_config_example.yaml to loggin_config.yaml\n\n- To backup Mysql databases, rename and adjust:\n\nmysql-backup-script_example.config to mysql-backup-script.config\n\nWork with it:\n- python\n- import dbbackup\n- from dbbackup import check_dbbackup\n',
    'author': 'Emmanuel DISCORS',
    'author_email': 'e.discors.perso@gmail.com',
    'maintainer': 'Emmanuel DISCORS',
    'maintainer_email': 'e.discors.perso@gmail.com',
    'url': 'https://github.com/EmmanuelDiscors?tab=repositories',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
