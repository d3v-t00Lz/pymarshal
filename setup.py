#!/usr/bin/env python3
"""

"""

import os
import setuptools
import sys

from setuptools.command.test import test as TestCommand


NAME = "pymarshal"
URL = 'https://github.com/j3ffhubb/pymarshal'
DESCRIPTION = (
    "Pythonic implementation of Golang's (un)marshalling of structs "
    "to/from various data serialization formats"
)


def _version():
    if 'test' in sys.argv:
        # avoid triggering a pytest coverage report bug
        return 'test'
    path = sys.path[:]
    dirname = os.path.dirname(__file__)
    abspath = os.path.abspath(dirname)
    sys.path.insert(
        0,
        abspath,
    )
    import pymarshal
    version = pymarshal.__version__
    sys.path = path
    return version

VERSION = _version()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            "--cov", NAME,
            "--cov-report", "html",
        ]

    def run_tests(self):
        import shlex
        #import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setuptools.setup(
    name=NAME,
    version=VERSION,
    author="Jeff Hubbard",
    author_email='j3ffhubb@users.noreply.github.com',
    license='BSD',
    description=DESCRIPTION,
    long_description=open('README.md', 'rt').read(),
    url=URL,
    packages=setuptools.find_packages(
        exclude=["*.test", "*.test.*", "test.*", "test"],
    ),
    include_package_data=True,
    install_requires=[],
    tests_require=[
        'bson',
        'pytest',
        'pytest-cov',
    ],
    extras_require={
        'bson': ['bson']
    },
    cmdclass = {'test': PyTest},
    setup_requires=['pytest-runner'],
    # PyPI
    download_url="/".join([
        URL,
        "archive",
        "{}.tar.gz".format(VERSION),
    ]),
    keywords=[
        "go",
        "golang",
        "json",
        "bson",
        "yaml",
        "marshal",
        "unmarshal",
        "struct",
    ],
)
