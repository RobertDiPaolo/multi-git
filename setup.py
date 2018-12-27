"""
DevOps Library for coralbay.tv development.
"""
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from multigit import __author__, __email__, __version__

here = path.abspath(path.dirname(__file__))

# # Get the long description from the README file
# with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(name='multi-git',
      version=__version__,
      description='Run a Git command on multiple repositories.',
      #long_description=long_description,

      url='https://github.com/RobertDiPaolo/multi-git.git',
      author=__author__,
      author_email=__email__,

      license='Commercial',
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: Other/Proprietary License',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='development build-tools git',
      packages=find_packages(exclude=['docs', 'tests']),
      scripts=['bin/multi-git', 'bin/multi-git.py'],

      # requirements that anyone consuming the library needs.
      install_requires=[
          "pyyaml"
      ]

      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      # extras_require={
      #     'dev': ['check-manifest'],
      #     'test': ['coverage'],
      #   },
      )
