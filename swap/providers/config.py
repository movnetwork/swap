#!/usr/bin/env python3


# Bitcoin
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
        "timeout": 60,
        "network": "testnet",
        "sequence": 1000,
        "headers": {
            # "Content-Type": "application/json"
        }
    }


# Bytom
def bytom():
    return {
        "mainnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": "https://blockmeta.com/api/v3",
            "blockcenter": {
                "v2": "https://bcapi.bystack.com/api/v2/btm",
                "v3": "https://bcapi.bystack.com/bytom/v3"
            },
        },
        "solonet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
        },
        "testnet": {
            "bytom": "http://localhost:9888",
            "blockmeta": None,
            "blockcenter": {
                "v2": None,
                "v3": None
            },
        },
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
