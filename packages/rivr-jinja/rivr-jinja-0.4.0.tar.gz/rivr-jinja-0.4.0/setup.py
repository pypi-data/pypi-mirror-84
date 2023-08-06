#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='rivr-jinja',
    version='0.4.0',
    description='rivr integration for using the Jinja template engine.',
    url='https://github.com/rivrproject/rivr-jinja',
    packages=find_packages(),
    install_requires=['rivr>=0.9.0', 'Jinja2'],
    author='Kyle Fuller',
    author_email='kyle@fuller.li',
    license='BSD',
    classifiers=(
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
    ),
)
