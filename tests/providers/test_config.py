#!/usr/bin/env python3

from swap.providers.config import bitcoin, bytom


def test_config():
    
    btc, btm = bitcoin(), bytom()
    
    assert isinstance(btc, dict) and isinstance(btm, dict)

    assert btc["mainnet"]["blockchain"] == "https://blockchain.info"
    assert btc["mainnet"]["smartbit"] == "https://api.smartbit.com.au/v1/blockchain"
    assert btc["mainnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/main"
    assert btc["mainnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert btc["testnet"]["blockchain"] == "https://testnet.blockchain.info"
    assert btc["testnet"]["smartbit"] == "https://testnet-api.smartbit.com.au/v1/blockchain"
    assert btc["testnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/test3"
    assert btc["testnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert btc["path"] == "m/44'/0'/0'/0/0"
    assert btc["BIP44"] == "m/44'/0'/{account}'/{change}/{address}"
    assert btc["symbol"] == "SATOSHI"
    assert btc["timeout"] == 60
    assert btc["locktime"] == 0
    assert btc["version"] == 2
    assert btc["network"] == "mainnet"
    assert btc["sequence"] == 1000
    assert btc["headers"] == {
        # "Content-Type": "application/json"
    }

    assert btm["mainnet"]["bytom-core"] == "http://localhost:9888"
    assert btm["mainnet"]["blockmeta"] == "https://blockmeta.com/api/v3"
    assert btm["mainnet"]["blockcenter"]["v2"] == "https://bcapi.bystack.com/api/v2/btm"
    assert btm["mainnet"]["blockcenter"]["v3"] == "https://bcapi.bystack.com/bytom/v3"

    assert btm["solonet"]["bytom-core"] == "http://localhost:9888"
    assert btm["solonet"]["blockmeta"] is None
    assert btm["solonet"]["blockcenter"]["v2"] is None
    assert btm["solonet"]["blockcenter"]["v3"] is None

    assert btm["testnet"]["bytom-core"] == "http://localhost:9888"
    assert btm["testnet"]["blockmeta"] is None
    assert btm["testnet"]["blockcenter"]["v2"] is None
    assert btm["testnet"]["blockcenter"]["v3"] is None

    assert btm["path"] == "m/44'/153/1/0/1"
    assert btm["BIP44"] == "m/44/153/{account}/{change}/{address}"
    assert btm["symbol"] == "NEU"
    assert btm["timeout"] == 60
    assert btm["asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert btm["fee"] == 10_000_000
    assert btm["confirmations"] == 1
    assert btm["network"] == "mainnet"
    assert btm["sequence"] == 1000
    assert btm["headers"] == {
        # "Content-Type": "application/json"
    }
