#!/usr/bin/env python3

from typing import (
    Optional, Union
)

import requests
import json

from ...exceptions import (
    BalanceError, APIError, NetworkError, AddressError
)
from ..config import vapor as config
from .assets import AssetNamespace
from .utils import (
    is_network, is_address, amount_unit_converter, get_address_type
)


def get_balance(address: str, asset: Union[str, AssetNamespace] = config["asset"], network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Vapor balance.

    :param address: Vapor address.
    :type address: str
    :param asset: Vapor asset, default to ``BTM``.
    :type asset: str, vapor.assets.AssetNamespace
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: int -- Vapor asset balance (NEU amount).

    >>> from swap.providers.vapor.rpc import get_balance
    >>> from swap.providers.vapor.assets import BTM as ASSET
    >>> get_balance(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", asset=ASSET, network="mainnet")
    97000000
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/address/{address}"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.json() is None or response.json()["data"] is None:
        return 0
    for _asset in response.json()["data"]["address"]:
        if (str(asset.ID) if isinstance(asset, AssetNamespace) else asset) == _asset["asset_id"]:
            return int(_asset["balance"])
    return 0


def get_utxos(program: str, asset: Union[str, AssetNamespace] = config["asset"], network: str = config["network"],
              limit: int = 15, by: str = "amount", order: str = "desc",
              headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Vapor unspent transaction outputs (UTXO's).

    :param program: Vapor control program.
    :type program: str
    :param asset: Vapor asset id, defaults to ``BTM``.
    :type asset: str, vapor.assets.AssetNamespace
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param limit: Vapor utxo's limit, defaults to ``15``.
    :type limit: int
    :param by: Sort by, defaults to ``amount``.
    :type by: str
    :param order: Sort order, defaults to ``desc``.
    :type order: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: list -- Vapor unspent transaction outputs (UTXO's).

    >>> from swap.providers.vapor.rpc import get_utxos
    >>> from swap.providers.vapor.assets import BTM as ASSET
    >>> get_utxos(program="00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", asset=ASSET, network="mainnet")
    [{'hash': 'e152f88d33c6659ad823d15c5c65b2ed946d207c42430022cba9bb9b9d70a7a4', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 587639800}, {'hash': '88289fa4c7633574931be7ce4102aeb24def0de20e38e7d69a5ddd6efc116b95', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 8160000}, {'hash': 'f71c68f921b434cc2bcd469d26e7927aa6db7500e4cdeef814884f11c10f5de2', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}, {'hash': 'e46cfecc1f1a26413172ce81c78affb19408e613915642fa5fb04d3b0a4ffa65', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 100}]
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/q/utxos"
    data = dict(filter=dict(
        script=program, asset=(str(asset.ID) if isinstance(asset, AssetNamespace) else asset)
    ), sort=dict(by=by, order=order))
    params = dict(limit=limit)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json["data"]


def estimate_transaction_fee(address: str, amount: int, asset: Union[str, AssetNamespace] = config["asset"],
                             confirmations: int = config["confirmations"], network: str = config["network"],
                             headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Estimate Vapor transaction fee.

    :param address: Vapor address.
    :type address: str
    :param amount: Vapor amount (NEU amount).
    :type amount: int
    :param asset: Vapor asset id, default to ``BTM``.
    :type asset: str, vapor.assets.AssetNamespace
    :param confirmations: Vapor confirmations, default to ``1``.
    :type confirmations: int
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: request timeout, default to ``60``.
    :type timeout: int

    :returns: str -- Estimated transaction fee (NEU amount).

    >>> from swap.providers.vapor.rpc import estimate_transaction_fee
    >>> from swap.providers.vapor.assets import BTM as ASSET
    >>> estimate_transaction_fee(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", asset=ASSET, amount=100_000, confirmations=100, network="mainnet")
    449000
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")

    url = f"{config[network]['blockcenter']}/merchant/estimate-tx-fee"
    data = dict(
        asset_amounts={
            (str(asset.ID) if isinstance(asset, AssetNamespace) else asset): str(amount_unit_converter(
                amount=amount, unit_from="NEU2BTM"
            ))
        },
        confirmations=confirmations
    )
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return amount_unit_converter(amount=float(response.json()["data"]["fee"]), unit_from="BTM2NEU")
    raise APIError(response.json()["msg"], response.json()["code"])


def account_create(xpublic_key: str, label: str = "1st address", account_index: int = 1,
                   network: str = config["network"], headers: dict = config["headers"],
                   timeout: int = config["timeout"]) -> dict:
    """
    Create account in blockcenter.

    :param xpublic_key: Bytom xpublic key.
    :type xpublic_key: str
    :param label: Bytom limit, defaults to ``1st address``.
    :type label: str
    :param account_index: Account index, defaults to ``1``.
    :type account_index: str
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bytom blockcenter guid, address and label.

    >>> from swap.providers.bytom.rpc import account_create
    >>> account_create(xpublic_key="f80a401807fde1ee5727ae032ee144e4b757e69431e68e6cd732eda3c8cd3936daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", network="mainnet")
    {"guid": "9ed61a9b-e7b6-4cb7-94fb-932b738e4f66", "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", "label": "1st address"}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/account/create"
    data = dict(pubkey=xpublic_key, label=label, account_index=account_index)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return response.json()["data"]
    raise APIError(response.json()["msg"], response.json()["code"])


def build_transaction(address: str, transaction: dict, network: str = config["network"],
                      headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Build Vapor transaction.

    :param address: Vapor address.
    :type address: str
    :param transaction: Vapor transaction (inputs, outputs, fee, confirmations & forbid_chain_tx).
    :type transaction: dict
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Vapor builted transaction.

    >>> from swap.providers.vapor.rpc import build_transaction
    >>> build_transaction(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", transaction={"fee": "0.1", "confirmations": 1, "inputs": [{"type": "spend_wallet", "amount": "0.1", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}], "outputs": [{"type": "control_address", "amount": "0.1", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "address": "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37"}]}, network="mainnet")
    {'tx': {'hash': 'f6b35e2f37862bc9a2cfbc9f21440102599fc5860ed73ba5c3f44e17408e2c8c', 'status': True, 'size': 279, 'submission_timestamp': 0, 'memo': '', 'inputs': [{'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.9', 'type': 'spend'}], 'outputs': [{'utxo_id': '793540933493c531efdc0dfd89d95041badc4e1efaf938d9916cdc7834984c74', 'script': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.1', 'type': 'control'}, {'utxo_id': '62c391358a7bccac6a3a1b9efd5339eb7207660372290ceb8718af2284467ba0', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.7', 'type': 'control'}], 'fee': '0.1', 'balances': [{'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '-0.1'}], 'types': ['ordinary'], 'min_veto_height': 0}, 'raw_transaction': '07010001015f015d0c8382b6aadd32748d0a9490259bf9ba5b55f6ac283535f8752cf5d51621801cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8095f52a00011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202014a0048ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade204012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013e003cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80bbb021011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00', 'signing_instructions': [{'derivation_path': ['2c000000', '99000000', '01000000', '00000000', '01000000'], 'sign_data': ['4491d22111d3b75faa8f65ab23cd4b221fd14c99b1260239e3398ab3c347a769'], 'pubkey': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'}]}
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction), params=params, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 422:
        raise BalanceError(f"There is no any asset balance recorded on this '{address}' address.")
    elif response.status_code == 200 and response.json()["code"] == 515:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    elif response.status_code == 200 and response.json()["code"] == 504:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    return response.json()["data"][0]


def get_transaction(transaction_hash: str, network: str = config["network"],
                    headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get Vapor transaction detail.

    :param transaction_hash: Vapor transaction hash/id.
    :type transaction_hash: str
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Vapor transaction detail.

    >>> from swap.providers.vapor.rpc import get_transaction
    >>> get_transaction(transaction_hash="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="mainnet")
    {'tx_id': '961d984b04214dc202fb40f4c48466d10a2813a138a31e1d2877ad3b6af0ef4c', 'timestamp': 1606993457000, 'block_hash': '440e791390f61c615b974c9292ac1d43bad67368076ef6d86a77cab22f1c2119', 'block_height': 85098064, 'trx_amount': 0, 'trx_fee': 10000000, 'status_fail': False, 'is_vote': False, 'is_cross_chain': False, 'coinbase': 0, 'size': 646, 'chain_status': 'mainnet', 'index_id': 18811685, 'mux_id': '97fdbe17d62ae8f8f2024ebc6a231183e8ce7c4e8fde5645b9a3c973f8d0d3ad', 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000, 'control_program': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37', 'spent_output_id': 'c30e26caef4ad3436542700c5b32a91cdf0622c60a6c8a6e11cb1c0b250bc65f', 'input_id': 'c470139ab9f9e81829e51096c57365392195ea2e90d7fb19e9eb2b309df22425', 'witness_arguments': ['db718488496e0823b1cfd9ce64f226ffc4e9debd30eac0b751aa6bd28f694908ae0c0f5d39dd6ed697cae9b0857832ffcb9989487eea81d49d5f2a1228425205', '01', '02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0'], 'decode_program': ['DUP ', 'SHA3 ', 'DATA_32 4f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'EQUALVERIFY ', 'DATA_8 ffffffffffffffff', 'SWAP ', 'FALSE ', 'CHECKPREDICATE '], 'decimals': 8, 'unit': 'BTM'}, {'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 16990000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'spent_output_id': '1a7f2357f2ec272ea2d96413aee511d2077447731a799110cef97de177739181', 'input_id': '4f50c438b5006eafc547cc48128cb94d2e39430ef30f117aa85e6f30ac92ce09', 'witness_arguments': ['e31abbf90f8b20cb41f4daedc2f558dedcbc258fcfb9a36ae1f8c0b4b80f448a78d1d835adb02cc918374c71df8c02c52b425b18d14601ad11e5f0ad8eb00a07', '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'], 'decode_program': ['DUP ', 'HASH160 ', 'DATA_20 2cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'EQUALVERIFY ', 'TXSIGHASH ', 'SWAP ', 'CHECKSIG '], 'decimals': 8, 'unit': 'BTM'}], 'outputs': [{'type': 'control', 'id': '20c00b6f9f4fc4f22ccee6c5f8b471a72b1f514f821b1c9c3d1f3243ff011cf1', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'decimals': 8, 'decode_program': ['DUP ', 'HASH160 ', 'DATA_20 2cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'EQUALVERIFY ', 'TXSIGHASH ', 'SWAP ', 'CHECKSIG '], 'unit': 'BTM'}, {'type': 'control', 'id': 'f7a36ebce7001e83510eb16c13ff0e5ef311179c25e8cf7bcb599ff8d17e23b2', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 6990000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'decimals': 8, 'decode_program': ['DUP ', 'HASH160 ', 'DATA_20 2cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'EQUALVERIFY ', 'TXSIGHASH ', 'SWAP ', 'CHECKSIG '], 'unit': 'BTM'}], 'mov_type': ''}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/tx/hash/{transaction_hash}"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return response.json()["data"]["transaction"]
    raise APIError(f"Not found this '{transaction_hash}' vapor transaction id.", 500)


def get_current_block_height(plus: int = 0, network: str = config["network"],
                             headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Vapor transaction detail.

    :param plus: Add block number on current block height, default to ``0``.
    :type plus: int
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: int -- Vapor current block height.

    >>> from swap.providers.vapor.rpc import get_current_block_height
    >>> get_current_block_height(plus=0)
    678722
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/block"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return int(response.json()["data"]["block"]["height"]) \
            if plus == 0 else int(response.json()["data"]["block"]["height"]) + plus
    raise APIError("Can't get current latest Vapor block height.")


def find_p2wsh_utxo(transaction: dict) -> Optional[dict]:
    """
    Find Vapor pay to witness script hash UTXO info's.

    :param transaction: Vapor transaction detail.
    :type transaction: dict

    :returns: dict -- Pay to Witness Secript Hash (P2WSH) UTXO info's.

    >>> from swap.providers.vapor.rpc import find_p2wsh_utxo, get_transaction
    >>> find_p2wsh_utxo(transaction=get_transaction("28168825b2eaded02973313b1c4152a6362157590ec8cd3f530306259eb390ce", "mainnet"))
    {'type': 'control', 'id': 'e99f811f25837d0472321e4e237631f40912bf4ca40766a46c8064ccff77d03a', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10499000, 'control_program': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37', 'decimals': 8, 'decode_program': ['DUP ', 'SHA3 ', 'DATA_32 4f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'EQUALVERIFY ', 'DATA_8 ffffffffffffffff', 'SWAP ', 'FALSE ', 'CHECKPREDICATE '], 'unit': 'BTM'}
    """

    transaction_outputs, utxo = transaction["outputs"], None
    for transaction_output in transaction_outputs:
        if get_address_type(transaction_output["address"]) == "p2wsh":
            utxo = transaction_output
            break
    return utxo


def decode_raw(raw: str, network: str = config["network"], 
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode original Vapor raw.

    :param raw: Vapor transaction raw.
    :type raw: str
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Vapor decoded transaction raw.

    >>> from swap.providers.vapor.rpc import decode_raw
    >>> decode_raw(raw="07010001015f015d0c8382b6aadd32748d0a9490259bf9ba5b55f6ac283535f8752cf5d51621801cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8095f52a00011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202014a0048ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade204012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013e003cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80bbb021011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", network="testnet")
    {'tx_id': 'f6b35e2f37862bc9a2cfbc9f21440102599fc5860ed73ba5c3f44e17408e2c8c', 'version': 1, 'size': 279, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 90000000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag', 'spent_output_id': 'f337ffe5333849636e7f6ca01b8a3aa0ef8cc50fadf875730cd40786bb504f80', 'input_id': '437cebc2dbdff6f5c821fbf6895455192685411bca64f796ff389554e0c23f44', 'witness_arguments': ['91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2']}], 'outputs': [{'type': 'control', 'id': '793540933493c531efdc0dfd89d95041badc4e1efaf938d9916cdc7834984c74', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000000, 'control_program': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37'}, {'type': 'control', 'id': '62c391358a7bccac6a3a1b9efd5339eb7207660372290ceb8718af2284467ba0', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 70000000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag'}], 'fee': 10000000}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['vapor-core']}/decode-raw-transaction"
    data = dict(raw_transaction=raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 400:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]


def submit_raw(address: str, raw: str, signatures: list, network: str = config["network"],
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> str:
    """
     Submit original Vapor raw into blockchain.

    :param address: Vapor address.
    :type address: str
    :param raw: Vapor transaction raw.
    :type raw: str
    :param signatures: Vapor signed massage datas.
    :type signatures: list
    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: str -- Vapor submitted transaction id/hash.

    >>> from swap.providers.vapor.rpc import submit_raw
    >>> submit_raw(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", raw="07010001015f015d0c8382b6aadd32748d0a9490259bf9ba5b55f6ac283535f8752cf5d51621801cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8095f52a00011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202014a0048ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade204012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013e003cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80bbb021011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", signatures=[["31818788bd6cfd255643242212efc1239db8f9dcd91b0e07ef1ddd38d8edf98c420da5578ec195ff7a5ddd72605a1973c040f2345ea630e0e584e28738ad3f03"]], network="mainnet")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json: dict = response.json()
    if response_json["code"] != 200 and response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]["tx_hash"]
