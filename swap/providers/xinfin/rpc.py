#!/usr/bin/env python3

from web3 import Web3
from web3.types import Wei
from web3.providers import (
    HTTPProvider, WebsocketProvider
)
from web3.contract import Contract
from web3._utils.threads import Timeout
from pyxdc.utils import decode_transaction_raw as dtr
from hexbytes.main import HexBytes
from eth_typing import URI
from typing import (
    Optional, Tuple
)

import web3 as _web3
import requests
import json
import sys
import os

from ...exceptions import (
    AddressError, NetworkError, APIError
)
from ..config import xinfin as config
from .utils import (
    is_network, is_address, to_checksum_address
)


def get_web3(network: str = config["network"], provider: str = config["provider"]) -> Web3:
    """
    Get XinFin Web3 instance.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: Web3 -- XinFin Web3 instance.

    >>> from swap.providers.xinfin.rpc import get_web3
    >>> get_web3(network="testnet", provider="http")
    <web3.main.Web3 object at 0x000001DDECCD0640>
    """

    # Check parameter instances
    if not is_network(network=network):
        raise NetworkError(f"Invalid XinFin '{network}' network",
                           "choose only 'mainnet', 'apothem' or 'testnet' networks.")

    if provider == "http":
        web3: Web3 = Web3(HTTPProvider(
                endpoint_uri=URI(config[network]["http"]),
                request_kwargs={
                    "timeout": config["timeout"]
                }
            )
        )
        return web3
    elif provider == "websocket":
        web3: Web3 = Web3(WebsocketProvider(
                endpoint_uri=URI(config[network]["websocket"])
            )
        )
        return web3
    else:
        raise ValueError(f"Invalid XinFin '{provider}' provider",
                         "choose only 'http' or 'websocket' providers.")


def get_balance(address: str, network: str = config["network"], provider: str = config["provider"]) -> Wei:
    """
    Get XinFin balance.

    :param address: XinFin address.
    :type address: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: Wei -- XinFin balance (Wei).

    >>> from swap.providers.xinfin.rpc import get_balance
    >>> get_balance("xdc70c1eb09363603a3b6391deb2daa6d2561a62f52", "mainnet")
    71560900
    """

    # Check parameter instances
    if not is_address(address=address):
        raise AddressError(f"Invalid XinFin '{address}' address.")

    web3: Web3 = get_web3(network=network, provider=provider)
    balance: int = web3.eth.get_balance(
        to_checksum_address(address=address, prefix="0x")
    )
    return Wei(balance)


def get_xrc20_balance(address: str, token_address: str, network: str = config["network"],
                      provider: str = config["provider"]) -> Tuple[int, str, str, int, str]:
    """
    Get XinFin XRC20 token balance.

    :param address: XinFin address.
    :type address: str
    :param token_address: XinFin XRC20 token address.
    :type token_address: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: tuple -- XinFin XRC20 token balance and decimals.

    >>> from swap.providers.xinfin.rpc import get_xrc20_balance
    >>> get_xrc20_balance(address="xdc70c1eb09363603a3b6391deb2daa6d2561a62f52", token_address="xdcDaB6844e863bdfEE6AaFf888D2D34Bf1B7c37861", network="testnet")
    (99999999999999999999999999998, 18)
    """

    # Check parameter instances
    if not is_address(address=address):
        raise AddressError(f"Invalid XinFin '{address}' address.")
    elif not is_address(address=token_address):
        raise AddressError(f"Invalid XinFin XRC20 token '{token_address}' address.")

    # Get current working directory path (like linux or unix path).
    cwd: str = os.path.dirname(sys.modules[__package__].__file__)
    with open(f"{cwd}/contracts/libs/xrc20.json", "r") as xrc20_json_file:
        xrc20_contract_data: dict = json.loads(xrc20_json_file.read())["xrc20.sol:XRC20"]
        xrc20_json_file.close()

    web3: Web3 = get_web3(network=network, provider=provider)
    xrc20_token: Contract = web3.eth.contract(
        address=to_checksum_address(
            address=token_address, prefix="0x"
        ),
        abi=xrc20_contract_data["abi"]
    )
    try:
        name:   str = xrc20_token.functions.name().call()
        symbol: str = xrc20_token.functions.symbol().call()
        decimals: int = xrc20_token.functions.decimals().call()
        balance: int = xrc20_token.functions.balanceOf(
            to_checksum_address(address=to_checksum_address(address=address, prefix="0x"), prefix="0x")
        ).call()
        balance_str: str = str(balance)[:-decimals] + "." + str(balance)[-decimals:]
        return balance, name, symbol, decimals, balance_str
    except _web3.exceptions.BadFunctionCallOutput:
        return 0, "", "", 0, ".0"


def get_xrc20_decimals(token_address: str, network: str = config["network"], provider: str = config["provider"]) -> int:
    """
    Get XinFin XRC20 token decimals.

    :param token_address: XinFin XRC20 token address.
    :type token_address: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: int -- XinFin XRC20 token decimals.

    >>> from swap.providers.xinfin.rpc import get_xrc20_decimals
    >>> get_xrc20_decimals(token_address="0xDaB6844e863bdfEE6AaFf888D2D34Bf1B7c37861", network="testnet")
    18
    """

    # Check parameter instances
    if not is_address(address=token_address):
        raise AddressError(f"Invalid XinFin XRC20 token '{token_address}' address.")

    # Get current working directory path (like linux or unix path).
    cwd: str = os.path.dirname(sys.modules[__package__].__file__)
    with open(f"{cwd}/contracts/libs/xrc20.json", "r") as xrc20_json_file:
        xrc20_contract_data: dict = json.loads(xrc20_json_file.read())["xrc20.sol:XRC20"]
        xrc20_json_file.close()

    web3: Web3 = get_web3(network=network, provider=provider)
    xrc20_token: Contract = web3.eth.contract(
        address=to_checksum_address(
            address=token_address, prefix="0x"
        ),
        abi=xrc20_contract_data["abi"]
    )
    decimals: int = xrc20_token.functions.decimals().call()
    return decimals


def get_transaction(transaction_hash: str, network: str = config["network"],
                    provider: str = config["provider"]) -> dict:
    """
    Get XinFin transaction detail.

    :param transaction_hash: XinFin transaction hash/id.
    :type transaction_hash: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: dict -- XinFin transaction detail.

    >>> from swap.providers.xinfin.rpc import get_transaction
    >>> get_transaction(transaction_hash="0xa4d57071427e3310b3e2fb16e7712f8d8aaaafb31ce5fcd6534fc50848905948")
    {'hash': '0xa4d57071427e3310b3e2fb16e7712f8d8aaaafb31ce5fcd6534fc50848905948', 'nonce': 0, 'blockHash': '0xb33a804ae10713bf549db8ec749f7d650347613ac784db1a8d17e0cb03741bf0', 'blockNumber': 1, 'transactionIndex': 0, 'from': '0x96cA14396341480E3b6384D1d1397d1f7f5a0AB7', 'to': None, 'value': 0, 'gas': 367400, 'gasPrice': 250000000, 'input': '0x608060405234801561001057600080fd5b506040518060400160405280600581526020017f48656c6c6f0000000000000000000000000000000000000000000000000000008152506000908051906020019061005c929190610062565b50610166565b82805461006e90610105565b90600052602060002090601f01602090048101928261009057600085556100d7565b82601f106100a957805160ff19168380011785556100d7565b828001600101855582156100d7579182015b828111156100d65782518255916020019190600101906100bb565b5b5090506100e491906100e8565b5090565b5b808211156101015760008160009055506001016100e9565b5090565b6000600282049050600182168061011d57607f821691505b6020821081141561013157610130610137565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b61053b806101756000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063a413686214610046578063cfae321714610062578063ef690cc014610080575b600080fd5b610060600480360381019061005b91906102e3565b61009e565b005b61006a6100b8565b604051610077919061035d565b60405180910390f35b61008861014a565b604051610095919061035d565b60405180910390f35b80600090805190602001906100b49291906101d8565b5050565b6060600080546100c790610433565b80601f01602080910402602001604051908101604052809291908181526020018280546100f390610433565b80156101405780601f1061011557610100808354040283529160200191610140565b820191906000526020600020905b81548152906001019060200180831161012357829003601f168201915b5050505050905090565b6000805461015790610433565b80601f016020809104026020016040519081016040528092919081815260200182805461018390610433565b80156101d05780601f106101a5576101008083540402835291602001916101d0565b820191906000526020600020905b8154815290600101906020018083116101b357829003601f168201915b505050505081565b8280546101e490610433565b90600052602060002090601f016020900481019282610206576000855561024d565b82601f1061021f57805160ff191683800117855561024d565b8280016001018555821561024d579182015b8281111561024c578251825591602001919060010190610231565b5b50905061025a919061025e565b5090565b5b8082111561027757600081600090555060010161025f565b5090565b600061028e610289846103a4565b61037f565b9050828152602081018484840111156102a657600080fd5b6102b18482856103f1565b509392505050565b600082601f8301126102ca57600080fd5b81356102da84826020860161027b565b91505092915050565b6000602082840312156102f557600080fd5b600082013567ffffffffffffffff81111561030f57600080fd5b61031b848285016102b9565b91505092915050565b600061032f826103d5565b61033981856103e0565b9350610349818560208601610400565b610352816104f4565b840191505092915050565b600060208201905081810360008301526103778184610324565b905092915050565b600061038961039a565b90506103958282610465565b919050565b6000604051905090565b600067ffffffffffffffff8211156103bf576103be6104c5565b5b6103c8826104f4565b9050602081019050919050565b600081519050919050565b600082825260208201905092915050565b82818337600083830152505050565b60005b8381101561041e578082015181840152602081019050610403565b8381111561042d576000848401525b50505050565b6000600282049050600182168061044b57607f821691505b6020821081141561045f5761045e610496565b5b50919050565b61046e826104f4565b810181811067ffffffffffffffff8211171561048d5761048c6104c5565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f830116905091905056fea264697066735822122002786b5114bea14354170503b8bffe80a17bb5e4610cb41deca549935965f30864736f6c63430008030033', 'v': 28, 'r': '0xa593dcfd7f7b17f8b22907e9c4b03721312a4d00dfd99f8f7267ccd5eb7d4613', 's': '0x70cd172ae92de7a046dfe28de1db8657f8c3b3ed00c060392fb1d5080646927b'}
    """

    web3: Web3 = get_web3(network=network, provider=provider)
    transaction_detail_dict: dict = web3.eth.get_transaction(transaction_hash).__dict__
    for key, value in transaction_detail_dict.items():
        if isinstance(value, HexBytes):
            transaction_detail_dict[key] = transaction_detail_dict[key].hex()
    return transaction_detail_dict


def get_transaction_receipt(transaction_hash: str, network: str = config["network"], provider: str = config["provider"],
                            headers: dict = config["headers"], timeout: int = config["timeout"]) -> Optional[dict]:
    """
    Get XinFin transaction receipt.

    :param transaction_hash: XinFin transaction hash/id.
    :type transaction_hash: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- XinFin transaction receipt.

    >>> from swap.providers.xinfin.rpc import get_transaction_receipt
    >>> get_transaction_receipt(transaction_hash="0x5f4b11c11553cf040131b273c2bbc8c93d217269dd9b28393d5d0a3d623c1fcc", network="testnet")
    {'blockHash': '0x08d711ba038b97d0622d2c08b74dd2d9d2d00492116ead11452c12688618dcbc', 'blockNumber': '0x1e93914', 'contractAddress': None, 'cumulativeGasUsed': '0x5208', 'from': 'xdc95e80fc8ef98b92fe71514168c2e4b8f0ce38169', 'gasUsed': '0x5208', 'logs': [], 'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'status': '0x1', 'to': 'xdc2224caa2235df8da3d2016d2ab1137d2d548a232', 'transactionHash': '0x5f4b11c11553cf040131b273c2bbc8c93d217269dd9b28393d5d0a3d623c1fcc', 'transactionIndex': '0x0'}
    """

    if network in ["mainnet", "apothem"]:
        url = f"{config[network][provider]}/getTransactionReceipt"
        data = dict(
            jsonrpc="2.0", method="eth_getTransactionReceipt", params=[transaction_hash], id=1
        )
        response = requests.post(
            url=url, data=json.dumps(data), headers=headers, timeout=timeout
        )
        if response.status_code == 200:
            return response.json()["result"]
        raise APIError(response.status_code, response.content)
    else:
        web3: Web3 = get_web3(network=network, provider=provider)
        try:
            transaction_dict: dict = web3.eth.get_transaction_receipt(transaction_hash).__dict__
            for key, value in transaction_dict.items():
                if isinstance(value, HexBytes):
                    transaction_dict[key] = transaction_dict[key].hex()
            return transaction_dict
        except _web3.exceptions.TransactionNotFound:
            return None


def wait_for_transaction_receipt(transaction_hash: str, network: str = config["network"],
                                 timeout: int = config["timeout"], provider: str = config["provider"],
                                 headers: dict = config["headers"]) -> dict:
    """
    Wait for XinFin transaction receipt.

    :param transaction_hash: XinFin transaction hash/id.
    :type transaction_hash: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param timeout: request timeout, default to ``60``.
    :type timeout: int
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict

    :returns: dict -- XinFin transaction receipt.

    >>> from swap.providers.xinfin.rpc import wait_for_transaction_receipt
    >>> wait_for_transaction_receipt(transaction_hash="0x5f4b11c11553cf040131b273c2bbc8c93d217269dd9b28393d5d0a3d623c1fcc", timeout=120, network="testnet")
    {'blockHash': '0x08d711ba038b97d0622d2c08b74dd2d9d2d00492116ead11452c12688618dcbc', 'blockNumber': '0x1e93914', 'contractAddress': None, 'cumulativeGasUsed': '0x5208', 'from': 'xdc95e80fc8ef98b92fe71514168c2e4b8f0ce38169', 'gasUsed': '0x5208', 'logs': [], 'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'status': '0x1', 'to': 'xdc2224caa2235df8da3d2016d2ab1137d2d548a232', 'transactionHash': '0x5f4b11c11553cf040131b273c2bbc8c93d217269dd9b28393d5d0a3d623c1fcc', 'transactionIndex': '0x0'}
    """

    poll_latency: float = 0.1
    with Timeout(timeout) as _timeout:
        while True:
            txn_receipt = get_transaction_receipt(
                transaction_hash=transaction_hash, network=network, provider=provider, headers=headers
            )
            if txn_receipt is not None and txn_receipt['blockHash'] is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt


def decode_raw(raw: str) -> dict:
    """
    Decode original XinFin raw into blockchain.

    :param raw: XinFin transaction raw.
    :type raw: str

    :returns: dict -- XinFin decoded transaction hash.

    >>> from swap.providers.xinfin.rpc import decode_raw
    >>> decode_raw(raw="0xf86c02840ee6b280825208943e0a9b2ee8f8341a1aead3e7531d75f1e395f24b8901236efcbcbb340000801ba03084982e4a9dd897d3cc1b2c8cc2d1b106b9d302eb23f6fae7d0e57e53e043f8a0116f13f9ab385f6b53e7821b3335ced924a1ceb88303347cd0af4aa75e6bfb73")
    {'hash': '0x04b3bfb804f2b3329555c6f3a17a794b3f099b6435a9cf58c78609ed93853907', 'from': '0x3769F63e3b694cD2e973e28af59bdFd751303273', 'to': '0x3e0a9B2Ee8F8341A1aEaD3E7531d75f1e395F24b', 'nonce': 2, 'gas': 21000, 'gas_price': 250000000, 'value': 21000000000000000000, 'data': '0x', 'chain_id': -4, 'r': '0x3084982e4a9dd897d3cc1b2c8cc2d1b106b9d302eb23f6fae7d0e57e53e043f8', 's': '0x116f13f9ab385f6b53e7821b3335ced924a1ceb88303347cd0af4aa75e6bfb73', 'v': 27}
    """

    return dtr(transaction_raw=raw)


def submit_raw(raw: str, network: str = config["network"], provider: str = config["provider"]) -> str:
    """
    Submit original XinFin raw into blockchain.

    :param raw: XinFin transaction raw.
    :type raw: str
    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: str -- XinFin submitted transaction hash/id.

    >>> from swap.providers.xinfin.rpc import submit_raw
    >>> submit_raw(raw="0xf86c02840ee6b280825208943e0a9b2ee8f8341a1aead3e7531d75f1e395f24b8901236efcbcbb340000801ba03084982e4a9dd897d3cc1b2c8cc2d1b106b9d302eb23f6fae7d0e57e53e043f8a0116f13f9ab385f6b53e7821b3335ced924a1ceb88303347cd0af4aa75e6bfb73", network="testnet")
    "0x04b3bfb804f2b3329555c6f3a17a794b3f099b6435a9cf58c78609ed93853907"
    """

    web3: Web3 = get_web3(network=network, provider=provider)
    transaction_hash: HexBytes = web3.eth.send_raw_transaction(raw)
    return transaction_hash.hex()
