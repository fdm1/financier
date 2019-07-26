#!/usr/bin/env python
# pylint: disable=missing-docstring,exec-used

from setuptools import setup, find_packages
import os.path


def read_version():
    """Read the library version"""
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'budgie',
        '_version.py'
    )
    with open(path) as f:
        exec(f.read())
        return locals()['__version__']

INSTALL_REQUIRES = [
    'scipy==1.3.0',
]

if __name__ == '__main__':
    setup(
        name='budgie',
        version=read_version(),
        description='Budget Forecasting Budget Builder, now with probabilities',
        author='fdm1',
        url='https://github.com/fdm1/financier',

        packages=find_packages(
            exclude='tests',
        ),

        install_requires=INSTALL_REQUIRES,
    )
