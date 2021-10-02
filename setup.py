#!/usr/bin/env python3
import os
from setuptools import setup

from party_calc import __author__, __version__

base_name = os.path.abspath(os.path.dirname(__file__))


setup(
    name='party-calc',
    version=__version__,
    author=__author__,
    description='Utility to calculate party payments',
    long_description=open(os.path.join(base_name, 'README.md'), encoding='utf-8').read(),
    packages=['party_calc'],
    entry_points={
        'console_scripts': [
            'party-calc=party_calc.gui:run'
        ]
    },
    python_requires='>=3.6',
    install_requires=[
       'dataclasses; python_version < "3.7"'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ]
)
