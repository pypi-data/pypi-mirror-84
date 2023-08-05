#!/usr/bin/env python

import setuptools


with open("README.md", "r") as fh:
    long_description = """
A couple of utility functions used to locate the regions of a cartesian
map where a condition is true or false

In many cases, this is not the optimal way to generate such tiles,
but it may be of use if you only have access to a function that
return true for an area.

See https://gitlab.com/jbrobertson/quad-filter/ for details.
"""


setuptools.setup(
    name='quad-filter',
    version='0.4',
    description='Filtering tools for quad trees',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='JB Robertson',
    author_email='jbr@freeshell.org',
    url='https://www.gitlab.com/jbrobertson/quad-filter/',
    packages=['quad_filter'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
