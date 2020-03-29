============================
Command Line Interface (CLI)
============================

:$ shuttle:
    **Option Commands**

    :-h, ---help:
        Print a short description of all command line options.

    :-v, ---version:
        Print the PyShuttle version number and exit. Example output could be:
        ::

            PyShuttle version 0.1.2


Bitcoin CLI
===========

:$ shuttle bitcoin:

    **Option Commands**

    :-h, ---help:
        Print a short description of bitcoin command line options.

    ::

        Usage: shuttle bitcoin [OPTIONS] COMMAND [ARGS]...

          SHUTTLE BITCOIN

        Options:
          -h, --help  Show this message and exit.

        Commands:
          decode  Select bitcoin transaction raw decoder.
          sign    Select bitcoin transaction raw signer.
          submit  Select bitcoin submit transaction raw.

Decode Command
---------------------

:$ shuttle bitcoin decode:

    Bitcoin transaction raw decoder.

    **Option Commands**

    :-h, ---help:
        Print a short description of bitcoin decode command line options.

    **Required Commands**

    :-r, ---raw:
        (str) – Bitcoin transaction raw.

    ::

        $ shuttle bitcoin decode --raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRkZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFvRHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0
        [SUCCESS] {"hex": "020000000168279838aa4eb9c4d1479a07b46a1e9ee61379855b159a53d75688e0ff09a7f70000000000ffffffff017c000000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000", "txid": "efeb2be0dc1dc0dba9ac882ce0e73c64f7fe09d5b3185b122849b38d124101f5", "hash": "efeb2be0dc1dc0dba9ac882ce0e73c64f7fe09d5b3185b122849b38d124101f5", "size": 85, "vsize": 85, "version": 2, "locktime": 0, "vin": [{"txid": "f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768", "vout": 0, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00000124", "n": 0, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac", "type": "p2pkh", "address": "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB"}}]}


Sign Command
------------------

:$ shuttle bitcoin sign:

    Bitcoin transaction raw signer.

    **Option Commands**

    :-h, ---help:
        Print a short description of bitcoin sign command line options.
    :-s, ---secret:
        (str) – Secret key for Claim/Refund.

    **Required Commands**

    :-r, ---raw:
        (str) – Bitcoin transaction raw.
    :-p, ---private:
        (str) – Bitcoin wallet private key.

    ::

        $ shuttle bitcoin sign --private 6bc3b581f3dea1963f9257ec2a0195969babee3704e6ba7cd2ec535140b9816f --raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRkZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFvRHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0
        [SUCCESS] eyJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMGQ4NDczMDQ0MDIyMDM0ZGM3MWMwZGU5NDEzZTc1MzVlN2RhMWU2NjliNTljM2I2NGZlMWZmMjE3ZjJjNzgxMjliNDg3ZTdiZWMzNGUwMjIwNzYxNTZkNGI5MWE2ZTQ2OTBhZmI4MmNlNmQwZWU3YjU4MDBkZjA2OWQ3MjUwYmMzOGJiZTNhOTdkZDkwYjA1NjAxMjEwMzkyMTNlYmNhZWZkZDNlMTA5NzIwYzE3ODY3Y2UxYmQ2ZDA3NmIwZTY1ZTNiNjM5MGU2ZTM4NTQ4YTY1ZTc2YWYwZTQ4NjU2YzZjNmYyMDRkNjU2ODY1NzI2NTc0MjE1MTRjNWM2M2FhMjA4MjExMjRiNTU0ZDEzZjI0N2IxZTVkMTBiODRlNDRmYjEyOTZmMThmMzhiYmFhMWJlYTM0YTEyYzg0M2UwMTU4ODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMmI4ODhhYzY3MDE2NGIyNzU3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzY4ZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAiZmVlIjogNTc2LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9jbGFpbV9zaWduZWQifQ

Submit Command
--------------

:$ shuttle bitcoin submit:

    Bitcoin submit signed transaction raw into blockchain.

    **Option Commands**

    :-h, ---help:
        Print a short description of bitcoin submit command line options.

    **Required Commands**

    :-r, ---raw:
        (str) – Bitcoin transaction raw.

    ::

        $ shuttle bitcoin submit --raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRkZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFvRHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0
        [SUCCESS] efeb2be0dc1dc0dba9ac882ce0e73c64f7fe09d5b3185b122849b38d124101f5

Bytom CLI
=========

:$ shuttle bytom:

    **Option Commands**

    :-h, ---help:
        Print a short description of bytom command line options.

    ::

        Usage: shuttle bytom [OPTIONS] COMMAND [ARGS]...

          SHUTTLE BYTOM

        Options:
          -h, --help  Show this message and exit.

        Commands:
          decode  Select bytom transaction raw decoder.
          sign    Select bytom transaction raw signer.
          submit  Select bytom submit transaction raw.

Decode Command
---------------------

:$ shuttle bytom decode:

    Bytom transaction raw decoder.

    **Option Commands**

    :-h, ---help:
        Print a short description of bytom decode command line options.

    **Required Commands**

    :-r, ---raw:
        (str) – Bytom transaction raw.

    ::

        $ shuttle bytom decode --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjZhMjMzNTAxN2VmOTY5MjhmN2E0NTdlZjVkZjUzYWYzNWFlZWY4MjkzZTUwOGNkZWU1YmMwYjkzYmUwZDNhZWUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyI0NDE1N2U1MjNhYWVkOTAzZmE0OGY1NTVmOGRkOTZiZGM3OGUzMzNlNGZiYmViMzhiNjM2ZmQxOTFkNGQ2MTUwIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogIjg4NDNiY2ExNzJlZDQ2ODViNTExYzBmMTA2ZmQzZjY4ODlhNDJmYTNmOTM4M2QwNTdlYTRlNTg3ZjdkYjBjYmUiLCAicmF3IjogIjA3MDEwMDAyMDE1YzAxNWFjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDE2MDAxNWVjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwOGFmOTgxMDkwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxYWMwMWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5ZjU1NDZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwZGQ5NmZkMDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0
        [SUCCESS] {"tx_id": "8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe", "version": 1, "size": 507, "time_range": 0, "inputs": [{"type": "spend", "asset_id": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "asset_definition": {}, "amount": 100, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "spent_output_id": "0f863bece342588542958b31e5bbfab1f8f0ad04e3e867ea6010375dd0ede287", "input_id": "e561efb4fea0b91305d2fa3ea159ea441fc8a84d59f4ed7ef4133721ab7841eb", "witness_arguments": ["91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"], "sign_data": "6a2335017ef96928f7a457ef5df53af35aeef8293e508cdee5bc0b93be0d3aee"}, {"type": "spend", "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 2420000000, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "spent_output_id": "df607d2ac2a9e3a00e8161457af8b0892bf0f42cbdca617d1033bd2958c0eb46", "input_id": "8fdd4feef611b22b19f82d69d52bf79e4f835b90291fc63374844fdee8e7abca", "witness_arguments": ["91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"], "sign_data": "44157e523aaed903fa48f555f8dd96bdc78e333e4fbbeb38b636fd191d4d6150"}], "outputs": [{"type": "control", "id": "d89449d3ec2117e4d2ad0f964f34a578cf8c980d049c273cb711f42378d734a3", "position": 0, "asset_id": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "asset_definition": {}, "amount": 100, "control_program": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"}, {"type": "control", "id": "9ac3616cd02d1a9f836a640dfc07d40c2d3ae4ccc6c7abe9e12b465c766be1a9", "position": 1, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 2410000000, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"}], "fee": 10000000}

Sign Command
------------------

:$ shuttle bytom sign:

    Bytom transaction raw signer.

    **Option Commands**

    :-h, ---help:
        Print a short description of bytom sign command line options.
    :-s, ---secret:
        (str) – Secret key for Claim.
    :-ac, ---account:
        (int) – Bytom derivation from account, defaults to 1.
    :-c, ---change:
        (bool) – Bytom derivation from change, defaults to False.
    :-ad, ---address:
        (int) – Bytom derivation from address, defaults to 1.
    :-p, ---path:
        (str) – Bytom derivation from path.
    :-i, ---indexes:
        (list) – Bytom derivation from indexes.

    **Required Commands**

    :-u, ---unsigned:
        (str) – Bytom unsigned transaction raw.
    :-xp, ---xprivate:
        (str) – Bytom wallet xprivate key.

    ::

        $ shuttle bytom sign --xprivate 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --unsigned eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjZhMjMzNTAxN2VmOTY5MjhmN2E0NTdlZjVkZjUzYWYzNWFlZWY4MjkzZTUwOGNkZWU1YmMwYjkzYmUwZDNhZWUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyI0NDE1N2U1MjNhYWVkOTAzZmE0OGY1NTVmOGRkOTZiZGM3OGUzMzNlNGZiYmViMzhiNjM2ZmQxOTFkNGQ2MTUwIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogIjg4NDNiY2ExNzJlZDQ2ODViNTExYzBmMTA2ZmQzZjY4ODlhNDJmYTNmOTM4M2QwNTdlYTRlNTg3ZjdkYjBjYmUiLCAicmF3IjogIjA3MDEwMDAyMDE1YzAxNWFjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDE2MDAxNWVjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwOGFmOTgxMDkwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxYWMwMWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5ZjU1NDZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwZGQ5NmZkMDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0
        [SUCCESS] eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAxMDAwMjAxNWMwMTVhY2ZlMDg2YzQ1OTQ5MmY4MGY4N2I5MjYzZGMwY2ZhNzU3ZGRlZTg1YTc1NTM3NzU4NmEzMjMzMmFiMjExN2MwMGYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAwMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNjAwMTVlY2ZlMDg2YzQ1OTQ5MmY4MGY4N2I5MjYzZGMwY2ZhNzU3ZGRlZTg1YTc1NTM3NzU4NmEzMjMzMmFiMjExN2MwMGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDhhZjk4MTA5MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDIwMWFjMDFmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmNjQwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI4ODQzYmNhMTcyZWQ0Njg1YjUxMWMwZjEwNmZkM2Y2ODg5YTQyZmEzZjkzODNkMDU3ZWE0ZTU4N2Y3ZGIwY2JlIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjZhMjMzNTAxN2VmOTY5MjhmN2E0NTdlZjVkZjUzYWYzNWFlZWY4MjkzZTUwOGNkZWU1YmMwYjkzYmUwZDNhZWUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyI0NDE1N2U1MjNhYWVkOTAzZmE0OGY1NTVmOGRkOTZiZGM3OGUzMzNlNGZiYmViMzhiNjM2ZmQxOTFkNGQ2MTUwIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAic2lnbmF0dXJlcyI6IFtbIjI4Yzk5YmEwZWJkYWU4ZTYxZjRmNzdmYjQ1MGEyYTVjOTllZGYxM2IzMTU4NzM4ODQwYjRjYzU0NjA1ZWM5MDhmOThjMzFmMmFkNzQ2NzM2MDZmZWFkNzhiYzVhYTgwYTQwNmJiZWI4NzZhNzU3YmU2ODRiNTIzYzM4ODgwYTBjIl0sIFsiN2ViODVlYzAyYzMzNzM4ZmY3ZDNhNGE0M2VlYjY2ODA0YzEwYjVhODA0MDdjZTJiN2YyZGI2ZDZkZGJmMjQ3YzY0YTdlM2I5MTU0YWM1ODZiYjA1MTllOTdmNzI0MmZlYzEyMDY5MzQ1MDI0ZjcxNWVlMzhkOTk4MDJjMTQyMGEiXV0sICJ0eXBlIjogImJ5dG9tX2Z1bmRfc2lnbmVkIn0

Submit Command
--------------

:$ shuttle bytom submit:

    Bytom submit signed transaction raw into blockchain.

    **Option Commands**

    :-h, ---help:
        Print a short description of bytom submit command line options.

    **Required Commands**

    :-r, ---raw:
        (str) – Bytom transaction raw.

    ::

        $ shuttle bytom submit --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjZhMjMzNTAxN2VmOTY5MjhmN2E0NTdlZjVkZjUzYWYzNWFlZWY4MjkzZTUwOGNkZWU1YmMwYjkzYmUwZDNhZWUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyI0NDE1N2U1MjNhYWVkOTAzZmE0OGY1NTVmOGRkOTZiZGM3OGUzMzNlNGZiYmViMzhiNjM2ZmQxOTFkNGQ2MTUwIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogIjg4NDNiY2ExNzJlZDQ2ODViNTExYzBmMTA2ZmQzZjY4ODlhNDJmYTNmOTM4M2QwNTdlYTRlNTg3ZjdkYjBjYmUiLCAicmF3IjogIjA3MDEwMDAyMDE1YzAxNWFjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDE2MDAxNWVjZmUwODZjNDU5NDkyZjgwZjg3YjkyNjNkYzBjZmE3NTdkZGVlODVhNzU1Mzc3NTg2YTMyMzMyYWIyMTE3YzAwZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwOGFmOTgxMDkwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxYWMwMWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5ZjU1NDZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwZGQ5NmZkMDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0
        [SUCCESS] 8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe
