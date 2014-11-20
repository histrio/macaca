#!/usr/bin/env python

import os
import sys

root_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root_dir, 'src'))


import macaca

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'macaca',
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = read('REQUIREMENTS')

setup(
    name='macaca',
    version=macaca.__version__,
    description='Redmine client for Jabber.',
    long_description=read('README.rst') + '\n\n' + read('HISTORY.rst'),
    author='Rinat Sabitov',
    author_email='rinat.sabitov@gmail.com',
    url='http://macaca.falseprotagonist.me',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    license=read('LICENSE'),
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ),
    entry_points = {
        'console_scripts': [
            'macaca = macaca.alfa:main',
        ]
    },
    test_suite='test',
    tests_require=['mock', 'pytest'],
)
