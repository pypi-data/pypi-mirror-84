# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codepost_stats',
 'codepost_stats.analyzers',
 'codepost_stats.analyzers.abstract']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'codepost>=0.2.25,<0.3.0',
 'confuse>=1.3.0,<2.0.0',
 'javalang>=0.13.0,<0.14.0',
 'mistune>=0.8.4,<0.9.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'codepost-stats',
    'version': '0.1.0',
    'description': 'A system to compile statistics automatically from a course on the codePost platform.',
    'long_description': None,
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
