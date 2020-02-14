from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))[:-1]

setup(
    name="pyshuttle",
    version="0.0.3.dev1",
    description="Cross-chain atomic swaps between the networks of two cryptocurrencies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    author="Meheret Tesfaye",
    author_email="meherett@zoho.com",
    url="https://github.com/mehetett/pyshuttle",
    packages=find_packages(),
    keywords=['shuttle'],
    entry_points={
        'console_scripts': ["shuttle=shuttle.shell.__main__:main"]
    },
    python_requires=">=3.5,<4",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
