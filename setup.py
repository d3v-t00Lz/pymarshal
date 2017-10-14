#!/usr/bin/env python3
"""

"""

import setuptools
import sys

from setuptools.command.test import test as TestCommand


NAME = "pymarshal"

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
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)



packages = [
    NAME
]

install_requires = []
tests_requires = [
    'pytest',
    'pytest-cov',
]

setuptools.setup(
    name=NAME,
    version="0.0.0",
    author="Jeff Hubbard",
    author_email='',
    license='BSD',
    description="Pythonic implementation of Golang's (un)marshalling of JSON",
    url='https://github.com/j3ffhubb/pymarshal',
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    cmdclass = {'test': PyTest},
    setup_requires=['pytest-runner'],
    test_suite='src/test',
)
