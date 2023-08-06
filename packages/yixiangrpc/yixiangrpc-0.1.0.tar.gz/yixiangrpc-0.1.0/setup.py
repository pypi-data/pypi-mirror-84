# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yixiangrpc']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.33.2,<2.0.0', 'grpcio>=1.33.2,<2.0.0']

setup_kwargs = {
    'name': 'yixiangrpc',
    'version': '0.1.0',
    'description': 'Generate protobuf and grpc stub python files to a package.',
    'long_description': None,
    'author': 'duyixian',
    'author_email': 'duyixian@meideng.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
