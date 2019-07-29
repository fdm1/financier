#!/usr/bin/env python
# pylint: disable=missing-docstring,exec-used

from setuptools import setup, find_packages
import os.path


def read_version():
    """Read the library version"""
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'budget_builder',
        '_version.py'
    )
    with open(path) as f:
        exec(f.read())
        return locals()['__version__']


def get_requirements():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'requirements.txt',
    )
    with open(path) as f:
        return f.readlines()


if __name__ == '__main__':
    setup(
        name='budget_builder',
        version=read_version(),
        description='Budget Forecasting Budget Builder',
        author='fdm1',
        url='https://github.com/fdm1/financier',

        packages=find_packages(
            exclude='tests',
        ),

        install_requires=get_requirements(),
    )
