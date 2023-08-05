# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calendarweek']

package_data = \
{'': ['*']}

extras_require = \
{u'django': ['Django>=2.2,<4.0']}

setup_kwargs = {
    'name': 'calendarweek',
    'version': '0.4.6',
    'description': 'Utilities for working with calendar weeks in Python and Django',
    'long_description': None,
    'author': 'Dominik George',
    'author_email': 'nik@naturalnet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/python-calendarweek',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
