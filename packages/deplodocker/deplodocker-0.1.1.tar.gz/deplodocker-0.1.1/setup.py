# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deplodocker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0', 'toml>=0.10,<0.11']

extras_require = \
{'speedups': ['orjson>=3.4,<4.0']}

entry_points = \
{'console_scripts': ['deplodocker = deplodocker.cli:main']}

setup_kwargs = {
    'name': 'deplodocker',
    'version': '0.1.1',
    'description': 'Locker of dependency files for deploy in docker and etc.',
    'long_description': '# DEPLODOCKER\n___________\n\n### Why?\n\nPoetry and others python dependency managers has no cozy interface to communicate with requirements.\nSome of them has no methods for export extras or extras without main requirements.\nSome of them has no possibilities to use anither format excluding `requirements.txt`.\nThis project aims to fix this problem.  \n\n\n### Basic usage\n\n```shell script\n>>> deplodocker --help\nUsage: deplodocker [OPTIONS] [SRC]\n\n  Select lock file to work with or use stdin as source\n\nOptions:\n  -d, --dst FILENAME        result file\n  -f, --input-format TEXT   format of input lock file\n  -o, --output-format TEXT  format of output file\n  --help                    Show this message and exit.\n```\n\n```shell script\n>>> deplodocker poetry.lock\n### MAIN\nclick==7.1.2\ntoml==0.10.2\n### DEV\nappdirs==1.4.4\natomicwrites==1.4.0\nattrs==20.3.0\nblack==20.8b1\n...\n### SPEEDUPS\norjson==3.4.3\n```\n\n```shell script\n>>> deplodocker poetry.lock -f poetry -o yaml\n    dev:\n      appdirs: 1.4.4\n      atomicwrites: 1.4.0\n      attrs: 20.3.0\n      black: 20.8b1\n      ...\n    main:\n      click: 7.1.2\n      toml: 0.10.2\n    speedups:\n      orjson: 3.4.3\n```\n\n```shell script\n>>> deplodocker poetry.lock -f poetry -o json\n{"main":{"click":"7.1.2","toml":"0.10.2"},"dev":{"appdirs":"1.4.4","atomicwrites":"1.4.0","attrs":"20.3.0","black":"20.8b1","cfgv":"3.2.0","colorama":"0.4.4","coverage":"5.3","distlib":"0.3.1","filelock":"3.0.12","identify":"1.5.9","iniconfig":"1.1.1","isort":"5.6.4","mypy-extensions":"0.4.3","nodeenv":"1.5.0","packaging":"20.4","pathspec":"0.8.0","pluggy":"0.13.1","pre-commit":"2.8.2","py":"1.9.0","pyparsing":"2.4.7","pytest":"6.1.2","pytest-cov":"2.10.1","pyyaml":"5.3.1","regex":"2020.10.28","six":"1.15.0","typed-ast":"1.4.1","typing-extensions":"3.7.4.3","virtualenv":"20.1.0"},"speedups":{"orjson":"3.4.3"}}\n```\n\nAlso you can use `stdin` as input and choose destination file trough arguments\n```shell script\n>>> cat poetry.lock | deplodocker poetry.lock -d requirements.json -f poetry -o json\n```\n\n<a href="https://www.buymeacoffee.com/RussianCheese" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/arial-violet.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>',
    'author': 'RCheese',
    'author_email': 'ruslan.v.samoylov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
