# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pachyderm', 'pachyderm.alice', 'pachyderm.alice.datasets', 'pachyderm.fit']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0',
 'iminuit>=1.5.2,<2.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numdifftools>=0.9.39,<0.10.0',
 'numpy>=1.19.3,<2.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'scipy>=1.5.3,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8',
                                                         'importlib-resources>=3.3.0,<4.0.0'],
 'docs': ['Sphinx>=3.2.1,<4.0.0',
          'recommonmark>=0.6.0,<0.7.0',
          'sphinx-markdown-tables>=0.0.15,<0.0.16'],
 'docs:python_version >= "3.6" and python_version < "3.8"': ['importlib-metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['downloadALICEDataset = '
                     'pachyderm.alice.download:run_dataset_download',
                     'downloadALICERunByRun = '
                     'pachyderm.alice.download:run_download_run_by_run_train_output']}

setup_kwargs = {
    'name': 'pachyderm',
    'version': '3.0',
    'description': 'Physics Analysis Core for Heavy-Ions',
    'long_description': "# 🐘 Pachyderm\n\n[![Documentation Status](https://readthedocs.org/projects/pachyderm-heavy-ion/badge/?version=latest)](https://pachyderm-heavy-ion.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.com/raymondEhlers/pachyderm.svg?branch=master)](https://travis-ci.com/raymondEhlers/pachyderm)\n[![codecov](https://codecov.io/gh/raymondEhlers/pachyderm/branch/master/graph/badge.svg)](https://codecov.io/gh/raymondEhlers/pachyderm)\n\nPachyderm[\\*](#name-meaning) provides core functionality for heavy-ion physics analyses. The main\nfunctionality includes a generic histogram projection interface, a recursive configuration determination\nmodule (including overriding (merging) capabilities), and general utilities (especially for histograms). It\nprovides base functionality to the [ALICE jet-hadron\nanalysis](https://github.com/raymondEhlers/alice-jet-hadron) package. This package provides many examples of\nhow pachyderm can be used in various analysis tasks.\n\nFor further information on the capabilities, see the\n[docuemntation](https://readthedocs.org/projects/pachyderm-heavy-ion/badge/?version=latest).\n\n## Installation\n\nPachyderm requires python 3.6 or above. It is available on [PyPI](https://pypi.org/project/pachyderm/) and can\nbe installed via pip:\n\n```bash\n$ pip install pachyderm\n```\n\n## Dependencies\n\nAll dependencies are specified in the `setup.py` (and will be handled automatically when installed via pip)\nexcept for ROOT. The package can be installed without ROOT with limited functionality, but for full\nfunctionality, ROOT must be available.\n\n### Dockerfile\n\nThere is a Dockerfile which is used for testing pachyderm with ROOT. It is based on the\n[Overwatch](https://github.com/raymondEhlers/OVERWATCH) [base docker\nimage](https://hub.docker.com/r/rehlers/overwatch-base/) to allow us to avoid redeveloping another container\njust to have ROOT available. It may also be used to run pachyderm if so desired, although such a use case\ndoesn't seem tremendously useful (which is why the image isn't pushed to docker hub).\n\n## Development\n\nI recommend setting up the development environment as follows:\n\n```bash\n# Setup\n$ poetry install\n# Setup git pre-commit hooks to reduce errors\n$ pre-commit install\n# develop develop develop...\n```\n\n## Documentation\n\nAll classes, functions, etc, should be documented, including with typing information. [The\ndocs](https://pachyderm-heavy-ion.readthedocs.io/en/latest/) are built on each new successful commit. They can\nalso be built locally using:\n\n```bash\n# Setup\n$ poetry install\n# Create the docs\n$ pushd doc && make html && popd\n# Open the created docs\n$ open docs/_build/html/index.html\n```\n\n## Name Meaning\n\n**PACHYDERM**: **P**hysics **A**nalysis **C**ore for **H**eav**Y**-ions with **D**etermination of (analysis)\n**E**lements via **R**ecursion and **M**erging.\n\n",
    'author': 'Raymond Ehlers',
    'author_email': 'raymond.ehlers@cern.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
