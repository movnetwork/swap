#!/usr/bin/env python3

from shuttle.providers.config import bitcoin, bytom


def test_config():
    btc, btm = bitcoin(), bytom()

    assert btc["mainnet"]["blockchain"] == "https://blockchain.info"
    assert btc["mainnet"]["smartbit"] == "https://api.smartbit.com.au/v1/blockchain"
    assert btc["mainnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/main"
    assert btc["mainnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert btc["testnet"]["blockchain"] == "https://testnet.blockchain.info"
    assert btc["testnet"]["smartbit"] == "https://testnet-api.smartbit.com.au/v1/blockchain"
    assert btc["testnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/test3"
    assert btc["testnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"

    assert btc["timeout"] == 60
    assert btc["sequence"] == 100

    assert btm["mainnet"]["bytom"] == "http://localhost:9888"
    assert btm["mainnet"]["blockmeta"] == "https://blockmeta.com/api/v2"
    assert btm["mainnet"]["blockcenter"] == "https://bcapi.bystack.com/api/v2/btm"

    assert btm["solonet"]["bytom"] == "http://localhost:9888"
    assert btm["solonet"]["blockmeta"] == "https://blockmeta.com/api/v2"
    assert btm["solonet"]["blockcenter"] == "https://bcapi.bystack.com/api/v2/btm"

    assert btm["testnet"]["bytom"] == "http://localhost:9888"
    assert btm["testnet"]["blockmeta"] == "https://blockmeta.com/api/wisdom"
    assert btm["testnet"]["blockcenter"] == "https://bcapi.bystack.com/api/v2/wisdom"

    assert btm["timeout"] == 60
    assert btm["BTM_asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert btm["fee"] == 10000000
    assert btm["confirmations"] == 1
    assert btm["sequence"] == 100
