#!/usr/bin/env python3
"""

"""

import setuptools
import sys

from setuptools.command.test import test as TestCommand


NAME = "pymarshal"
VERSION = "1.1.0"
URL = 'https://github.com/j3ffhubb/pymarshal'


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
    description="Pythonic implementation of Golang's (un)marshalling of JSON",
    long_description=open('README.md', 'rt').read(),
    url=URL,
    packages=[
        NAME
    ],
    include_package_data=True,
    install_requires=[],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
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
        "marshal",
        "unmarshal",
    ],
)
