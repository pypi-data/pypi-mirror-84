# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gino_aiohttp']
install_requires = \
['aiohttp>=3.7.2,<4.0.0', 'gino>=1.0.1,<2.0.0']

entry_points = \
{'gino.extensions': ['aiohttp = gino_aiohttp']}

setup_kwargs = {
    'name': 'gino-aiohttp',
    'version': '0.2.0',
    'description': 'An extension for GINO to integrate with aiohttp',
    'long_description': '# gino-aiohttp\n\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7579f869992a4b618e115731821e43ee)](https://www.codacy.com/gh/python-gino/gino-aiohttp?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=python-gino/gino-aiohttp&amp;utm_campaign=Badge_Grade)\n\n## Introduction\n\nAn extension for GINO to support aiohttp.web server.\n\n## Usage\n\nThe common usage looks like this:\n\n```python\nfrom aiohttp import web\nfrom gino.ext.aiohttp import Gino\n\ndb = Gino()\napp = web.Application(middlewares=[db])\ndb.init_app(app)\n```\n\n',
    'author': 'Fantix King',
    'author_email': 'fantix.king@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-gino/gino-aiohttp',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
