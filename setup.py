# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_entry_points():
    from ssh_mitm_plugins.__entrypoints__ import entry_points as plugins_entry_points
    return {
        **plugins_entry_points
    }


setup(
    name='ssh-mitm-plugins',
    version='0.1',
    author='Simon Böhm',
    author_email='support@ssh-mitm.at',
    description='advanced features for ssh-mitm server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="ssh proxy mitm network security audit plugins features advanced",
    packages=find_packages(),
    url="https://github.com/The5imon/ssh-mitm-plugins",
    project_urls={
        'Documentation': 'https://ssh-mitm-plugins.readthedocs.io',
        'Source': 'https://github.com/The5imon/ssh-mitm-plugins',
        'Tracker': 'https://github.com/The5imon/ssh-mitm-plugins/issues',
    },
    python_requires='>= 3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Topic :: System :: Networking",
        "Development Status :: 4 - Beta"
    ],
    entry_points={
        **get_entry_points()
    },
    install_requires=[
        'ssh-mitm'
    ]
)
