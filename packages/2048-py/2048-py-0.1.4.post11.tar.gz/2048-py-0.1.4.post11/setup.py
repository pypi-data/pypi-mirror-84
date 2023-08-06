# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main']
install_requires = \
['termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': '2048-py',
    'version': '0.1.4.post11',
    'description': '2048 written in Python by the Ladue High School Computer Science Club',
    'long_description': "# 2048\n\n\n## What is this?\n\nIt's 2048, written in Python by the Ladue High School Computer Science Club. It's still in its early stages, so expect bugs!\n\n\n## Getting started\n\n### Download and run\n\nDownload or clone this repo, then run `python3 main.py`.\n\nIf Python complains about `termcolor`, install it with `pip install termcolor`.\n\n### Run online\n\nRun it online on [Repl.it](https://repl.it/@Ta180m/2048#main.py).\n\n### Install using `pip`\n\nRun `pip install 2048-py`.\n\n### Get it from the AUR\n\nOn Arch Linux, get the `2048-py` package from the AUR.\n",
    'author': 'Anthony Wang',
    'author_email': 'ta180m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
