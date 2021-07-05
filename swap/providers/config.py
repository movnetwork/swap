#!/usr/bin/env python3

from swap import __version__

# Bitcoin config
bitcoin: dict = {
    "mainnet": {
        "blockchain": "https://blockchain.info",
        "smartbit": "https://api.smartbit.com.au/v1/blockchain",
        "blockcypher": {
            "url": "https://api.blockcypher.com/v1/btc/main",
            "token": "c6ef693d3c024088810e6fac2a1494ee"
        }
    },
    "testnet": {
        "blockchain": "https://testnet.blockchain.info",
        "smartbit": "https://testnet-api.smartbit.com.au/v1/blockchain",
        "blockcypher": {
            "url": "https://api.blockcypher.com/v1/btc/test3",
            "token": "c6ef693d3c024088810e6fac2a1494ee"
        }
    },
    "path": "m/44'/0'/0'/0/0",
    "bip44_path": "m/44'/0'/{account}'/{change}/{address}",
    "locktime": 0,
    "version": 2,
    "network": "mainnet",
    "units": {
        "BTC": 1,
        "mBTC": 1_000,
        "Satoshi": 100_000_000
    },
    "unit": "Satoshi",
    "timeout": 60,
    "headers": {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
}

# Bytom config
bytom: dict = {
    "mainnet": {
        "bytom-core": "http://localhost:9888",
        "blockmeta": "https://blockmeta.com/api/v3",
        "blockcenter": "https://ex.movapi.com/bytom/v3"
    },
    "solonet": {
        "bytom-core": "http://localhost:9888",
        "blockmeta": None,
        "blockcenter": None
    },
    "testnet": {
        "bytom-core": "http://localhost:9888",
        "blockmeta": None,
        "blockcenter": None
    },
    "path": "m/44/153/1/0/1",
    "bip44_path": "m/44/153/{account}/{change}/{address}",
    "indexes": ["2c000000", "99000000", "01000000", "00000000", "01000000"],
    "unit": "NEU",
    "timeout": 60,
    "htlc_script_binary": "547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac",
    "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "to_create_new_block_seconds": 150,  # 2.5 minutes -> 150 seconds
    "units": {
        "BTM": 1,
        "mBTM": 1_000,
        "NEU": 100_000_000
    },
    "confirmations": 1,
    "network": "mainnet",
    "forbid_chain_tx": False,
    "headers": {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
}

# Ethereum config
ethereum: dict = {
    "mainnet": {
        "infura": {
            "http": "https://mainnet.infura.io/v3",
            "websocket": "wss://mainnet.infura.io/ws/v3",
            "token": "4414fea5f7454211956b1627621450b4"
        },
        "contract_address": None
    },
    "ropsten": {
        "infura": {
            "http": "https://ropsten.infura.io/v3",
            "websocket": "wss://ropsten.infura.io/ws/v3",
            "token": "4414fea5f7454211956b1627621450b4"
        },
        "contract_address": "0xE5cb615899436A490dBde26d7880A0C2502Fc676"
    },
    "kovan": {
        "infura": {
            "http": "https://kovan.infura.io/v3",
            "websocket": "wss://kovan.infura.io/ws/v3",
            "token": "4414fea5f7454211956b1627621450b4"
        },
        "contract_address": None
    },
    "rinkeby": {
        "infura": {
            "http": "https://rinkeby.infura.io/v3",
            "websocket": "wss://rinkeby.infura.io/ws/v3",
            "token": "4414fea5f7454211956b1627621450b4"
        },
        "contract_address": None
    },
    "testnet": {
        "ganache-cli": {
            "http": "http://localhost:8545",
            "websocket": "wss://localhost:8545",
            "token": None
        },
        "contract_address": None
    },
    "path": "m/44'/60'/0'/0/0",
    "bip44_path": "m/44'/60'/{account}'/{change}/{address}",
    "units": {
        "Ether": 1,
        "Gwei": 1_000_000_000,
        "Wei": 1_000_000_000_000_000_000
    },
    "provider": "http",
    "network": "mainnet",
    "unit": "Wei",
    "timeout": 60,
    "headers": {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
}

# Vapor config
vapor: dict = {
    "mainnet": {
        "vapor-core": "http://localhost:9889",
        "blockmeta": "https://vapor.blockmeta.com/api/v1",
        "blockcenter": "https://ex.movapi.com/vapor/v3"
    },
    "solonet": {
        "vapor-core": "http://localhost:9889",
        "blockmeta": None,
        "blockcenter": None
    },
    "testnet": {
        "vapor-core": "http://localhost:9889",
        "blockmeta": None,
        "blockcenter": None
    },
    "path": "m/44/153/1/0/1",
    "bip44_path": "m/44/153/{account}/{change}/{address}",
    "indexes": ["2c000000", "99000000", "01000000", "00000000", "01000000"],
    "unit": "NEU",
    "timeout": 60,
    "htlc_script_binary": "547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac",
    "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "to_create_new_block_seconds": 0.5,  # 0.5 second
    "units": {
        "BTM": 1,
        "mBTM": 1_000,
        "NEU": 100_000_000
    },
    "confirmations": 1,
    "network": "mainnet",
    "forbid_chain_tx": False,
    "headers": {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
}

# XinFin config
xinfin: dict = {
    "mainnet": {
        "http": "https://rpc.xinfin.network",
        "websocket": "wss://ws.xinfin.network",
        "contract_address": "xdc656869af3Ec1E8b2982Fc370A0526541C0Ceb90B"
    },
    "testnet": {
        "http": "http://localhost:8545",
        "websocket": "wss://localhost:8545",
        "contract_address": None
    },
    "path": "m/44'/550'/0'/0/0",
    "bip44_path": "m/44'/550'/{account}'/{change}/{address}",
    "units": {
        "XDC": 1,
        "Gwei": 1_000_000_000,
        "Wei": 1_000_000_000_000_000_000
    },
    "provider": "http",
    "network": "mainnet",
    "unit": "Wei",
    "timeout": 60,
    "headers": {
        "user-agent": f"Swap User-Agent {__version__}",
        "content-type": "application/json; charset=utf-8",
        "accept": "application/json"
    }
}
