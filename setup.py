#!/usr/bin/env python3

from setuptools import setup, find_packages

import shuttle

# README.md
with open("README.md", "r") as readme:
    long_description = readme.read()

# requirements.txt
with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))

setup(
    name="pyshuttle",
    version=shuttle.__version__,
    description="Cross-chain atomic swaps between the networks of two cryptocurrencies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=shuttle.__license__,
    author=shuttle.__author__,
    author_email=shuttle.__email__,
    url="https://github.com/meherett/shuttle",
    packages=find_packages(),
    keywords=["cross-chain", "atomic-swap", "cryptocurrencies"],
    entry_points={
        "console_scripts": ["shuttle=shuttle.cli.__main__:main"]
    },
    python_requires=">=3.6,<4",
    install_requires=requirements,
    extras_require={
        "tests": [
            "pytest>=5.4.1,<6",
            "pytest-cov>=2.8.1,<3"
        ],
        "docs": [
            "sphinx>=2.4.4,<3",
            "sphinx_rtd_theme>=0.4.3,<1",
            "sphinx_click>=2.3.1,<3"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development"
    ],
)
