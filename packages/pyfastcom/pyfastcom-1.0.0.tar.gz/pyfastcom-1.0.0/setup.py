# coding=utf-8
"""
pyfastcom
https://github.com/ppizarror/pyfastcom

SETUP DISTRIBUTION
Create setup for PyPi.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Library imports
from setuptools import setup, find_packages
import pyfastcom

# Load readme
with open('README.rst') as f:
    long_description = f.read()

# Load requirements
with open('requirements.txt') as f:
    requirements = []
    for line in f:
        requirements.append(line.strip())

# Setup library
setup(
    name='pyfastcom',
    version=pyfastcom.__version__,
    author=pyfastcom.__author__,
    author_email=pyfastcom.__email__,
    description=pyfastcom.__description__,
    long_description=long_description,
    url=pyfastcom.__url__,
    project_urls={
        'Bug Tracker': pyfastcom.__url_bug_tracker__,
        'Documentation': pyfastcom.__url_documentation__,
        'Source Code': pyfastcom.__url_source_code__,
    },
    license=pyfastcom.__license__,
    platforms=['any'],
    keywords=pyfastcom.__keywords__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia',
    ],
    include_package_data=True,
    packages=find_packages(exclude=['test']),
    python_requires='>=3, <4',
    install_requires=requirements,
    setup_requires=[
        'setuptools',
    ],
)
