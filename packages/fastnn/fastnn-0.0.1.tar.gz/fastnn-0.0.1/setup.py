# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastnn']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'onnxruntime-tools>=1.4.2,<2.0.0',
 'onnxruntime>=1.4.0,<2.0.0',
 'torch>=1.4.0,<2.0.0',
 'transformers>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'fastnn',
    'version': '0.0.1',
    'description': 'A python library and framework for fast neural network computations.',
    'long_description': None,
    'author': 'aychang95',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
