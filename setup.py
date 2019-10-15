#!/usr/bin/env python3
import codecs
from os import path
import re
import setuptools

name = "gibberify"


def find_version():
    with codecs.open(path.join('gibberify', 'utils', 'general.py'), 'r') as f:
        version_file = f.read()
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f.readlines()]

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name=name,
        scripts=['bin/gibberify'],
        version=find_version(),
        author='Lorenzo Gaifas',
        author_email='brisvag@gmail.com',
        description='Simple gibberish generator that translates words from a real language '
                    'to a pronounceable gibberish.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/brisvag/gibberify',
        packages=setuptools.find_packages(),
        package_data={
            'assets': '*',
            'config': 'config.json'
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
            'Operating System :: OS Independent',
        ],
        install_requires=requirements,
        python_requires='>=3.5'
        )
