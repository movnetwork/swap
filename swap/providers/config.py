#!/usr/bin/env python3


def bitcoin(blockcypher_token=None):
    if blockcypher_token is None:
        blockcypher_token = "c6ef693d3c024088810e6fac2a1494ee"
    return {
        "mainnet": {
            "blockchain": "https://blockchain.info",
            "sochain": "https://sochain.com/api/v2",
            "blockcypher": {
                "url": "https://api.blockcypher.com/v1/btc/main",
                "token": blockcypher_token
            }
        },
        "testnet": {
            "blockchain": "https://testnet.blockchain.info",
            "sochain": "https://sochain.com/api/v2",
            "blockcypher": {
                "url": "https://api.blockcypher.com/v1/btc/test3",
                "token": blockcypher_token
            }
        },
        "path": "m/44'/0'/0'/0/0",
        "BIP44": "m/44'/0'/{account}'/{change}/{address}",
        "symbol": "SATOSHI",
        "timeout": 60,
        "network": "testnet",
        "sequence": 1000,
        "headers": {
            # "Content-Type": "application/json"
        }
    }


def bytom():
    return {
        "mainnet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": {
                "v2": "https://bcapi.bystack.com/api/v2/btm",
                "v3": "https://bcapi.bystack.com/bytom/v3"
            },
        },
        "solonet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
        },
        "testnet": {
            "bytom-core": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
        },
        "path": "m/44'/153/1/0/1",
        "BIP44": "m/44/153/{account}/{change}/{address}",
        "symbol": "NEU",
        "timeout": 60,
        "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "fee": 10_000_000,
        "confirmations": 1,
        "network": "mainnet",
        "sequence": 1000,
        "headers": {
            # "Content-Type": "application/json"
        }
    }
