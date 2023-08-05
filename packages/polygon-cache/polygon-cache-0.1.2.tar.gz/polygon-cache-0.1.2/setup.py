# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polygon_cache', 'polygon_cache.tests']

package_data = \
{'': ['*']}

install_requires = \
['polygon-api-client>=0.1.6,<0.2.0',
 'pytz>=2020.1,<2021.0',
 'requests-cache>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'polygon-cache',
    'version': '0.1.2',
    'description': 'A package that caches polygon API calls and seamlessly calls the API multiple times to get all requested data.',
    'long_description': '# Polygon Cache\n\n![Tests](https://github.com/raymond-devries/polygon-cache/workflows/Tests/badge.svg)\n\nThis a very specific package that is wrapper over the polygon python sdk to allow for caching of historical data calls. This package will also automatically calculate and combine multiple calls to get all requested historical data. \n',
    'author': 'raymond-devries',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
