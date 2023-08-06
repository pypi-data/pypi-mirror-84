# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['auto_reloader']
setup_kwargs = {
    'name': 'auto-reloader',
    'version': '0.1.2',
    'description': 'Automatic reloading library for Jupyter',
    'long_description': '<h1 align="center">Welcome to auto-reloader 👋</h1>\n<p>\n  <img alt="Version" src="https://badge.fury.io/py/auto-reloader.svg" />\n  <a href="https://github.com/moisutsu/auto-reloader/blob/master/LICENSE" target="_blank">\n    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />\n  </a>\n  <a href="https://twitter.com/moisutsu" target="_blank">\n    <img alt="Twitter: moisutsu" src="https://img.shields.io/twitter/follow/moisutsu.svg?style=social" />\n  </a>\n</p>\n\n> Automatic reloading library for Jupyter\n\n## Install\n\n```sh\npip install auto-reloader\n```\n\n## Usage\n\n```python\nimport module as _module\nfrom auto_reloader import AutoReloader\n\nmodule = AutoReloader(_module)\n\ninstance = module.Class()\n```\n\nThe module is reloaded when an instance is created with `instance = module.Class()`.\n\nBesides this, the module is reloaded every time you access the `module` attribute.\n\n## Run tests\n\n```sh\npoetry run pytest tests\n```\n\n## Author\n\n👤 **moisutsu**\n\n* Twitter: [@moisutsu](https://twitter.com/moisutsu)\n* Github: [@moisutsu](https://github.com/moisutsu)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n## 📝 License\n\nCopyright © 2020 [moisutsu](https://github.com/moisutsu).<br />\nThis project is [MIT](https://github.com/moisutsu/auto-reloader/blob/master/LICENSE) licensed.\n\n***\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'moisutsu',
    'author_email': 'moisutsu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moisutsu/auto-reloader',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
