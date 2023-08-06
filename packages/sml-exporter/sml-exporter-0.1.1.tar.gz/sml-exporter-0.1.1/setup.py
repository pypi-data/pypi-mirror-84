# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sml_exporter']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'prometheus-client>=0.8.0,<0.9.0',
 'pysml>=0.0.2,<0.0.3']

entry_points = \
{'console_scripts': ['sml-exporter = sml_exporter.__main__:main']}

setup_kwargs = {
    'name': 'sml-exporter',
    'version': '0.1.1',
    'description': 'Smartmeter Message Language Prometheus Exporter',
    'long_description': None,
    'author': 'Martin Weinelt',
    'author_email': 'hexa@darmstadt.ccc.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
