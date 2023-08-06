# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_encrypted_filefield',
 'django_encrypted_filefield.migrations',
 'django_encrypted_filefield.tests']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=1.7.1',
 'django>=2.2',
 'python-magic>=0.4.12,<0.5.0',
 'requests>=2.12.4']

setup_kwargs = {
    'name': 'django-encrypted-filefield',
    'version': '0.3.0',
    'description': 'Encrypt uploaded files, store them wherever you like and stream them back unencrypted',
    'long_description': None,
    'author': 'Daniel Quinn',
    'author_email': 'code@danielquinn.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielquinn/django-encrypted-filefield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
