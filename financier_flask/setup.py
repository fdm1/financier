#!/usr/bin/env python
# pylint: disable=missing-docstring,exec-used

from setuptools import setup, find_packages
import os.path


def read_version():
    """Read the library version"""
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'financier_flask',
        '_version.py'
    )
    with open(path) as f:
        exec(f.read())
        return locals()['__version__']

INSTALL_REQUIRES = [
    'Flask==1.0',
    'Flask-Menu',
    'Flask-Session',
    'PyYAML==3.12',
]


if __name__ == '__main__':
    setup(
        name='financier_flask',
        version=read_version(),
        description='Budget Forecasting Flask App',
        author='fdm1',
        url='https://github.com/fdm1/financier',

        packages=find_packages(
            exclude='tests',
        ),

        install_requires=INSTALL_REQUIRES,
    )
