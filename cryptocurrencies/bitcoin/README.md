# CLI - Bitcoin Commands

<img align="right" height="65" src="https://github.com/meherett/swap/blob/master/docs/static/svg/bitcoin.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Withdraw Command](#withdraw-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `bitcoin` command

```shell script
swap bitcoin --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode    Select Bitcoin Transaction raw decoder.
  fund      Select Bitcoin Fund transaction builder.
  htlc      Select Bitcoin Hash Time Lock Contract (HTLC) builder.
  refund    Select Bitcoin Refund transaction builder.
  sign      Select Bitcoin Transaction raw signer.
  submit    Select Bitcoin Transaction raw submitter.
  withdraw  Select Bitcoin Withdraw transaction builder.
```
</details>

## HTLC Command

> $ swap bitcoin `htlc` command

```shell script
swap bitcoin htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT        Set secret 256 hash.  [required]
  -ra, --recipient-address TEXT  Set Bitcoin recipient address.  [required]
  -sa, --sender-address TEXT     Set Bitcoin sender address.  [required]
  -e, --endtime INTEGER          Set Expiration block time (Seconds).
                                 [default: Current time plus 1hr]

  -n, --network TEXT             Set Bitcoin network.  [default: mainnet]
  -i, --indent INTEGER           Set json indent.  [default: 4]
  -h, --help                     Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Address** _(str)_ -> mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V **[required]**<br/>
**Sender Address** _(str)_ -> n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a **[required]**<br/>
**Endtime** _(int)_ -> 1624687630 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin Hash Time Lock Contract (HTLC) bytecode.

```shell script
swap bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-address mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V --sender-address n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a --endtime 1624687630 --network testnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
{
    "secret_hash": "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
    "recipient_address": "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V",
    "sender_address": "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a",
    "endtime": {
        "datetime": "2021-06-26 09:07:10",
        "timestamp": 1624687630
    },
    "bytecode": "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68",
    "contract_address": "2NBYr6gvh4ujsRwKKjDrrRr2vGonazzX6Z6"
}
```
</details>

## Fund Command

> $ swap bitcoin `fund` command

```shell script
swap bitcoin fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin fund [OPTIONS]

Options:
  -a, --address TEXT            Set Bitcoin sender address.  [required]
  -ca, --contract-address TEXT  Set Bitcoin Hash Time Lock Contract (HTLC)
                                address.  [required]

  -am, --amount FLOAT           Set Bitcoin fund amount.  [required]
  -u, --unit TEXT               Set Bitcoin fund amount unit.  [default:
                                Satoshi]

  -n, --network TEXT            Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER         Set Bitcoin transaction version.  [default: 2]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `fund` command

**Sender Address** _(str)_ -> n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a **[required]**<br/>
**Contract Address** _(str)_ -> 2NBYr6gvh4ujsRwKKjDrrRr2vGonazzX6Z6 **[required]**<br/>
**Amount** _(int, float)_ -> 0.001 **[required]**<br/>
**Unit** _(str)_ -> BTC **[default: `SATOSHI`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned fund transaction raw.

```shell script
swap bitcoin fund --address n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a --contract-address 2NBYr6gvh4ujsRwKKjDrrRr2vGonazzX6Z6 --amount 0.001 --unit BTC --network testnet --version 2
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```
</details>

## Withdraw Command

> $ swap bitcoin `withdraw` command

```shell script
swap bitcoin withdraw --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin withdraw [OPTIONS]

Options:
  -a, --address TEXT            Set Bitcoin recipient address.  [required]
  -th, --transaction-hash TEXT  Set Bitcoin funded transaction hash/id.
                                [required]

  -n, --network TEXT            Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER         Set Bitcoin transaction version.  [default: 2]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `withdraw` command

**Recipient Address** _(str)_ -> mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V **[required]**<br/>
**Transaction Hash** _(str)_ -> a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned withdraw transaction raw.

```shell script
swap bitcoin withdraw --address mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V --transaction-hash a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31 --network testnet --version 2
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNDBhMGE2NTkwZTZiYTRiNDgxMThkMjFiODY4MTI2MTUyMTllY2U3NmI4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl93aXRoZHJhd191bnNpZ25lZCJ9
```
</details>

## Refund Command

> $ swap bitcoin `refund` command

```shell script
swap bitcoin refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin refund [OPTIONS]

Options:
  -a, --address TEXT            Set Bitcoin sender address.  [required]
  -th, --transaction-hash TEXT  Set Bitcoin funded transaction hash/id.
                                [required]

  -n, --network TEXT            Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER         Set Bitcoin transaction version.  [default: 2]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `refund` command

**Sender Address** _(str)_ -> n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a **[required]**<br/>
**Transaction Hash** _(str)_ -> a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned refund transaction raw.

```shell script
swap bitcoin refund --address n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a --transaction-hash a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31 --network testnet --version 2
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9yZWZ1bmRfdW5zaWduZWQifQ==
```
</details>

## Decode Command

> $ swap bitcoin `decode` command

```shell script
swap bitcoin decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin decode [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set Bitcoin transaction raw.  [required]
  -i, --indent INTEGER         Set json indent.  [default: 4]
  -o, --offline BOOLEAN        Set Offline decode transaction raw.  [default:
                               True]

  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `decode` command

**Transaction Raw** _(str)_ -> eyJyYXciOiAiMDIwMDAwMDAwMjMxZmI3NmEwYzM4ZDU3MzgxYjMx... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin transaction json.

```shell script
swap bitcoin decode --transaction-raw eyJyYXciOiAiMDIwMDAwMDAwMjMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwZDM2MjhiYjJhYjk4YmFhMWUwMzVlMzBlNjZjZDEyYmRjN2RjNzcyNGQ2YzE5OGJjMWU5Nzk5ODM5ZjA2OTJmNTAyMjAzMDMxZjJjMmRjM2JlMDdmMGVmYWUwNDk4Y2RkNDM2NTYwOGZhNzZkMzFhNGVkOTUxYzk3MGRiMjI0MDI5NTAyMDEyMTAzN2NlODcxMDA3ZTMwMmQ1MGQyOGM5YzM5ZTRlMWY4NTk5MTMyNGIxN2Q5OTExMjYyMDUzZTQyOWM1YzUwZjRhZGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwNmI0ODMwNDUwMjIxMDBlZTg0YmYyYWMwNzBlNmQwZTljM2M5MTI5M2QwMTEzMWJjZGY1MGRkMjNjMzVjNDg2YTUxMjUzY2Q1ZmM0ZmVmMDIyMDcxNjkzM2MxMmYxMDhjOTU4NmRjYTdkMTU5ZjVjNmRlMWNjNzE3OTBmMGVkNTY3MTE2M2M0MmE2NGYyMGU1MzAwMTIxMDM3Y2U4NzEwMDdlMzAyZDUwZDI4YzljMzllNGUxZjg1OTkxMzI0YjE3ZDk5MTEyNjIwNTNlNDI5YzVjNTBmNGFkZmZmZmZmZmYwMmEwODYwMTAwMDAwMDAwMDAxN2E5MTRjOGM3N2E5YjQzZWUyYmRmMWEwN2M0ODY5OTgzM2Q3NjY4YmYyNjRjODczMjljMGQwMDAwMDAwMDAwMTk3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYzAwMDAwMDAwIiwgImZlZSI6IDExMjIsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0=
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "fee": 1122,
    "type": "bitcoin_fund_signed",
    "transaction": {
        "hex": "020000000231fb76a0c38d57381b3110e4f5ee9b5281dcf2fbe2fe2569266b751011d211a2010000006b483045022100d3628bb2ab98baa1e035e30e66cd12bdc7dc7724d6c198bc1e9799839f0692f502203031f2c2dc3be07f0efae0498cdd4365608fa76d31a4ed951c970db2240295020121037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4adffffffff080b82eec332996a422ae4f080f74e53fd2ca4f07011d47c590853e1e305fe11010000006b483045022100ee84bf2ac070e6d0e9c3c91293d01131bcdf50dd23c35c486a51253cd5fc4fef0220716933c12f108c9586dca7d159f5c6de1cc71790f0ed5671163c42a64f20e5300121037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4adffffffff02a08601000000000017a914c8c77a9b43ee2bdf1a07c48699833d7668bf264c87329c0d00000000001976a914e00ff2a640b7ce2d336860739169487a57f84b1588ac00000000",
        "txid": "f6d0ee0002359df9d3b03a59dca3258630f1a50b30da1c7b8c771b1e5db4a7e6",
        "hash": "f6d0ee0002359df9d3b03a59dca3258630f1a50b30da1c7b8c771b1e5db4a7e6",
        "size": 372,
        "vsize": 372,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31",
                "vout": 1,
                "scriptSig": {
                    "asm": "3045022100d3628bb2ab98baa1e035e30e66cd12bdc7dc7724d6c198bc1e9799839f0692f502203031f2c2dc3be07f0efae0498cdd4365608fa76d31a4ed951c970db22402950201 037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4ad",
                    "hex": "483045022100d3628bb2ab98baa1e035e30e66cd12bdc7dc7724d6c198bc1e9799839f0692f502203031f2c2dc3be07f0efae0498cdd4365608fa76d31a4ed951c970db2240295020121037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4ad"
                },
                "sequence": "4294967295"
            },
            {
                "txid": "11fe05e3e15308597cd41170f0a42cfd534ef780f0e42a426a9932c3ee820b08",
                "vout": 1,
                "scriptSig": {
                    "asm": "3045022100ee84bf2ac070e6d0e9c3c91293d01131bcdf50dd23c35c486a51253cd5fc4fef0220716933c12f108c9586dca7d159f5c6de1cc71790f0ed5671163c42a64f20e53001 037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4ad",
                    "hex": "483045022100ee84bf2ac070e6d0e9c3c91293d01131bcdf50dd23c35c486a51253cd5fc4fef0220716933c12f108c9586dca7d159f5c6de1cc71790f0ed5671163c42a64f20e5300121037ce871007e302d50d28c9c39e4e1f85991324b17d9911262053e429c5c50f4ad"
                },
                "sequence": "4294967295"
            }
        ],
        "vout": [
            {
                "value": "0.00100000",
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_HASH160 c8c77a9b43ee2bdf1a07c48699833d7668bf264c OP_EQUAL",
                    "hex": "a914c8c77a9b43ee2bdf1a07c48699833d7668bf264c87",
                    "type": "p2sh",
                    "address": "2NBYr6gvh4ujsRwKKjDrrRr2vGonazzX6Z6"
                }
            },
            {
                "value": "0.00891954",
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 e00ff2a640b7ce2d336860739169487a57f84b15 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914e00ff2a640b7ce2d336860739169487a57f84b1588ac",
                    "type": "p2pkh",
                    "address": "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a"
                }
            }
        ]
    },
    "network": "testnet"
}
```
</details>

## Sign Command

> $ swap bitcoin `sign` command

```shell script
swap bitcoin sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin sign [OPTIONS]

Options:
  -xpk, --xprivate-key TEXT    Set Bitcoin root xprivate key.  [required]
  -tr, --transaction-raw TEXT  Set Bitcoin unsigned transaction raw.
                               [required]

  -b, --bytecode TEXT          Set Bitcoin witness HTLC bytecode.  [default:
                               None]

  -sk, --secret-key TEXT       Set secret key.  [default: None]
  -e, --endtime INTEGER        Set Expiration block time (Seconds).  [default:
                               current time plus 1hr]

  -ac, --account INTEGER       Set Bitcoin derivation from account.  [default:
                               1]

  -ch, --change BOOLEAN        Set Bitcoin derivation from change.  [default:
                               False]

  -ad, --address INTEGER       Set Bitcoin derivation from address.  [default:
                               1]

  -p, --path TEXT              Set Bitcoin derivation from path.  [default:
                               None]

  -v, --version INTEGER        Set Bitcoin transaction version.  [default: 2]
  -h, --help                   Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `withdraw` transaction you have to be use `--secret-key` option.

> **Example** -> swap bitcoin `sign` command

**Root XPrivate Key** _(str)_ -> tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNz... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin signed transaction raw.

```shell script
swap bitcoin sign --xprivate-key tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf --transaction-raw eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJyYXciOiAiMDIwMDAwMDAwMjMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwZDM2MjhiYjJhYjk4YmFhMWUwMzVlMzBlNjZjZDEyYmRjN2RjNzcyNGQ2YzE5OGJjMWU5Nzk5ODM5ZjA2OTJmNTAyMjAzMDMxZjJjMmRjM2JlMDdmMGVmYWUwNDk4Y2RkNDM2NTYwOGZhNzZkMzFhNGVkOTUxYzk3MGRiMjI0MDI5NTAyMDEyMTAzN2NlODcxMDA3ZTMwMmQ1MGQyOGM5YzM5ZTRlMWY4NTk5MTMyNGIxN2Q5OTExMjYyMDUzZTQyOWM1YzUwZjRhZGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwNmI0ODMwNDUwMjIxMDBlZTg0YmYyYWMwNzBlNmQwZTljM2M5MTI5M2QwMTEzMWJjZGY1MGRkMjNjMzVjNDg2YTUxMjUzY2Q1ZmM0ZmVmMDIyMDcxNjkzM2MxMmYxMDhjOTU4NmRjYTdkMTU5ZjVjNmRlMWNjNzE3OTBmMGVkNTY3MTE2M2M0MmE2NGYyMGU1MzAwMTIxMDM3Y2U4NzEwMDdlMzAyZDUwZDI4YzljMzllNGUxZjg1OTkxMzI0YjE3ZDk5MTEyNjIwNTNlNDI5YzVjNTBmNGFkZmZmZmZmZmYwMmEwODYwMTAwMDAwMDAwMDAxN2E5MTRjOGM3N2E5YjQzZWUyYmRmMWEwN2M0ODY5OTgzM2Q3NjY4YmYyNjRjODczMjljMGQwMDAwMDAwMDAwMTk3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYzAwMDAwMDAwIiwgImZlZSI6IDExMjIsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0=
```
</details>

## Submit Command

> $ swap bitcoin `submit` command

```shell script
swap bitcoin submit --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin submit [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set signed Bitcoin transaction raw.  [required]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `submit` command

**Signed Transaction Raw** _(str)_ -> eyJyYXciOiAiMDIwMDAwMDAwMjMxZmI3NmEwYzM4ZDU3MzgxYjMx... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin blockchain transaction id.

```shell script
swap bitcoin submit --transaction-raw eyJyYXciOiAiMDIwMDAwMDAwMjMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwZDM2MjhiYjJhYjk4YmFhMWUwMzVlMzBlNjZjZDEyYmRjN2RjNzcyNGQ2YzE5OGJjMWU5Nzk5ODM5ZjA2OTJmNTAyMjAzMDMxZjJjMmRjM2JlMDdmMGVmYWUwNDk4Y2RkNDM2NTYwOGZhNzZkMzFhNGVkOTUxYzk3MGRiMjI0MDI5NTAyMDEyMTAzN2NlODcxMDA3ZTMwMmQ1MGQyOGM5YzM5ZTRlMWY4NTk5MTMyNGIxN2Q5OTExMjYyMDUzZTQyOWM1YzUwZjRhZGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwNmI0ODMwNDUwMjIxMDBlZTg0YmYyYWMwNzBlNmQwZTljM2M5MTI5M2QwMTEzMWJjZGY1MGRkMjNjMzVjNDg2YTUxMjUzY2Q1ZmM0ZmVmMDIyMDcxNjkzM2MxMmYxMDhjOTU4NmRjYTdkMTU5ZjVjNmRlMWNjNzE3OTBmMGVkNTY3MTE2M2M0MmE2NGYyMGU1MzAwMTIxMDM3Y2U4NzEwMDdlMzAyZDUwZDI4YzljMzllNGUxZjg1OTkxMzI0YjE3ZDk5MTEyNjIwNTNlNDI5YzVjNTBmNGFkZmZmZmZmZmYwMmEwODYwMTAwMDAwMDAwMDAxN2E5MTRjOGM3N2E5YjQzZWUyYmRmMWEwN2M0ODY5OTgzM2Q3NjY4YmYyNjRjODczMjljMGQwMDAwMDAwMDAwMTk3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYzAwMDAwMDAwIiwgImZlZSI6IDExMjIsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0=
```

<details open>
  <summary>Output</summary><br/>

```shell script
f6d0ee0002359df9d3b03a59dca3258630f1a50b30da1c7b8c771b1e5db4a7e6
```
</details>
