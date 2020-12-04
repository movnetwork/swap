#!/usr/bin/env python3

from swap import __version__
from swap.providers.config import (
    bitcoin, bytom, vapor
)


def test_config():
    
    assert isinstance(bitcoin, dict) and isinstance(bytom, dict) and isinstance(vapor, dict)

    assert bitcoin["mainnet"]["blockchain"] == "https://blockchain.info"
    assert bitcoin["mainnet"]["smartbit"] == "https://api.smartbit.com.au/v1/blockchain"
    assert bitcoin["mainnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/main"
    assert bitcoin["mainnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert bitcoin["testnet"]["blockchain"] == "https://testnet.blockchain.info"
    assert bitcoin["testnet"]["smartbit"] == "https://testnet-api.smartbit.com.au/v1/blockchain"
    assert bitcoin["testnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/test3"
    assert bitcoin["testnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert bitcoin["path"] == "m/44'/0'/0'/0/0"
    assert bitcoin["BIP44"] == "m/44'/0'/{account}'/{change}/{address}"
    assert bitcoin["symbol"] == "SATOSHI"
    assert bitcoin["timeout"] == 60
    assert bitcoin["locktime"] == 0
    assert bitcoin["version"] == 2
    assert bitcoin["network"] == "mainnet"
    assert bitcoin["sequence"] == 1000
    assert bitcoin["headers"] == {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }

    assert bytom["mainnet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["mainnet"]["blockmeta"] == "https://blockmeta.com/api/v3"
    assert bytom["mainnet"]["blockcenter"] == "https://bcapi.bystack.com/bytom/v3"
    assert bytom["mainnet"]["mov"] == "https://ex.movapi.com/bytom/v3"

    assert bytom["solonet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["solonet"]["blockmeta"] is None
    assert bytom["solonet"]["blockcenter"] is None
    assert bytom["solonet"]["mov"] is None

    assert bytom["testnet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["testnet"]["blockmeta"] is None
    assert bytom["testnet"]["blockcenter"] is None
    assert bytom["testnet"]["mov"] is None

    assert bytom["path"] == "m/44/153/1/0/1"
    assert bytom["BIP44"] == "m/44/153/{account}/{change}/{address}"
    assert bytom["symbol"] == "NEU"
    assert bytom["timeout"] == 60
    assert bytom["asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert bytom["fee"] == 10_000_000
    assert bytom["estimate_fee"] is True
    assert bytom["confirmations"] == 1
    assert bytom["network"] == "mainnet"
    assert bytom["forbid_chain_tx"] is False
    assert bytom["sequence"] == 1000
    assert bytom["headers"] == {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }

    assert vapor["mainnet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["mainnet"]["blockmeta"] == "https://vapor.blockmeta.com/api/v1"
    assert vapor["mainnet"]["blockcenter"] == "https://bcapi.bystack.com/vapor/v3"
    assert vapor["mainnet"]["mov"] == "https://ex.movapi.com/vapor/v3"

    assert vapor["solonet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["solonet"]["blockmeta"] is None
    assert vapor["solonet"]["blockcenter"] is None
    assert vapor["solonet"]["mov"] is None

    assert vapor["testnet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["testnet"]["blockmeta"] is None
    assert vapor["testnet"]["blockcenter"] is None
    assert vapor["testnet"]["mov"] is None

    assert vapor["path"] == "m/44/153/1/0/1"
    assert vapor["BIP44"] == "m/44/153/{account}/{change}/{address}"
    assert vapor["symbol"] == "NEU"
    assert vapor["timeout"] == 60
    assert vapor["asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert vapor["fee"] == 10_000_000
    assert vapor["estimate_fee"] is True
    assert vapor["confirmations"] == 1
    assert vapor["network"] == "mainnet"
    assert vapor["forbid_chain_tx"] is False
    assert vapor["sequence"] == 1000
    assert vapor["headers"] == {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
