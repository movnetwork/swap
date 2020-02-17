#!/usr/bin/env python3

from setuptools import setup, find_packages

import shuttle

# README.md
with open("README.md", "r") as readme:
    long_description = readme.read()

# requirements.txt
with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))[:-1]

setup(
    name="pyshuttle",
    version=shuttle.__version__,
    description="Cross-chain atomic swaps between the networks of two cryptocurrencies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    author=shuttle.__author__,
    author_email=shuttle.__author_email__,
    url="https://github.com/mehetett/pyshuttle",
    packages=find_packages(),
    keywords=['shuttle'],
    entry_points={
        'console_scripts': ["shuttle=shuttle.cli.__main__:main"]
    },
    python_requires=">=3.6,<4",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
