#!/usr/bin/env python3

from swap import __version__
from swap.providers.config import (
    bitcoin, bytom, ethereum, vapor, xinfin
)


def test_config():
    
    assert isinstance(bitcoin, dict)
    assert bitcoin["mainnet"]["blockchain"] == "https://blockchain.info"
    assert bitcoin["mainnet"]["smartbit"] == "https://api.smartbit.com.au/v1/blockchain"
    assert bitcoin["mainnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/main"
    assert bitcoin["mainnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"
    assert bitcoin["testnet"]["blockchain"] == "https://testnet.blockchain.info"
    assert bitcoin["testnet"]["smartbit"] == "https://testnet-api.smartbit.com.au/v1/blockchain"
    assert bitcoin["testnet"]["blockcypher"]["url"] == "https://api.blockcypher.com/v1/btc/test3"
    assert bitcoin["testnet"]["blockcypher"]["token"] == "c6ef693d3c024088810e6fac2a1494ee"
    assert bitcoin["path"] == "m/44'/0'/0'/0/0"
    assert bitcoin["bip44_path"] == "m/44'/0'/{account}'/{change}/{address}"
    assert bitcoin["locktime"] == 0
    assert bitcoin["version"] == 2
    assert bitcoin["network"] == "mainnet"
    assert bitcoin["units"]["BTC"] == 1
    assert bitcoin["units"]["mBTC"] == 1_000
    assert bitcoin["units"]["Satoshi"] == 100_000_000
    assert bitcoin["unit"] == "Satoshi"
    assert bitcoin["timeout"] == 60
    assert bitcoin["headers"]["user-agent"] == f"Swap User-Agent {__version__}"
    assert bitcoin["headers"]["content-type"] == "application/json; charset=utf-8"
    assert bitcoin["headers"]["accept"] == "application/json"

    assert isinstance(ethereum, dict)
    assert ethereum["mainnet"]["infura"]["http"] == "https://mainnet.infura.io/v3"
    assert ethereum["mainnet"]["infura"]["websocket"] == "wss://mainnet.infura.io/ws/v3"
    assert ethereum["mainnet"]["infura"]["token"] == "4414fea5f7454211956b1627621450b4"
    assert ethereum["mainnet"]["contract_address"] is None
    assert ethereum["ropsten"]["infura"]["http"] == "https://ropsten.infura.io/v3"
    assert ethereum["ropsten"]["infura"]["websocket"] == "wss://ropsten.infura.io/ws/v3"
    assert ethereum["ropsten"]["infura"]["token"] == "4414fea5f7454211956b1627621450b4"
    assert ethereum["ropsten"]["contract_address"] == "0xE5cb615899436A490dBde26d7880A0C2502Fc676"
    assert ethereum["kovan"]["infura"]["http"] == "https://kovan.infura.io/v3"
    assert ethereum["kovan"]["infura"]["websocket"] == "wss://kovan.infura.io/ws/v3"
    assert ethereum["kovan"]["infura"]["token"] == "4414fea5f7454211956b1627621450b4"
    assert ethereum["kovan"]["contract_address"] is None
    assert ethereum["rinkeby"]["infura"]["http"] == "https://rinkeby.infura.io/v3"
    assert ethereum["rinkeby"]["infura"]["websocket"] == "wss://rinkeby.infura.io/ws/v3"
    assert ethereum["rinkeby"]["infura"]["token"] == "4414fea5f7454211956b1627621450b4"
    assert ethereum["rinkeby"]["contract_address"] is None
    assert ethereum["testnet"]["ganache-cli"]["http"] == "http://localhost:8545"
    assert ethereum["testnet"]["ganache-cli"]["websocket"] == "wss://localhost:8545"
    assert ethereum["testnet"]["ganache-cli"]["token"] is None
    assert ethereum["testnet"]["contract_address"] is None
    assert ethereum["path"] == "m/44'/60'/0'/0/0"
    assert ethereum["bip44_path"] == "m/44'/60'/{account}'/{change}/{address}"
    assert ethereum["units"]["Ether"] == 1
    assert ethereum["units"]["Gwei"] == 1_000_000_000
    assert ethereum["units"]["Wei"] == 1_000_000_000_000_000_000
    assert ethereum["provider"] == "http"
    assert ethereum["network"] == "mainnet"
    assert ethereum["unit"] == "Wei"
    assert ethereum["timeout"] == 60
    assert ethereum["headers"]["user-agent"] == f"Swap User-Agent {__version__}"
    assert ethereum["headers"]["content-type"] == "application/json; charset=utf-8"
    assert ethereum["headers"]["accept"] == "application/json"

    assert isinstance(bytom, dict)
    assert bytom["mainnet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["mainnet"]["blockmeta"] == "https://blockmeta.com/api/v3"
    assert bytom["mainnet"]["blockcenter"] == "https://ex.movapi.com/bytom/v3"
    assert bytom["solonet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["solonet"]["blockmeta"] is None
    assert bytom["solonet"]["blockcenter"] is None
    assert bytom["testnet"]["bytom-core"] == "http://localhost:9888"
    assert bytom["testnet"]["blockmeta"] is None
    assert bytom["testnet"]["blockcenter"] is None
    assert bytom["path"] == "m/44/153/1/0/1"
    assert bytom["bip44_path"] == "m/44/153/{account}/{change}/{address}"
    assert bytom["indexes"] == ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    assert bytom["unit"] == "NEU"
    assert bytom["timeout"] == 60
    assert bytom["htlc_script_binary"] == "547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac"
    assert bytom["asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert bytom["to_create_new_block_seconds"] == 150
    assert bytom["units"]["BTM"] == 1
    assert bytom["units"]["mBTM"] == 1_000
    assert bytom["units"]["NEU"] == 100_000_000
    assert bytom["confirmations"] == 1
    assert bytom["network"] == "mainnet"
    assert bytom["forbid_chain_tx"] is False
    assert bytom["headers"]["user-agent"] == f"Swap User-Agent {__version__}"
    assert bytom["headers"]["content-type"] == "application/json; charset=utf-8"
    assert bytom["headers"]["accept"] == "application/json"

    assert isinstance(vapor, dict)
    assert vapor["mainnet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["mainnet"]["blockmeta"] == "https://vapor.blockmeta.com/api/v1"
    assert vapor["mainnet"]["blockcenter"] == "https://ex.movapi.com/vapor/v3"
    assert vapor["solonet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["solonet"]["blockmeta"] is None
    assert vapor["solonet"]["blockcenter"] is None
    assert vapor["testnet"]["vapor-core"] == "http://localhost:9889"
    assert vapor["testnet"]["blockmeta"] is None
    assert vapor["testnet"]["blockcenter"] is None
    assert vapor["path"] == "m/44/153/1/0/1"
    assert vapor["bip44_path"] == "m/44/153/{account}/{change}/{address}"
    assert vapor["indexes"] == ["2c000000", "99000000", "01000000", "00000000", "01000000"]
    assert vapor["unit"] == "NEU"
    assert vapor["timeout"] == 60
    assert vapor["htlc_script_binary"] == "547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac"
    assert vapor["asset"] == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert vapor["to_create_new_block_seconds"] == 0.5
    assert vapor["units"]["BTM"] == 1
    assert vapor["units"]["mBTM"] == 1_000
    assert vapor["units"]["NEU"] == 100_000_000
    assert vapor["confirmations"] == 1
    assert vapor["network"] == "mainnet"
    assert vapor["forbid_chain_tx"] is False
    assert vapor["headers"]["user-agent"] == f"Swap User-Agent {__version__}"
    assert vapor["headers"]["content-type"] == "application/json; charset=utf-8"
    assert vapor["headers"]["accept"] == "application/json"

    assert isinstance(xinfin, dict)
    assert xinfin["mainnet"]["http"] == "https://rpc.xinfin.network"
    assert xinfin["mainnet"]["websocket"] == "wss://ws.xinfin.network"
    assert xinfin["mainnet"]["contract_address"] == "xdc656869af3Ec1E8b2982Fc370A0526541C0Ceb90B"
    assert xinfin["testnet"]["http"] == "http://localhost:8545"
    assert xinfin["testnet"]["websocket"] == "wss://localhost:8545"
    assert xinfin["testnet"]["contract_address"] is None
    assert xinfin["path"] == "m/44'/550'/0'/0/0"
    assert xinfin["bip44_path"] == "m/44'/550'/{account}'/{change}/{address}"
    assert xinfin["units"]["XDC"] == 1
    assert xinfin["units"]["Gwei"] == 1_000_000_000
    assert xinfin["units"]["Wei"] == 1_000_000_000_000_000_000
    assert xinfin["provider"] == "http"
    assert xinfin["network"] == "mainnet"
    assert xinfin["unit"] == "Wei"
    assert xinfin["timeout"] == 60
    assert xinfin["headers"]["user-agent"] == f"Swap User-Agent {__version__}"
    assert xinfin["headers"]["content-type"] == "application/json; charset=utf-8"
    assert xinfin["headers"]["accept"] == "application/json"
