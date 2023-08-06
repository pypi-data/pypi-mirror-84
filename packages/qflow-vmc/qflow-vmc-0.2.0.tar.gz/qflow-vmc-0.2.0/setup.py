# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qflow',
 'qflow.hamiltonians',
 'qflow.optimizers',
 'qflow.samplers',
 'qflow.wavefunctions',
 'qflow.wavefunctions.nn',
 'qflow.wavefunctions.nn.activations',
 'qflow.wavefunctions.nn.layers']

package_data = \
{'': ['*']}

install_requires = \
['mpi4py>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'qflow-vmc',
    'version': '0.2.0',
    'description': 'Quantum Variational Monte Carlo',
    'long_description': '[![Build Status](https://travis-ci.org/bsamseth/qflow.svg?branch=master)](https://travis-ci.org/bsamseth/qflow)\n[![codecov](https://codecov.io/gh/bsamseth/qflow/branch/master/graph/badge.svg)](https://codecov.io/gh/bsamseth/qflow)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/bsamseth/qflow.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bsamseth/qflow/context:python)\n[![Language grade: C/C++](https://img.shields.io/lgtm/grade/cpp/g/bsamseth/qflow.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bsamseth/qflow/context:cpp)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/bsamseth/qflow.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bsamseth/qflow/alerts/)\n[![Lines of Code](https://tokei.rs/b1/github/bsamseth/qflow)](https://tokei.rs/b1/github/bsamseth/qflow)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n<p align="center">\n  <img src="docs/logo.png" height="200px">\n</p>\n\n# QFLOW - Quantum Variational Monte Carlo with Neural Networks\n\nSee the [documentation pages](https://bsamseth.github.io/qflow) for details regarding the `qflow` package.\n\nFor the accompanying master\'s thesis, see [writing/Thesis.pdf](https://github.com/bsamseth/qflow/raw/master/writing/Thesis.pdf)\n',
    'author': 'Bendik Samseth',
    'author_email': 'b.samseth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bsamseth.github.io/qflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
