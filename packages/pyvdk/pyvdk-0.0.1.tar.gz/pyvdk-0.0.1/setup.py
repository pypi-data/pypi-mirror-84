# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvdk',
 'pyvdk.event',
 'pyvdk.rule',
 'pyvdk.tools',
 'pyvdk.tools.keyboard',
 'pyvdk.types',
 'pyvdk.vk_api',
 'pyvdk.vk_api.categories']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0', 'pyyaml>=5.3.1,<6.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pyvdk',
    'version': '0.0.1',
    'description': 'vk toolkit',
    'long_description': None,
    'author': 'lightmanLP',
    'author_email': 'liteman1000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
