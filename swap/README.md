# Swap on Shuttle CLI

- [Shuttle Command](#shuttle-command)
  - [Version Option](#version-option)
  - [Bitcoin Command](#bitcoin-command)
    - [HTLC Command](#htlc-command)
    - [Fund Command](#fund-command)
    - [Claim Command](#claim-command)
    - [Refund Command](#refund-command)
    - [Decode Command](#decode-command)
    - [Sign Command](#sign-command)
    - [Submit Command](#submit-command)
  - [Bytom Command](#bytom-command)
    - [HTLC Command](#htlc-command-1)
    - [Fund Command](#fund-command-1)
    - [Claim Command](#claim-command-1)
    - [Refund Command](#refund-command-1)
    - [Decode Command](#decode-command-1)
    - [Sign Command](#sign-command-1)
    - [Submit Command](#submit-command-1)

## Shuttle Command

> $ `shuttle` command

```shell script
$ shuttle --help
```

<details open>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show Shuttle version and exit.
  -h, --help     Show this message and exit.

Commands:
  bitcoin  Select Bitcoin provider.
  bytom    Select Bytom provider.
```
</details>

### Version Option

> $ shuttle `--version` option

```shell script
$ shuttle --version
```

<details open>
  <summary>Output</summary><br/>

```shell script
v0.2.0a1
```
</details>

## Bitcoin Command

> $ shuttle `bitcoin` command

```shell script
$ shuttle bitcoin --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode  Select Bitcoin transaction raw decoder.
  fund    Select Bitcoin fund transaction builder.
  htlc    Select Bitcoin Hash Time Lock Contract (HTLC) builder.
  sign    Select Bitcoin transaction raw signer.
  submit  Select Bitcoin transaction raw submitter.
```
</details>

### HTLC Command

> $ shuttle bitcoin `htlc` command

```shell script
$ shuttle bitcoin htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT        Set secret 256 hash.  [required]
  -ra, --recipient-address TEXT  Set Bitcoin recipient address.  [required]
  -sa, --sender-address TEXT     Set Bitcoin sender address.  [required]
  -s, --sequence INTEGER         Set Bitcoin expiration block (sequence).
  -n, --network TEXT             Set Bitcoin network.
  -h, --help                     Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Address** _(str)_ -> muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB **[required]**<br/>
**Sender Address** _(str)_ -> mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q **[required]**<br/>
**Sequence** _(int)_ -> 100 **[default: `100`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ shuttle bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-address muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB --sender-address mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q --sequence 100 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68
```
</details>

### Fund Command

> $ shuttle bitcoin `fund` command

```shell script
$ shuttle bitcoin fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin fund [OPTIONS]

Options:
  -sa, --sender-address TEXT  Set Bitcoin sender address.  [required]
  -a, --amount INTEGER        Set Bitcoin amount to fund on HTLC.  [required]
  -b, --bytecode TEXT         Set Bitcoin HTLC bytecode.  [required]
  -v, --version INTEGER       Set Bitcoin transaction version.
  -n, --network TEXT          Set Bitcoin network.
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `fund` command

**Sender Address** _(str)_ -> mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**bytecode** _(str)_ -> 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned fund transaction raw.

```shell script
$ shuttle bitcoin fund --sender-address mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q --amount 10000 --bytecode 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2ZjM5OWMzYmU3MTc3YjkwMWY0YTY2ODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```
</details>

### Claim Command

> $ shuttle bitcoin `claim` command

```shell script
$ shuttle bitcoin claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin claim [OPTIONS]

Options:
  -t, --transaction TEXT         Set Bitcoin fund transaction id.  [required]
  -ra, --recipient-address TEXT  Set Bitcoin recipient address.  [required]
  -a, --amount INTEGER           Set Bitcoin amount to claim.  [required]
  -v, --version INTEGER          Set Bitcoin transaction version.
  -n, --network TEXT             Set Bitcoin network.
  -h, --help                     Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `claim` command

**Transaction Id** _(str)_ -> f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768 **[required]**<br/>
**Recipient Address** _(str)_ -> muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB **[required]**<br/>
**Amount** _(int)_ -> 700 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> mainnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned claim transaction raw.

```shell script
$ shuttle bitcoin claim --transaction f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768 --recipient-address muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB --amount 700 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRkZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFvRHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0==
```
</details>

### Refund Command

> $ shuttle bitcoin `refund` command

```shell script
$ shuttle bitcoin refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin refund [OPTIONS]

Options:
  -t, --transaction TEXT         Set Bitcoin fund transaction id.  [required]
  -ra, --recipient-address TEXT  Set Bitcoin recipient address.  [required] 
  -a, --amount INTEGER           Set Bitcoin amount to refund.  [required]
  -v, --version INTEGER          Set Bitcoin transaction version.
  -n, --network TEXT             Set Bitcoin network.
  -h, --help                     Show this message and exit.
```
</details>

**Note**: Don't forget, Bitcoin refund command it takes recipient address not sender b/c it is the witness of the contract.

> **Example** -> shuttle bitcoin `refund` command

**Transaction Id** _(str)_ -> f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768 **[required]**<br/>
**Recipient Address** _(str)_ -> muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB **[required]**<br/>
**Amount** _(int)_ -> 700 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> mainnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned refund transaction raw.

```shell script
$ shuttle bitcoin refund --transaction f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768 --recipient-address muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB --amount 700 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZTYxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAwMDAxOTc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRkZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFvRHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

### Decode Command

> $ shuttle bitcoin `decode` command

```shell script
$ shuttle bitcoin decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin decode [OPTIONS]

Options:
  -r, --raw TEXT  Set Bitcoin transaction raw.  [required]
  -h, --help      Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `decode` command

**Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4O... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin transaction json.

```shell script
$ shuttle bitcoin decode --raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2ZjM5OWMzYmU3MTc3YjkwMWY0YTY2ODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 678,
    "type": "bitcoin_fund_unsigned",
    "tx": {
        "hex": "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f3910100000000ffffffff02102700000000000017a9146f08b254e4c58dc65f6f399c3be7177b901f4a6687bcdd0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000",
        "txid": "76054d887e7e859eb8915ca830872681247598bcfdc38d8fc0fba6117005e016",
        "hash": "76054d887e7e859eb8915ca830872681247598bcfdc38d8fc0fba6117005e016",
        "size": 117,
        "vsize": 117,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88",
                "vout": 1,
                "scriptSig": {
                    "asm": "",
                    "hex": ""
                },
                "sequence": "4294967295"
            }
        ],
        "vout": [
            {
                "value": "0.00010000",
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_HASH160 6f08b254e4c58dc65f6f399c3be7177b901f4a66 OP_EQUAL",
                    "hex": "a9146f08b254e4c58dc65f6f399c3be7177b901f4a6687",
                    "type": "p2sh",
                    "address": "2N3NKQpymf1KunR4W8BpZjs8za5La5pV5hF"
                }
            },
            {
                "value": "0.00974268",
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac",
                    "type": "p2pkh",
                    "address": "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q"
                }
            }
        ]
    },
    "network": "testnet"
}
```
</details>

### Sign Command

> $ shuttle bitcoin `sign` command

```shell script
$ shuttle bitcoin sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin sign [OPTIONS]

Options:
  -p, --private TEXT     Set Bitcoin private key.  [required]
  -r, --raw TEXT         Set Bitcoin unsigned transaction raw.  [required]
  -s, --secret TEXT      Set secret key.
  -v, --version INTEGER  Set Bitcoin transaction version.  [default: 2]
  -h, --help             Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing unsigned `claim/refund` transaction you have to be use `--secret` option.

> **Example** -> shuttle bitcoin `sign` command

**Private Key** _(str)_ -> 92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b **[required]**<br/>
**Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4O... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin signed transaction raw.

```shell script
$ shuttle bitcoin sign --private 92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b --raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2ZjM5OWMzYmU3MTc3YjkwMWY0YTY2ODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwOTQyNTU4MjIzMDNjZWU2MzAwYTRjOTFkZDZkNTBiYWUzZDY3ZmUyYTljNWJiNjMwOGUzNWZhODBkOTNiMWNmNjAyMjA3NDAxMmZlMTVjZjM2MmZhOGMzY2RhMGI3NjJjMTk0ODUxZmIxNjlkMDU3OWQ4ZGVjYWZmZTcwZmEwNmFhZjZkMDEyMTAzYzU2YTYwMDVkNGE4ODkyZDI4Y2MzZjcyNjVlNTY4NWI1NDg2MjdkNTkxMDg5NzNlNDc0YzRlMjZmNjlhNGM4NGZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0NmYwOGIyNTRlNGM1OGRjNjVmNmYzOTljM2JlNzE3N2I5MDFmNGE2Njg3YmNkZDBlMDAwMDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0=====
```
</details>

### Submit Command

> $ shuttle bitcoin `submit` command

```shell script
$ shuttle bitcoin submit --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bitcoin submit [OPTIONS]

Options:
  -r, --raw TEXT  Set signed Bitcoin transaction raw.  [required]
  -h, --help      Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `submit` command

**Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4O... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin blockchain transaction id.

```shell script
$ shuttle bitcoin submit --raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2ZjM5OWMzYmU3MTc3YjkwMWY0YTY2ODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
fe030ac60e97475862582236866ffd309f962cc71c0c8110b829e706cb02d796
```
</details>

## Bytom Command

> $ shuttle `bytom` command

```shell script
$ shuttle bytom --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode  Select Bytom transaction raw decoder.
  fund    Select Bytom fund transaction builder.
  htlc    Select Bytom Hash Time Lock Contract (HTLC) builder.
  sign    Select Bytom transaction raw signer.
  submit  Select Bytom transaction raw submitter.
```
</details>

### HTLC Command

> $ shuttle bytom `htlc` command

```shell script
$ shuttle bytom htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT       Set secret 256 hash.  [required]
  -rp, --recipient-public TEXT  Set Bytom recipient public key.  [required]
  -sp, --sender-public TEXT     Set Bytom sender public key.  [required]
  -s, --sequence INTEGER        Set Bytom expiration block (sequence).
  -n, --network TEXT            Set Bytom network.
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 **[required]**<br/>
**Sender Public Key** _(str)_ -> 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 **[required]**<br/>
**Sequence** _(int)_ -> 100 **[default: `100`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bytom Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ shuttle bytom htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 --sender-public 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 --sequence 100 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0
```
</details>

### Fund Command

> $ shuttle bytom `fund` command

```shell script
$ shuttle bytom fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom fund [OPTIONS]

Options:
  -sg, --sender-guid TEXT  Set Bytom sender GUID.  [required]
  -a, --amount INTEGER     Set Bytom amount to fund on HTLC.  [required]
  -as, --asset TEXT        Set Bytom asset id.  [required]
  -b, --bytecode TEXT      Set Bytom HTLC bytecode.  [required]
  -n, --network TEXT       Set Bytom network.
  -h, --help               Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `fund` command

**Sender GUID** _(str)_ -> f0ed6ddd-9d6b-49fd-8866-a52d1083a13b **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf **[required]**<br/>
**bytecode** _(str)_ -> 01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0 **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned fund transaction raw.

```shell script
$ shuttle bytom fund --sender-guid f0ed6ddd-9d6b-49fd-8866-a52d1083a13b --amount 10000 --asset f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf --bytecode 01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM3ODkzMzE3YzJhMmUxOTVlN2RjZDcwNjdjYzYwZDFhMGE3NDg1NGJmZGEwODNjNDZjYTcxMzkyOWY1NTNiODMiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJlNDFlZThmZDI4ZTgzYzMzMTkxM2VjODI5ZWVjNDQ2ZTUzZDA3ZjRhOTYxZDFiZjI3YjZkNDk5MWVkM2Y4YzMzIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogImMyZTIxYmNmYzFhY2Q3ZTQ1YzhiYTAwY2QyNTA5ZTA1YWNhMGZmOGNjNjk2MTJiNzA0MzIyN2EzY2U0NzBmMDEiLCAicmF3IjogIjA3MDEwMDAyMDE2MTAxNWY4MWU1MGUxMmY4MjM2ZjkxYzg4NDJkM2Y0OTU1MDJiOTc1MmZjMzVkMDE1MDA5MWVhNWIyYzI2NjA1MTVjM2I1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZmE4Y2JkYmMzZjQwMjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDMwMWFkMDFmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmOTA0ZTAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWI3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMDAxM2VmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmOThmZGRhYzNmNDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```
</details>

### Claim Command

> $ shuttle bytom `claim` command

```shell script
$ shuttle bytom claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom claim [OPTIONS]

Options:
  -t, --transaction TEXT        Set Bytom fund transaction id.  [required]
  -rg, --recipient-guid TEXT    Set Bytom recipient GUID.  [required]
  -rp, --recipient-public TEXT  Set Bytom recipient public key.  [required]
  -a, --amount INTEGER          Set Bytom amount to claim.  [required]
  -as, --asset TEXT             Set Bytom asset id.  [required]
  -n, --network TEXT            Set Bytom network.
  -h, --help                    Show this message and exit
```
</details>

> **Example** -> shuttle bytom `claim` command

**Transaction Id** _(str)_ -> 8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe **[required]**<br/>
**Recipient GUID** _(str)_ -> f0ed6ddd-9d6b-49fd-8866-a52d1083a13b **[required]**<br/>
**Recipient Public Key** _(str)_ -> ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 **[required]**<br/>
**Amount** _(int)_ -> 100 **[required]**<br/>
**Asset Id** _(str)_ -> f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned claim transaction raw.

```shell script
$ shuttle bytom claim --transaction 8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe --recipient-guid f0ed6ddd-9d6b-49fd-8866-a52d1083a13b --recipient-public ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 --amount 100 --asset f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjg0MGYwZjM5MTFiOTllY2NlODk0MjA0OWFhYjY4NjEzMmE5MTAzNTBiZTAxNDY0MTU1YzkzM2ZjMWE5Y2NmZjQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjg2ZGFiNjAwZWFjMDMxYjM4YjE2YmQ1NGQzMjMwYjgyNWUwYjI2YmNkZGZkZGJhNTdjODBhZDNmNjI4YTllYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiZTg5OWVjNzlhN2IxYTk0MzFjYjczNWMxYmMxYmNhYzg1MDJjZjZkYmY3NTA0ODdjMzcxYjQ0NDFkNTUyNmVjNiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MTFiYzE5MGY0ZWJlM2E2ZGRjYmM3YWVmNjk3M2FjNGE4OTNiNDQ1NjAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2VjcmV0IjogbnVsbCwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0=
```
</details>

### Refund Command

> $ shuttle bytom `refund` command

```shell script
$ shuttle bytom refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom refund [OPTIONS]

Options:
  -t, --transaction TEXT     Set Bytom fund transaction id.  [required]
  -sg, --sender-guid TEXT    Set Bytom sender GUID.  [required]
  -sp, --sender-public TEXT  Set Bytom sender public key.  [required]
  -a, --amount INTEGER       Set Bytom amount to refund.  [required]
  -as, --asset TEXT          Set Bytom asset id.  [required]
  -n, --network TEXT         Set Bytom network.
  -h, --help                 Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `refund` command

**Transaction Id** _(str)_ -> 8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe **[required]**<br/>
**Sender GUID** _(str)_ -> f0ed6ddd-9d6b-49fd-8866-a52d1083a13b **[required]**<br/>
**Sender Public Key** _(str)_ -> ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 **[required]**<br/>
**Amount** _(int)_ -> 100 **[required]**<br/>
**Asset Id** _(str)_ -> f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned refund transaction raw.

```shell script
$ shuttle bytom refund --transaction 8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe --sender-guid f0ed6ddd-9d6b-49fd-8866-a52d1083a13b --sender-public ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 --amount 100 --asset f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjg0MGYwZjM5MTFiOTllY2NlODk0MjA0OWFhYjY4NjEzMmE5MTAzNTBiZTAxNDY0MTU1YzkzM2ZjMWE5Y2NmZjQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjg2ZGFiNjAwZWFjMDMxYjM4YjE2YmQ1NGQzMjMwYjgyNWUwYjI2YmNkZGZkZGJhNTdjODBhZDNmNjI4YTllYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiZTg5OWVjNzlhN2IxYTk0MzFjYjczNWMxYmMxYmNhYzg1MDJjZjZkYmY3NTA0ODdjMzcxYjQ0NDFkNTUyNmVjNiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MTFiYzE5MGY0ZWJlM2E2ZGRjYmM3YWVmNjk3M2FjNGE4OTNiNDQ1NjAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fcmVmdW5kX3Vuc2lnbmVkIn0==
```
</details>

### Decode Command

> $ shuttle bytom `decode` command

```shell script
$ shuttle bytom decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom decode [OPTIONS]

Options:
  -r, --raw TEXT  Set Bytom transaction raw.  [required]
  -h, --help      Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `decode` command

**Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZ... **[required]**<br/>

> **Returns** _(str)_ -> Bytom transaction json.

```shell script
$ shuttle bytom decode --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbImQxZTUwMWZlYzlkNjMwZDM3ZDZhMjhkZmJiZWZiOWNjMjNlZjczNDY5ODg4MWFiYjc1NTVjMjYwYTNmODhjMmUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiY2I4YTMxYmNhNzQyZGU3ZmI2OGQ5NzY3ZDMzNDk4Mjk3ZjRjZGRkZjc1ZWNiYmJiMTljNWVjMTBkYjRmODIwNyIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDFhZDAxZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAzYTI2ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMGUxYjNmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 10000000,
    "guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
    "type": "bytom_fund_unsigned",
    "tx": {
        "tx_id": "cb8a31bca742de7fb68d9767d33498297f4cdddf75ecbbbb19c5ec10db4f8207",
        "version": 1,
        "size": 379,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 2410000000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
                "spent_output_id": "9ac3616cd02d1a9f836a640dfc07d40c2d3ae4ccc6c7abe9e12b465c766be1a9",
                "input_id": "026f4a641843db9f95333f014e72bf423bafe8a971437ef0640e08e1a6c1f51d",
                "witness_arguments": [
                    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
                ],
                "sign_data": "d1e501fec9d630d37d6a28dfbbefb9cc23ef734698881abb7555c260a3f88c2e"
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "e97475862582b829e706cb02d796236866ffd309f962cc71c0c8110fe030ac60",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000,
                "control_program": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
            },
            {
                "type": "control",
                "id": "ff24d784c174743a58d90dea29db7e5e3f7704070e083a105835c70f64b24054",
                "position": 1,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 2399990000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
            }
        ],
        "fee": 10000000
    },
    "unsigned": [
        {
            "datas": [
                "d1e501fec9d630d37d6a28dfbbefb9cc23ef734698881abb7555c260a3f88c2e"
            ],
            "public_key": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
            "network": "mainnet",
            "path": "m/44/153/1/0/1"
        }
    ],
    "signatures": [],
    "network": "mainnet"
}
```
</details>

### Sign Command

> $ shuttle bytom `sign` command

```shell script
$ shuttle bytom sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom sign [OPTIONS]

Options:
  -xp, --xprivate TEXT    Set Bytom xprivate key.  [required]
  -r, --raw TEXT          Set Bytom unsigned transaction raw.  [required]
  -ac, --account INTEGER  Set Bytom derivation from account.  [default: 1]
  -c, --change BOOLEAN    Set Bytom derivation from change.  [default: False]
  -ad, --address INTEGER  Set Bytom derivation from address.  [default: 1]
  -s, --secret TEXT       Set secret key.
  -p, --path TEXT         Set Bytom derivation from path.
  -i, --indexes LIST      Set Bytom derivation from indexes.
  -h, --help              Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret` option.

> **Example** -> shuttle bytom `sign` command

**XPrivate Key** _(str)_ -> 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b **[required]**<br/>
**Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZ... **[required]**<br/>

> **Returns** _(str)_ -> Bytom signed transaction raw.

```shell script
$ shuttle bytom sign --xprivate 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbImQxZTUwMWZlYzlkNjMwZDM3ZDZhMjhkZmJiZWZiOWNjMjNlZjczNDY5ODg4MWFiYjc1NTVjMjYwYTNmODhjMmUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiY2I4YTMxYmNhNzQyZGU3ZmI2OGQ5NzY3ZDMzNDk4Mjk3ZjRjZGRkZjc1ZWNiYmJiMTljNWVjMTBkYjRmODIwNyIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDFhZDAxZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAzYTI2ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMGUxYjNmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAxMDAwMTAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDIwMWFkMDFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWI3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYwZTFiM2Y4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogImNiOGEzMWJjYTc0MmRlN2ZiNjhkOTc2N2QzMzQ5ODI5N2Y0Y2RkZGY3NWVjYmJiYjE5YzVlYzEwZGI0ZjgyMDciLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiZDFlNTAxZmVjOWQ2MzBkMzdkNmEyOGRmYmJlZmI5Y2MyM2VmNzM0Njk4ODgxYWJiNzU1NWMyNjBhM2Y4OGMyZSJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInNpZ25hdHVyZXMiOiBbWyI1YWI0ZGY0YWY2NDQ4NDQ2ZjUzYTFmZjhjODE1NzhjOGUzODYwNDdiOWMyYWYzZGRjZTE1YjI5M2QzNWUzMWQxMjE3OTdiOWQ0MGUxNzU3NDViOGM1Njk2YTVhMDkwODFlODkyODc2YTYwZDI3ZmZiMzdhNjhkMDE1YTBlNDAwNiJdXSwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ====
```
</details>

### Submit Command

> $ shuttle bytom `submit` command

```shell script
$ shuttle bytom submit --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom submit [OPTIONS]

Options:
  -r, --raw TEXT  Set signed Bytom transaction raw.  [required]
  -h, --help      Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `submit` command

**Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZ... **[required]**<br/>

> **Returns** _(str)_ -> Bytom blockchain transaction id.

```shell script
$ shuttle bytom submit --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbImQxZTUwMWZlYzlkNjMwZDM3ZDZhMjhkZmJiZWZiOWNjMjNlZjczNDY5ODg4MWFiYjc1NTVjMjYwYTNmODhjMmUiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiY2I4YTMxYmNhNzQyZGU3ZmI2OGQ5NzY3ZDMzNDk4Mjk3ZjRjZGRkZjc1ZWNiYmJiMTljNWVjMTBkYjRmODIwNyIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDFhZDAxZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAzYTI2ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMGUxYjNmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
236866ffd309f962cc71c0c8110fe030ac60e97475862582b829e706cb02d796
```
</details>
