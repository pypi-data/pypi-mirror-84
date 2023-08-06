# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['penvy', 'penvy.logger.colorlog']

package_data = \
{'': ['*'],
 'penvy': ['bash/*',
           'check/*',
           'cli/*',
           'cmd/*',
           'conda/*',
           'conda/activate.d/*',
           'conda/deactivate.d/*',
           'container/*',
           'dotenv/*',
           'env/*',
           'filesystem/*',
           'git/*',
           'logger/*',
           'parameters/*',
           'poetry/*',
           'python/*',
           'setup/*',
           'shell/*',
           'string/*',
           'tear_down/*']}

entry_points = \
{'console_scripts': ['penvy-init = penvy.init:main']}

setup_kwargs = {
    'name': 'penvy',
    'version': '1.0.0a2',
    'description': 'Pyfony framework development environment initializer',
    'long_description': "# Penvy - Pyfony development environment\n\nfor the [Pyfony framework](https://github.com/pyfony/pyfony)\n\n### What it does:\n\n* Prepares the **Conda-based python dev environment** in the project's **.venv directory**\n* Installs the [Poetry package manager](https://python-poetry.org/) into the user's home dir\n* Installs all the dependencies defined in project's **poetry.lock** file\n* Sets conda activation & deactivation scripts (mostly setting environment variables based on the project's **.env file**)\n* Copies the project's **.env file** from the **.env.dist** template file\n* Adds `poetry install --no-root` to post-merge GIT hook \n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/penvy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
