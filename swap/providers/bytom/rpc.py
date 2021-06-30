#!/usr/bin/env python3

from typing import (
    Optional, Union
)

import requests
import json

from ...exceptions import (
    BalanceError, APIError, NetworkError, AddressError
)
from ..config import bytom as config
from .assets import AssetNamespace
from .utils import (
    is_network, is_address, amount_unit_converter, get_address_type
)


def get_balance(address: str, asset: Union[str, AssetNamespace] = config["asset"], network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Bytom balance.

    :param address: Bytom address.
    :type address: str
    :param asset: Bytom asset, default to ``BTM``.
    :type asset: str, bytom.assets.AssetNamespace
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: int -- Bytom asset balance (NEU amount).

    >>> from swap.providers.bytom.rpc import get_balance
    >>> from swap.providers.bytom.assets import BTM as ASSET
    >>> get_balance(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", asset=ASSET, network="mainnet")
    71560900
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/address/{address}/asset"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json is None:
        return 0
    for _asset in response_json:
        if (str(asset.ID) if isinstance(asset, AssetNamespace) else asset) == _asset["asset_id"]:
            return int(_asset["balance"])
    return 0


def get_utxos(program: str, network: str = config["network"], asset: Union[str, AssetNamespace] = config["asset"],
              limit: int = 15, by: str = "amount", order: str = "desc",
              headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Bytom unspent transaction outputs (UTXO's).

    :param program: Bytom control program.
    :type program: str
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param asset: Bytom asset id, defaults to ``BTM``.
    :type asset: str, bytom.assets.AssetNamespace
    :param limit: Bytom utxo's limit, defaults to ``15``.
    :type limit: int
    :param by: Sort by, defaults to ``amount``.
    :type by: str
    :param order: Sort order, defaults to ``desc``.
    :type order: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: list -- Bytom unspent transaction outputs (UTXO's).

    >>> from swap.providers.bytom.rpc import get_utxos
    >>> get_utxos(program="00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", network="mainnet")
    [{'hash': '7c1e20e6ff719176a3ed6f5332ec3ff665ab28754d2511950e591267e0e675df', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 71510800}, {'hash': '01b07c3523085b75f1e047be3a73b263635d0b86f9b751457a51b26c5a97a110', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 50000}, {'hash': 'e46cfecc1f1a26413172ce81c78affb19408e613915642fa5fb04d3b0a4ffa65', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 100}]
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
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
    Estimate Bytom transaction fee.

    :param address: Bytom address.
    :type address: str
    :param amount: Bytom amount (NEU amount).
    :type amount: int
    :param asset: Bytom asset id, default to ``BTM``.
    :type asset: str, bytom.assets.AssetNamespace
    :param confirmations: Bytom confirmations, default to ``1``.
    :type confirmations: int
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: request timeout, default to ``60``.
    :type timeout: int

    :returns: str -- Estimated transaction fee (NEU amount).

    >>> from swap.providers.bytom.rpc import estimate_transaction_fee
    >>> from swap.providers.bytom.assets import BTM as ASSET
    >>> estimate_transaction_fee(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", asset=ASSET, amount=100_000, confirmations=100, network="mainnet")
    449000
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")

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
    elif response.status_code == 200 and response.json()["code"] == 504:
        raise BalanceError("Insufficient spend UTXO's", "you don't have enough amount.")
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
    Build Bytom transaction.

    :param address: Bytom address.
    :type address: str
    :param transaction: Bytom transaction (inputs, outputs, fee, confirmations & forbid_chain_tx).
    :type transaction: dict
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bytom builted transaction.

    >>> from swap.providers.bytom.rpc import build_transaction
    >>> build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", transaction={"fee": "0.1", "confirmations": 1, "inputs": [{"type": "spend_wallet", "amount": "0.0001", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}], "outputs": [{"type": "control_address", "amount": "0.0001", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8"}]}, network="mainnet")
    {'tx': {'hash': '5d4ae68487953863783599045f99eb8740b5745376ed8d8926d68de695e72476', 'status': True, 'size': 404, 'submission_timestamp': 0, 'memo': '', 'inputs': [{'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.0005', 'type': 'spend'}, {'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.715108', 'type': 'spend'}], 'outputs': [{'utxo_id': '0d5c097b8e75f711765ff63017fe8a4a987d8b50f7ca3a5d1873120af5f46116', 'script': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.0001', 'type': 'control'}, {'utxo_id': 'c49da44ef15d227ca978191e91d5d8915a3f92baf6b5778b7377deb2bddca554', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx', 'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '0.615908', 'type': 'control'}], 'fee': '0.0996', 'balances': [{'asset': {'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'decimals': 0, 'unit': 'BTM'}, 'amount': '-0.0001'}], 'types': ['ordinary'], 'min_veto_height': 0}, 'raw_transaction': '07010002015e015c88650475abf87eb364f93c608db879ad71643fbc7725ded246e8883e79c75a78ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd0860300011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2015f015da72ea4ad87d7b5a51534c07edc005887345ef38fac8d258987dd17268e8d0336ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff90d68c2201011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020146ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff909aaf1d011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00', 'signing_instructions': [{'derivation_path': ['2c000000', '99000000', '01000000', '00000000', '01000000'], 'sign_data': ['a5da2ae06bfaea9854423fe9cc544d775854cf57827c8c2ab606418452d30209'], 'pubkey': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'}, {'derivation_path': ['2c000000', '99000000', '01000000', '00000000', '01000000'], 'sign_data': ['3e44203712c4e981783810875fa67f2efe0afda38afe229fd09da0d113c3d885'], 'pubkey': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'}]}
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
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
    Get Bytom transaction detail.

    :param transaction_hash: Bytom transaction hash/id.
    :type transaction_hash: str
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bytom transaction detail.

    >>> from swap.providers.bytom.rpc import get_transaction
    >>> get_transaction(transaction_hash="bc935995cb3408b51aa3d05e7e77226840eb68340b229f9c561edae31ebc8b95", network="mainnet")
    {'id': 'bc935995cb3408b51aa3d05e7e77226840eb68340b229f9c561edae31ebc8b95', 'timestamp': 1524765978, 'block_height': 3487, 'trx_amount': 41249562600, 'trx_fee': 437400, 'status_fail': False, 'coinbase': False, 'size': 332, 'chain_status': 'mainnet', 'time_range': 0, 'index_id': 3489, 'mux_id': '305a28d8d34b40c65936810f9e9c1f8bc9c793ec2e72c70f9203fbbeb0a56db9', 'inputs': [{'txtype': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 41250000000, 'control_program': '0014151df3db084d909ccb55d45d4e59db2e17e5f237', 'address': 'bm1qz5wl8kcgfkgfej6463w5ukwm9ct7tu3ht8p7te', 'spent_output_id': '6def8e6a7c29ccff4c5596a37a6698b71f392bf713bc67bb3fa0af54bf50f815', 'input_id': 'fb226e3ad39e38341f0d232c910065b76ef7c267faa3ea4e49a31836405b6747', 'witness_arguments': ['1848cb550620b971fd244eb625ccf4507ccd9944da65b47674550397c983247e1bd3ff880782beca963a81c34c17c8ef664e2501a11cdd9097300e44567ff10f', '268402537b02d91fafdcdeb6eda3aa542548d77cd6cccb38ecd7ea7ce8a22cf7'], 'asset_name': 'BTM', 'asset_definition': '{}', 'cross_chain_asset': False, 'asset_decimals': 8}], 'outputs': [{'txtype': 'control', 'id': 'a8a7b5363379dee8ff77da7c4acf63dc3469a79ebaade079fc1842543964c6e9', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 41239562600, 'control_program': '0014fc22634a713ac1e6f831c56184f847b7546fbda4', 'address': 'bm1qls3xxjn38tq7d7p3c4scf7z8ka2xl0dyppj52k', 'asset_name': 'BTM', 'asset_definition': '{}', 'cross_chain_asset': False, 'position': 0, 'asset_decimals': 8}, {'txtype': 'control', 'id': '84287fb5b2b461dbd3b937a9013d89c0d54a21768e31fb8345b02d57a7992533', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000000, 'control_program': '00140e43a92a9e8aca788eb1551c316448c2e3f78215', 'address': 'bm1qpep6j2573t983r4325wrzezgct3l0qs4q04pem', 'asset_name': 'BTM', 'asset_definition': '{}', 'cross_chain_asset': False, 'position': 1, 'asset_decimals': 8}], 'confirmations': 558509}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/transaction/{transaction_hash}"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["inputs"] is not None:
        return response.json()
    raise APIError(f"Not found this '{transaction_hash}' transaction hash.", 500)


def get_current_block_height(plus: int = 0, network: str = config["network"],
                             headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Bytom transaction detail.

    :param plus: Add block number on current block height, default to ``0``.
    :type plus: int
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: int -- Bytom current block height.

    >>> from swap.providers.bytom.rpc import get_current_block_height
    >>> get_current_block_height(plus=0)
    678722
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/latest-block"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.status_code == 200:
        return int(response.json()["block"]["height"]) \
            if plus == 0 else int(response.json()["block"]["height"]) + plus
    raise APIError("Can't get current latest Bytom block height.")


def find_p2wsh_utxo(transaction: dict) -> Optional[dict]:
    """
    Find Bytom pay to witness script hash UTXO info's.

    :param transaction: Bytom transaction detail.
    :type transaction: dict

    :returns: dict -- Pay to Witness Secript Hash (P2WSH) UTXO info's.

    >>> from swap.providers.bytom.rpc import find_p2wsh_utxo, get_transaction
    >>> find_p2wsh_utxo(transaction=get_transaction(transaction_hash="b6d12407bbd238938941246fd0dd3e5234f1e3c370bef3fcbc1f60ebee022e76", network="mainnet"))
    {'txtype': 'control', 'id': 'a1c5cce9df9343a10dafa582dea04e61c402ee8398b5268ba5c9c3aefd58017a', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10499000, 'control_program': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8', 'asset_name': 'BTM', 'asset_definition': '{}', 'cross_chain_asset': False, 'position': 0, 'asset_decimals': 8}
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
    Decode original Bytom raw.

    :param raw: Bytom transaction raw.
    :type raw: str
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bytom decoded transaction raw.

    >>> from swap.providers.bytom.rpc import decode_raw
    >>> decode_raw(raw="07010002015e015c88650475abf87eb364f93c608db879ad71643fbc7725ded246e8883e79c75a78ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd0860300011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2015f015da72ea4ad87d7b5a51534c07edc005887345ef38fac8d258987dd17268e8d0336ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff90d68c2201011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020146ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff909aaf1d011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", network="testnet")
    {'tx_id': '5d4ae68487953863783599045f99eb8740b5745376ed8d8926d68de695e72476', 'version': 1, 'size': 404, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 50000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx', 'spent_output_id': '01b07c3523085b75f1e047be3a73b263635d0b86f9b751457a51b26c5a97a110', 'input_id': 'de193c78772c93356f81a5061a90d8dcfba84d03ae4d78b2a57a9201f88c38af', 'witness_arguments': ['91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'], 'sign_data': 'a5da2ae06bfaea9854423fe9cc544d775854cf57827c8c2ab606418452d30209'}, {'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 71510800, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx', 'spent_output_id': '7c1e20e6ff719176a3ed6f5332ec3ff665ab28754d2511950e591267e0e675df', 'input_id': 'de2c7bcf9caf00f78ca8e316cf37cf88c86b0457e47cf58e2465d783151abd0e', 'witness_arguments': ['91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'], 'sign_data': '3e44203712c4e981783810875fa67f2efe0afda38afe229fd09da0d113c3d885'}], 'outputs': [{'type': 'control', 'id': '0d5c097b8e75f711765ff63017fe8a4a987d8b50f7ca3a5d1873120af5f46116', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc', 'address': 'bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8'}, {'type': 'control', 'id': 'c49da44ef15d227ca978191e91d5d8915a3f92baf6b5778b7377deb2bddca554', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 61590800, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx'}], 'fee': 9960000}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['bytom-core']}/decode-raw-transaction"
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
     Submit original Bytom raw into blockchain.

    :param address: Bytom address.
    :type address: str
    :param raw: Bytom transaction raw.
    :type raw: str
    :param signatures: Bytom signed massage datas.
    :type signatures: list
    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: str -- Bytom submitted transaction id/hash.

    >>> from swap.providers.bytom.rpc import submit_raw
    >>> submit_raw(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", raw="07010002015e015c88650475abf87eb364f93c608db879ad71643fbc7725ded246e8883e79c75a78ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd0860300011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2015f015da72ea4ad87d7b5a51534c07edc005887345ef38fac8d258987dd17268e8d0336ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff90d68c2201011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020146ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff909aaf1d011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", signatures=[["f8466336a79d166e47fb5d64f1e7ec01b203b59b3ee86686492bd1e4d0bdd642dfe4a575049071a052a441635c336708ab7d869cccd5331bc29f60e0ed9cd80d"], ["ebf33fbda5c2f3d144e90c3b763b1e7e42d501e595216fcd2b310b089918bae2ef4c7b8a2e1f650ee741578aba7960706d2bf9be7dffbf0fe77199075f155909"]], network="mainnet")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v3']}/merchant/submit-payment"
    data = dict(raw_transaction=raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]["tx_hash"]
