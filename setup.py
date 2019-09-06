#!/usr/bin/env python3
import codecs
from os import path
import re
import setuptools

HERE = path.abspath(path.dirname(__file__))
NAME = "gibberify"


# Load the version
def read(*parts):
    with codecs.open(path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f.readlines()]

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name=NAME,
        scripts=['bin/gibberify'],
        version=find_version("gibberify", "utils.py"),
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
