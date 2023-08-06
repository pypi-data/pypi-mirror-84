# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beelzebub', 'beelzebub.base']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'logging-config>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'beelzebub',
    'version': '0.1.0',
    'description': 'Lightweight framework for transforming input to output',
    'long_description': None,
    'author': 'Paul Breen',
    'author_email': 'paul.breen6@btinternet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
