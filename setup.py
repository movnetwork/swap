#!/usr/bin/env python3

from setuptools import (
    setup, find_packages
)

import swap

# README.md
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

# requirements.txt
with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))

setup(
    name="swap",
    version=swap.__version__,
    description=swap.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=swap.__license__,
    author=swap.__author__,
    author_email=swap.__email__,
    url="https://github.com/meherett/swap",
    packages=find_packages(),
    keywords=[
        "cross-chain", "atomic", "swap", "htlc", "bitcoin", "bytom", "ethereum", "vapor", "xinfin", "cryptocurrencies"
    ],
    entry_points={
        "console_scripts": ["swap=swap.cli.__main__:main"]
    },
    python_requires=">=3.6,<4",
    install_requires=requirements,
    extras_require={
        "tests": [
            "pytest>=6.2.4,<7",
            "pytest-cov>=2.12.1,<3"
        ],
        "docs": [
            "sphinx>=4.0.2,<5",
            "sphinx-rtd-theme>=0.5.2,<1",
            "sphinx-click>=3.0.1,<4"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development"
    ],
    include_package_data=True
)
