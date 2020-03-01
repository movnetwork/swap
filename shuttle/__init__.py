#!/usr/bin/env python3


from .shuttle import Provider
from .providers import bitcoin, bytom, config

# Shuttle Information's
__version__ = "0.1.0.dev1"
__author__ = "Meheret Tesfaye"
__email__ = "meherett@zoho.com"

# Cryptocurrency name
Bitcoin = "bitcoin"
Bytom = "bytom"


__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "Provider",
    "Bitcoin",
    "Bytom",
    "bitcoin",
    "bytom",
    "config"
]
