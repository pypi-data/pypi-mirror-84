#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import find_namespace_packages, setup

NAME = "zsv.ticker"
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), "r") as f:
    readme = f.read()

with open(os.path.join(here, "src", "zsv", "ticker", "__init__.py"), "r") as f:
    version = re.search('__version__ = "([^"]+)"', f.read()).group(1)

with open(os.path.join(here, "requirements.txt"), "r") as f:
    requires = [x.strip() for x in f if x.strip()]

with open(os.path.join(here, "requirements-test.txt"), "r") as f:
    requires_test = [x.strip() for x in f if x.strip()]

with open(os.path.join(here, "requirements-dev.txt"), "r") as f:
    requires_dev = [x.strip() for x in f if x.strip()]

setup(
    name=NAME,
    version=version,
    description="Enabling flexible and idiomatic regular execution of tasks.",
    entry_points=None,
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Tobias Dély",
    author_email="cleverhatcamouflage@gmail.com",
    python_requires=">=3.6",
    url="https://gitlab.com/tdely/zsv.ticker",
    namespace_packages=["zsv"],
    packages=find_namespace_packages(include=["zsv.*"], where="src"),
    package_dir={"": "src"},
    install_requires=requires,
    setup_requires=["pytest-runner"],
    tests_require=requires_test,
    extras_require={"test": requires_test, "dev": requires_dev},
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
