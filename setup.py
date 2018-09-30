# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from basic_mondrian.version import __version__

setup(
    name='basic-mondrian',
    version=__version__,
    author='amon',
    author_email='amon@nandynarwhals.org',
    description='This provides an extendable implmentation of the Basic Mondrian algorithm.',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
        'setuptools',
    ],
    tests_require=[
        'pytest',
        'tox<=2.9.1',
    ],
    install_requires=[
        'Sphinx>=1.7.0',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    url='https://github.com/nnamon/basic-mondrian'
)
