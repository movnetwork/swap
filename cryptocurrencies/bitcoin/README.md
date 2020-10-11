# CLI - Bitcoin Commands

<img align="right" height="65" src="https://github.com/meherett/swap/blob/master/docs/static/svg/bitcoin.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Claim Command](#claim-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `bitcoin` command

```shell script
$ swap bitcoin --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  claim   Select Bitcoin Claim transaction builder.
  decode  Select Bitcoin transaction raw decoder.
  fund    Select Bitcoin Fund transaction builder.
  htlc    Select Bitcoin Hash Time Lock Contract (HTLC) builder.
  refund  Select Bitcoin Refund transaction builder.
  sign    Select Bitcoin transaction raw signer.
  submit  Select Bitcoin transaction raw submitter.
```
</details>

## HTLC Command

> $ swap bitcoin `htlc` command

```shell script
$ swap bitcoin htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT        Set secret 256 hash.  [required]
  -ra, --recipient-address TEXT  Set Bitcoin recipient address.  [required]
  -sa, --sender-address TEXT     Set Bitcoin sender address.  [required]
  -s, --sequence INTEGER         Set Bitcoin sequence/expiration block.  [default: 1000]
  -n, --network TEXT             Set Bitcoin network.  [default: testnet]
  -h, --help                     Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Address** _(str)_ -> mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF **[required]**<br/>
**Sender Address** _(str)_ -> mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ swap bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-address mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF --sender-address mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC --sequence 1000 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68
```
</details>

## Fund Command

> $ swap bitcoin `fund` command

```shell script
$ swap bitcoin fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin fund [OPTIONS]

Options:
  -a, --address TEXT        Set Bitcoin sender address.  [required]
  -ha, --htlc-address TEXT  Set Bitcoin Hash Time Lock Contract (HTLC) address.  [required]
  -am, --amount INTEGER     Set Bitcoin amount (SATOSHI).  [required]
  -n, --network TEXT        Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER     Set Bitcoin transaction version.  [default: 2]
  -h, --help                Show this message and exit.

```
</details>

> **Example** -> swap bitcoin `fund` command

**Sender Address** _(str)_ -> mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC **[required]**<br/>
**HTLC Address** _(str)_ -> 2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned fund transaction raw.

```shell script
$ swap bitcoin fund --address mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC --amount 10000 --htlc-address 2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWExN2Q1N2U3ZDdmMDYyMzkzNTcxYjE4NDM3YmJhM2VjYzI2OTc4ZTNkZDI4NTgyODI0YTljODU3OGViNjI1OTgwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ5NDE4ZmVlZDQ2NDdlMTU2ZDY2NjNkYjNlMGNlZjdjMDUwZDAzODY3ODc3ZTA5MDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDc4NjQ0LCAidHhfb3V0cHV0X24iOiAxLCAic2NyaXB0IjogIjc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjIn1dLCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3Vuc2lnbmVkIn0=
```
</details>

## Claim Command

> $ swap bitcoin `claim` command

```shell script
$ swap bitcoin claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin claim [OPTIONS]

Options:
  -a, --address TEXT          Set Bitcoin recipient address.  [required]
  -ti, --transaction-id TEXT  Set Bitcoin funded transaction id/hash.  [required]
  -am, --amount INTEGER       Set Bitcoin amount (SATOSHI).  [required]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER       Set Bitcoin transaction version.  [default: 2]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `claim` command

**Recipient Address** _(str)_ -> mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF **[required]**<br/>
**Transaction Id** _(str)_ -> 5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned claim transaction raw.

```shell script
$ swap bitcoin claim --address mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF --transaction-id 5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318 --amount 10000 --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDBlMjU5ZTA4ZjJlYzlmYzk5YTkyYjZmNjZmZGZjYjNjNzkxNGZkNjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0=
```
</details>

## Refund Command

> $ swap bitcoin `refund` command

```shell script
$ swap bitcoin refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin refund [OPTIONS]

Options:
  -a, --address TEXT          Set Bitcoin sender address.  [required]
  -ti, --transaction-id TEXT  Set Bitcoin funded transaction id/hash.  [required]
  -am, --amount INTEGER       Set Bitcoin amount (SATOSHI).  [required]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER       Set Bitcoin transaction version.  [default: 2]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `refund` command

**Sender Address** _(str)_ -> mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC **[required]**<br/>
**Transaction Id** _(str)_ -> 5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned refund transaction raw.

```shell script
$ swap bitcoin refund --address mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC --transaction-id 5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318 --amount 10000 --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

## Decode Command

> $ swap bitcoin `decode` command

```shell script
$ swap bitcoin decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin decode [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set Bitcoin transaction raw.  [required]
  -i, --indent INTEGER         Set json indent.  [default: 4]
  -o, --offline BOOLEAN        Set Offline decode transaction raw.  [default: True]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `decode` command

**Transaction Raw** _(str)_ -> eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAw... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin transaction json.

```shell script
$ swap bitcoin decode --transaction-raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 576,
    "type": "bitcoin_refund_unsigned",
    "tx": {
        "hex": "02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a0000000000ffffffff01d0240000000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000",
        "txid": "6d8083644b7999c1d5451d6027427c11875f4e79ddc0881ad35957e5c112164c",
        "hash": "6d8083644b7999c1d5451d6027427c11875f4e79ddc0881ad35957e5c112164c",
        "size": 85,
        "vsize": 85,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318",
                "vout": 0,
                "scriptSig": {
                    "asm": "",
                    "hex": ""
                },
                "sequence": "4294967295"
            }
        ],
        "vout": [
            {
                "value": "0.00009424",
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac",
                    "type": "p2pkh",
                    "address": "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC"
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
$ swap bitcoin sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bitcoin sign [OPTIONS]

Options:
  -rxk, --root-xprivate-key TEXT  Set Bitcoin root xprivate key.  [required]
  -tr, --transaction-raw TEXT     Set Bitcoin unsigned transaction raw.  [required]
  -b, --bytecode TEXT             Set Bitcoin witness HTLC bytecode.  [default: None]
  -sk, --secret-key TEXT          Set secret key.  [default: None]
  -s, --sequence INTEGER          Set Bitcoin sequence/expiration block.  [default: 1000]
  -ac, --account INTEGER          Set Bitcoin derivation from account.  [default: 1]
  -ch, --change BOOLEAN           Set Bitcoin derivation from change.  [default: False]
  -ad, --address INTEGER          Set Bitcoin derivation from address.  [default: 1]
  -p, --path TEXT                 Set Bitcoin derivation from path.  [default: None]
  -v, --version INTEGER           Set Bitcoin transaction version.  [default: 2]
  -h, --help                      Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `sign` command

**Root XPrivate Key** _(str)_ -> tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTE4M... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin signed transaction raw.

```shell script
$ swap bitcoin sign --root-xprivate-key tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR --transaction-raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ5NDE4ZmVlZDQ2NDdlMTU2ZDY2NjNkYjNlMGNlZjdjMDUwZDAzODY3ODczNDMzMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDg5MzIyLCAidHhfb3V0cHV0X24iOiAxLCAic2NyaXB0IjogIjc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjIn1dLCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3Vuc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwYTUxYmIwOTE2YTc5YTE3MjJkMzhjYTRjNGNjZmM1MmUzYTEwMjNlY2E4NjhmNTEyMTRhZTVkMzA1MzQ4ZjMwZDAyMjAxZmY2ODcwZWI5MTMzNGIwNjI2NDkxYzcxMjQyYTBiMjA1N2UyY2YzZjhlZWNjZGFmZWI1ZGE3MTI2NmI0MmUyMDEyMTAyMzljZmQ4ODY1NDI4ZjEyNDhjNWU0MjM1NzhlYjBjOTg3MTU5OTQ0MWJkMmY3N2Q4M2I2ZDU0YjMzOWI3ZGE1Y2ZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3MzQzMzAxMDAwMDAwMDAwMDE5NzZhOTE0MzNlY2FiM2Q2N2YwZTJiZGU0M2U1MmY0MWVjMWVjYmRjNzNmMTFmODg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0=
```
</details>

## Submit Command

> $ swap bitcoin `submit` command

```shell script
$ swap bitcoin submit --help
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

**Signed Transaction Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4O... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin blockchain transaction id.

```shell script
$ swap bitcoin submit --transaction-raw eyJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwYTUxYmIwOTE2YTc5YTE3MjJkMzhjYTRjNGNjZmM1MmUzYTEwMjNlY2E4NjhmNTEyMTRhZTVkMzA1MzQ4ZjMwZDAyMjAxZmY2ODcwZWI5MTMzNGIwNjI2NDkxYzcxMjQyYTBiMjA1N2UyY2YzZjhlZWNjZGFmZWI1ZGE3MTI2NmI0MmUyMDEyMTAyMzljZmQ4ODY1NDI4ZjEyNDhjNWU0MjM1NzhlYjBjOTg3MTU5OTQ0MWJkMmY3N2Q4M2I2ZDU0YjMzOWI3ZGE1Y2ZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3MzQzMzAxMDAwMDAwMDAwMDE5NzZhOTE0MzNlY2FiM2Q2N2YwZTJiZGU0M2U1MmY0MWVjMWVjYmRjNzNmMTFmODg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318
```
</details>
