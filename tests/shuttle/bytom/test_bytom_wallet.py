#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet


def test_mainnet_from_mnemonic():
    
    # Initialize bytom sender wallet
    bytom_wallet = Wallet(network="mainnet")\
        .from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
    
    seed = bytom_wallet.seed().hex()
    assert seed == "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"

    xprivate_key = bytom_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_wallet.public_key()
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

    program = bytom_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_wallet.address()
    assert address == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"


def test_testnet_from_mnemonic():

    # Initialize bytom testnet wallet
    bytom_wallet = Wallet(network="testnet") \
        .from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")

    seed = bytom_wallet.seed().hex()
    assert seed == "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"

    xprivate_key = bytom_wallet.xprivate_key()
    assert xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    xpublic_key = bytom_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_wallet.public_key()
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

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
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

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
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

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

    public_key = bytom_mainnet_wallet.public_key()
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

    program = bytom_mainnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_mainnet_wallet.address()
    assert address == "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"


def test_testnet_from_xprivate_key():
    # Initialize bytom sender wallet
    bytom_testnet_wallet = Wallet(network="testnet") \
        .from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")

    xpublic_key = bytom_testnet_wallet.xpublic_key()
    assert xpublic_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"

    expand_xprivate_key = bytom_testnet_wallet.expand_xprivate_key()
    assert expand_xprivate_key == "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"

    public_key = bytom_testnet_wallet.public_key()
    assert public_key == "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5"

    program = bytom_testnet_wallet.program()
    assert program == "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"

    address = bytom_testnet_wallet.address()
    assert address == "tm1q9ndylx02syfwd7npehfxz4lddhzqsve2d2mgc0"
