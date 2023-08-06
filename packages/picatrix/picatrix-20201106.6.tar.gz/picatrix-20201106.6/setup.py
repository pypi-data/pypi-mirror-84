#!/usr/bin/env python
# Copyright 2020 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This is the setup file for the project."""
import sys

from setuptools import find_packages
from setuptools import setup

from picatrix import version

DEPENDENCIES = [
    'altair>=4.1.0',
    'click>=7.1.2',
    'dfdatetime>=20200824',
    'google-auth>=1.17.2',
    'google-auth-oauthlib>=0.4.1',
    'ipython>=5.5.0',
    'ipywidgets>=5.1.1',
    'jupyter>=1.0.0',
    'jupyter-http-over-ws>=0.0.8',
    'MarkupSafe>=1.1.1',
    'nest-asyncio>=1.4.1',
    'notebook>=5.3.0',
    'numpy>=1.19.0',
    'oauthlib==3.1.0',
    'pandas>=1.1.3',
    'python-dateutil>=2.8.1',
    'pytz>=2020.1',
    'PyYAML>=5.3.1',
    'requests>=2.23.0',
    'requests-oauthlib>=1.3.0',
    'timesketch-api-client>=20201027',
    'timesketch-import-client>=20200910',
    'vega>=3.4.0',
    'xlrd>=1.2.0',
]


# Conditional dependencies define a dependency and then a condition that
# should return a bool. This bool will then be used to determine whether
# to include the dependency or not.
CONDITIONAL_DEPENDENCIES = [
    (
        'typing-extensions==3.7.4.3',
        (sys.version_info.major == 3 and sys.version_info.minor < 8)
    ),
]

def get_requirements():
  """Returns a list of requirements."""
  requires = DEPENDENCIES

  for dependency, condition in CONDITIONAL_DEPENDENCIES:
    if condition:
      requires.append(dependency)
  return requires


def get_test_requirements():
  requires = []
  with open('test_requirements.txt', 'r') as fh:
    for line in fh:
      requires.append(line.strip())
  return requires


long_description = (
    'picatrix - a framework to assist security analysts using '
    'Colab or Jupyter to perform forensic investigations.')

setup(
    name='picatrix',
    version=version.get_version(),
    description='Picatrix IPython Helpers',
    long_description=long_description,
    license='Apache License, Version 2.0',
    url='https://github.com/google/picatrix/',
    maintainer='Picatrix development team',
    maintainer_email='picatrix-developers@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
    zip_safe=False,
    #install_requires=get_requirements(),
    intall_requires=DEPENDENCIES,
    tests_require=get_test_requirements(),
)
