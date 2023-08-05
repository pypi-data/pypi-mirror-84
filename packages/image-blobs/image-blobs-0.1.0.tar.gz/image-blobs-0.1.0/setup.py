#!/usr/bin/env python

import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as F:
    long_description = F.read()

setup(
    name='image-blobs',
    version='0.1.0',
    description="Analysis for gray scale images containing gaussian shaped blobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPL-3+',
    author='Michael Davidsaver',
    author_email='mdavidsaver@gmail.com',
    url='https://github.com/mdavidsaver/blobs',
    python_requires='>=2.7',

    packages=find_packages(),
    install_requires = [
        'scipy',
    ],
    extras_require={
        'test': ['nose'],
    },
    zip_safe = True,

    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
    ],
    keywords='image fitting',
)
