#!/usr/bin/env python3

from typing import (
    List, Optional
)

from ...utils import NestedNamespace


class AssetNamespace(NestedNamespace):

    NAME: Optional[str] = None
    ID: str  # Asset ID is required
    SYMBOL: Optional[str] = None


BTM: AssetNamespace = AssetNamespace({
    "NAME": "Bytom",
    "ID": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "SYMBOL": "BTM"
})

BTC: AssetNamespace = AssetNamespace({
    "NAME": "Bitcoin",
    "ID": "bda946b3110fa46fd94346ce3f05f0760f1b9de72e238835bc4d19f9d64f1742",
    "SYMBOL": "BTC"
})

DAI: AssetNamespace = AssetNamespace({
    "NAME": "Dai Stablecoin",
    "ID": "25f2069140fa3ff4d6e0dc1d0fcaa11ace01eb721f115f0f1a5a3782db597fb1",
    "SYMBOL": "DAI"
})

ETH: AssetNamespace = AssetNamespace({
    "NAME": "Ethereum",
    "ID": "78de44ffa1bce37b757c9eae8925b5f199dc4621b412ef0f3f46168865284a93",
    "SYMBOL": "ETH"
})

LTC: AssetNamespace = AssetNamespace({
    "NAME": "Litecoin",
    "ID": "011a24f9da7551d4cd9ae0f194aa1d1691e22a173edf7d81aabd9a97ca386252",
    "SYMBOL": "LTC"
})

SUP: AssetNamespace = AssetNamespace({
    "NAME": "SUP",
    "ID": "47fcd4d7c22d1d38931a6cd7767156babbd5f05bbbb3f7d3900635b56eb1b67e",
    "SYMBOL": "SUP"
})

USDC: AssetNamespace = AssetNamespace({
    "NAME": "USD Coin",
    "ID": "c4644dd6643475d57ed624f63129ab815f282b61f4bb07646d73423a6e1a1563",
    "SYMBOL": "USDC"
})

USDT: AssetNamespace = AssetNamespace({
    "NAME": "Tether",
    "ID": "184e1cc4ee4845023888810a79eed7a42c02c544cf2c61ceac05e176d575bd46",
    "SYMBOL": "USDT"
})


__all__:  List[AssetNamespace] = [
    BTM, BTC, DAI, ETH, LTC, SUP, USDC, USDT
]
