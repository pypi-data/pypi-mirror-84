# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_tools',
 'fast_tools.base',
 'fast_tools.exporter',
 'fast_tools.limit',
 'fast_tools.limit.backend']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-tools',
    'version': '1.1.0',
    'description': 'fast-tools is a FastApi/Starlette toolset, Most of the tools can be used in FastApi/Starlette, a few tools only support FastApi which is divided into the lack of compatibility with FastApi',
    'long_description': None,
    'author': 'So1n',
    'author_email': 'qaz6803609@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/so1n/fast-tools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
