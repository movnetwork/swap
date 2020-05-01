#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet

import pytest


def test_mainnet_from_mnemonic():
    
    # Initialize bytom sender wallet
    bytom_wallet = Wallet(network="mainnet")\
        .from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
    
    seed = bytom_wallet.seed()
    assert seed == "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"

    xprivate_key = bytom_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_wallet.address()
    assert address == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"


def test_testnet_from_mnemonic():

    # Initialize bytom testnet wallet
    bytom_wallet = Wallet(network="testnet") \
        .from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")

    seed = bytom_wallet.seed()
    assert seed == "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"

    xprivate_key = bytom_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_wallet.address()
    assert address == "tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0"


def test_mainnet_from_seed():
    # Initialize bytom mainnet wallet
    bytom_mainnet_wallet = Wallet(network="mainnet") \
        .from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")

    xprivate_key = bytom_mainnet_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_mainnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_mainnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_mainnet_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_mainnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_mainnet_wallet.address()
    assert address == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"


def test_testnet_from_seed():
    # Initialize bytom sender wallet
    bytom_testnet_wallet = Wallet(network="testnet") \
        .from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")

    xprivate_key = bytom_testnet_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_testnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_testnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_testnet_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_testnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_testnet_wallet.address()
    assert address == "tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0"


def test_mainnet_from_xprivate_key():
    # Initialize bytom mainnet wallet
    bytom_mainnet_wallet = Wallet(network="mainnet") \
        .from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")

    xpublic_key = bytom_mainnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_mainnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    assert bytom_mainnet_wallet.path() == "m/44/153/1/0/1"

    public_key = bytom_mainnet_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_mainnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_mainnet_wallet.address()
    assert address == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"


def test_testnet_from_xprivate_key():
    # Initialize bytom sender wallet
    bytom_testnet_wallet = Wallet(network="testnet", path="m/44/153/1/0/1") \
        .from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")

    xpublic_key = bytom_testnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    assert bytom_testnet_wallet.path() == "m/44/153/1/0/1"

    expand_xprivate_key = bytom_testnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_testnet_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    program = bytom_testnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_testnet_wallet.address()
    assert address == "tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0"


def test_solonet_from_xprivate_key():
    # Initialize bytom sender wallet
    bytom_testnet_wallet = Wallet(network="solonet",
                                  indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"]) \
        .from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")

    xpublic_key = bytom_testnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    assert bytom_testnet_wallet.path() == "m/44/153/1/0/1"

    expand_xprivate_key = bytom_testnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_testnet_wallet.public_key()
    assert public_key == "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"

    assert bytom_testnet_wallet.indexes() == ["2c000000", "99000000", "01000000", "00000000", "01000000"]

    program = bytom_testnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_testnet_wallet.address()
    assert address == "sm1q9ndylx02syfwd7npehfxz4lddhzqsve2gdsdcs"

    private_key = bytom_testnet_wallet.private_key()
    assert private_key == "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"


def test_bytom_wallet_tools():
    wallet = Wallet(network="mainnet", indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"])
    wallet.from_xpublic_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b"
                            "6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    assert wallet.address() == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"

    assert wallet.path() == "m/44/153/1/0/1"
    assert isinstance(wallet.guid(), str)

    wallet = Wallet(network="solonet")
    wallet.from_entropy("063679ca1b28b5cfda9c186b367e271e")
    assert wallet.address() == "sm1qzq3k0cg89qudwnlxs7frykxg0r357kupzccnzv"
    assert wallet.path() == "m/44/153/1/0/1"

    wallet = Wallet(network="testnet")
    wallet.from_guid(guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b")

    wallet = Wallet(network="mainnet")
    wallet.from_public_key("91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2")
    assert wallet.address() == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"

    assert wallet.path() is None
    assert wallet.seed() is None
    assert wallet.xprivate_key() is None
    assert wallet.xpublic_key() is None
    assert wallet.expand_xprivate_key() is None
    assert isinstance(wallet.balance(), int)


def test_bytom_wallet_error():

    with pytest.raises(ValueError, match=r"invalid network, .*"):
        Wallet(network="unknown")

    with pytest.raises(TypeError, match="derivation change must be boolean format."):
        Wallet(network="solonet", change=1)

