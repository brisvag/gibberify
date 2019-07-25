#!/usr/bin/env python3

from os import path
import setuptools

HERE = path.abspath(path.dirname(__file__))
NAME = "gibberify"

# Load the version
with open(path.join(HERE, NAME, "version.py")) as version_file:
    exec(version_file.read())


with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f.readlines()]

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name=NAME,
        scripts=['bin/gibberify'],
        version=__version__,
        author='Lorenzo Gaifas',
        author_email='brisvag@gmail.com',
        description='Simple gibberish generator that translates words from a real language '
                    'to a pronounceable gibberish.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/brisvag/gibberify',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
            'Operating System :: OS Independent',
        ],
        install_requires=requirements,
        python_requires='>=3.5'
        )
