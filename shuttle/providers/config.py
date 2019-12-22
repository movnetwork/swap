# Bitcoin network
def bitcoin():
    return {
        "mainnet": {
            "coin_type": "0",
            "blockchain": "https://blockchain.info",
            "blockcypher": "https://api.blockcypher.com/v1/btc/main"
        },
        "testnet": {
            "coin_type": "1",
            "blockchain": "https://testnet.blockchain.info",
            "blockcypher": "https://api.blockcypher.com/v1/btc/test3"
        }
    }
