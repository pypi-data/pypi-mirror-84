# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drizm_commons', 'drizm_commons.sqla']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy==1.3.20']

setup_kwargs = {
    'name': 'drizm-commons',
    'version': '0.2.2',
    'description': 'Python3 commons for the Drizm organization',
    'long_description': '# Python Commons\n[![PyPI version](https://badge.fury.io/py/drizm-commons.svg)](https://badge.fury.io/py/drizm-commons)  \n\nThis package includes shared code used by\nthe Drizm organizations development team.  \n\nIt is not intended for public usage but you\nmay still download, redistribute or \nmodify it to your liking.\n\n## Usage\n\nInstall:  \n>pip install drizm-commons\n\nImport like so:  \nimport drizm_commons\n\n## Documentation\n\npass\n\n## Changelog\n\n### 0.1.1\n\n- Added SQLAlchemy JSON Encoder\n- Fixed bugs related to the Introspection\nAPI\n- Added table registry\n- Added additional utilities\n\n### 0.1.2\n\n- Added get_root_path and recursive delete\nPath utilities\n- Fixed various bugs\n\n### 0.2.0\n\n- Added full test suite\n- Added testing tools\n- Revamped introspection API\n- Provided additional overrides for the\nSQL connection adapter\n\n### 0.2.1\n\n- Added support for datetime JSON\nencoding\n\n### 0.2.2\n\n- Improved in-code documentation\n- Integrated additional utils from\ndrizm-django-commons\n',
    'author': 'ThaRising',
    'author_email': 'kochbe.ber@gmail.com',
    'maintainer': 'Dominik Lewandowski',
    'maintainer_email': 'dominik.lewandow@gmail.com',
    'url': 'https://github.com/drizm-team/python-commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
