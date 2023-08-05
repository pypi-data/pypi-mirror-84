#!/usr/bin/env python

from setuptools import setup

setup(name='pizzabot',
    version='1.1.3',
    author='light at zero',
    author_email='lightatzero@gmail.com',
    packages=['pizzabot'],
    install_requires=[
        "pytest",
    ],
    scripts=['bin/pizzabot'],
)
