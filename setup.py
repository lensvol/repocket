# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

description = 'Automatic rule-based tag suggestor for Pocket'
if os.path.exists('README.md'):
    with open('README.md', 'r') as fp:
        long_description = fp.read()
else:
    long_description = description

setup(
    description=description,
    name='repocket',
    zip_safe=False,
    author='Kirill Borisov',
    author_email='borisov.kir@gmail.com',
    url='https://github.com/lensvol/repocket',
    keywords=['pocket', 'tag'],
    long_description=long_description,
    version='0.1.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    license='MIT',
    install_requires=[
        'click==3.3',
        'pocket==0.3.5',
        'PyYAML==3.11',
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    packages=['repocket', 'tests'],
    entry_points={
        'console_scripts': ['repocket=repocket.main:processor']
    },
)
