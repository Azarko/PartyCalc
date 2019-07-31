#!/usr/bin/env python3
from setuptools import setup

from PartyCalc import __author__, __version__


setup(
    name='party-calc',
    version=__version__,
    author=__author__,
    description='Utility to calculate party payments',
    long_description=open('README.md', encoding='utf-8').read(),
    packages=['PartyCalc'],
    entry_points={
        'console_scripts': [
            'party-calc=PartyCalc.gui:run'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7'
    ]
)
