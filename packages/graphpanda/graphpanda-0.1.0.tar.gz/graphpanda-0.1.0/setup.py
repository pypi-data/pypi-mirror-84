#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open('README.md') as readme_file:
    readme = (here / 'README.md').read_text(encoding='utf-8')

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Maksim Bober",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="It's a python package that allows you to convert pandas dataframe into Cypher insert queries. It gives you a way to specify your record linking algorithms for determining edges and setting attributes.",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/markdown',
    long_description=readme,
    include_package_data=True,
    keywords='graphpanda',
    name='graphpanda',
    packages=find_packages(include=['graphpanda', 'graphpanda.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bobrinik/graphpanda',
    version='0.1.0',
    zip_safe=False,
)
