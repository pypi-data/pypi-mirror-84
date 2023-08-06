# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_env']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.20,<2.0.0',
 'adaptive>=0.11.1,<0.12.0',
 'deepdish>=0.3.6,<0.4.0',
 'h5py>=2.10.0,<3.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numba>=0.51.2,<0.52.0',
 'numexpr>=2.7.1,<3.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'plotly>=4.12.0,<5.0.0',
 'requests>=2.24.0,<3.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'seaborn>=0.11.0,<0.12.0',
 'tensorflow>=2.3.0,<3.0.0',
 'xarray>=0.16.1,<0.17.0',
 'xyzpy>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'ml-env',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rafal Skolasinski',
    'author_email': 'r.j.skolasinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
