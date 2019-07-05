#!/usr/bin/env python3

import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name='gibberify',
        scripts=['bin/gibberify'],
        version='1.0-beta',
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
        install_requires=[
            'pyphen',
            'transliterate',
            'PyQt5',
        ],
        python_requires='>=3.5'
        )
