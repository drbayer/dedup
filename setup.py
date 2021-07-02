#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='dedup',
    version='0.0.1',
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'dedup = src.scripts.dedup:dedup',
        ],
    },
)