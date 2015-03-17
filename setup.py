# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Automatic rule-based tag suggestor for Pocket',
    name='repocket',
    zip_safe=False,
    author='Kirill Borisov',
    author_email='borisov.kir@gmail.com',
    url='https://github.com/lensvol/repocket',
    version='0.0.1',
    install_requires=[
        'click==3.3',
        'pocket==0.3.5',
        'PyYAML==3.11',
    ],
    packages=['repocket'],
    entry_points={
        'console_scripts': ['repocket=repocket.main:processor']
    },
)
