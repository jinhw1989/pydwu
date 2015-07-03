# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pydwu',
    Version=find_packages('pydwu.py'),
    description='A python interface to retrieve historical weather data from Weather Underground without API',
    author='Hongwei Jin',
    author_email='jinhw1989@gmail.com',
    url='https://github.com/jinhw1989/pydwu',
    license='Apache License, Version 2.0',
    keywords='weather underground history download',
    packages=find_packages(),
    scripts=['pydwu.py'],
    install_requires=['urllib', 'datetime'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
