#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r') as buf:
    long_description = buf.read()

setuptools.setup(
    name='licheepi',
    version='0.0.0',
    author='alan',
    author_email='alan@licheepi.com',
    description='licheepi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/licheepi/pip-licheepi',
    packages=setuptools.find_packages(),
    package_data={
        # '': ['/path/to/file', ],
    },
    install_requires=[
        # 'PACKAGE==VERSION',
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ]
)
