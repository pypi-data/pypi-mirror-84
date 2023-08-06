#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import join, dirname

from src import __version__, __license__, __mail__, __author__

readme = open(join(dirname(__file__), "README.rst")).read()

requirements = [
    r.strip() for r in open(join(dirname(__file__), "requirements.txt")).readlines()
]

test_requirements = [
    r.strip()
    for r in open(join(dirname(__file__), "test_requirements.txt")).readlines()
]

setup(
    name="sigfoxapi_fork",
    version=__version__,
    description="Python wrapper for the Sigfox backend REST API",
    long_description=readme,
    author=__author__,
    author_email=__mail__,
    url="https://github.com/KanduTeam/python-sigfox-backend-api.git",
    packages=["sigfoxapi_fork"],
    package_dir={"sigfoxapi_fork": "src"},
    include_package_data=True,
    install_requires=requirements,
    license=__license__,
    keywords="sigfox",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ]
)
