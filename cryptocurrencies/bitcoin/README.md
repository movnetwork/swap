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
  decode  Select Bitcoin Transaction raw decoder.
  fund    Select Bitcoin Fund transaction builder.
  htlc    Select Bitcoin Hash Time Lock Contract (HTLC) builder.
  refund  Select Bitcoin Refund transaction builder.
  sign    Select Bitcoin Transaction raw signer.
  submit  Select Bitcoin Transaction raw submitter.
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
  -n, --network TEXT             Set Bitcoin network.  [default: mainnet]
  -i, --indent INTEGER           Set json indent.  [default: 4]
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
{
    "bytecode": "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1e
cbdc73f11f888ac68",
    "address": "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae"
}
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
  -am, --amount FLOAT       Set Bitcoin fund amount.  [required]
  -u, --unit TEXT           Set Bitcoin fund amount unit.  [default: SATOSHI]
  -n, --network TEXT        Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER     Set Bitcoin transaction version.  [default: 2]
  -h, --help                Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `fund` command

**Sender Address** _(str)_ -> mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC **[required]**<br/>
**HTLC Address** _(str)_ -> 2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae **[required]**<br/>
**Amount** _(int, float)_ -> 0.1 **[required]**<br/>
**Unit** _(str)_ -> BTC **[default: `SATOSHI`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned fund transaction raw.

```shell script
$ swap bitcoin fund --address mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC --amount 0.1 --unit BTC --htlc-address 2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMTAwMDAwMDAwZmZmZmZmZmYwMjgwOTY5ODAwMDAwMDAwMDAxN2E5MTQ5NDE4ZmVlZDQ2NDdlMTU2ZDY2NjNkYjNlMGNlZjdjMDUwZDAzODY3ODdmZDg4YzYwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDIzMDExODc1LCAidHhfb3V0cHV0X24iOiAxLCAic2NyaXB0IjogIjc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjIn1dLCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3Vuc2lnbmVkIn0=
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
  -am, --amount FLOAT         Set Bitcoin withdraw amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Bitcoin withdraw max amount.  [default: True]
  -u, --unit TEXT             Set Bitcoin withdraw amount unit.  [default: SATOSHI]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER       Set Bitcoin transaction version.  [default: 2]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `claim` command

**Recipient Address** _(str)_ -> mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF **[required]**<br/>
**Transaction Id** _(str)_ -> 161da7d35fc7ec2f9a3b5f6469b2d3526d3a72ad7c4b124aae5838245a8bc64a **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned claim transaction raw.

```shell script
$ swap bitcoin claim --address mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF --transaction-id 161da7d35fc7ec2f9a3b5f6469b2d3526d3a72ad7c4b124aae5838245a8bc64a --max-amount True --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMDAwMDAwMDAwZmZmZmZmZmYwMTM2NWE5OTAwMDAwMDAwMDAxOTc2YTkxNDBlMjU5ZTA4ZjJlYzlmYzk5YTkyYjZmNjZmZGZjYjNjNzkxNGZkNjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDA1MDY3OCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0=
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
  -am, --amount FLOAT         Set Bitcoin refund amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Bitcoin refund max amount.  [default: True]
  -u, --unit TEXT             Set Bitcoin refund amount unit.  [default: SATOSHI]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -v, --version INTEGER       Set Bitcoin transaction version.  [default: 2]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bitcoin `refund` command

**Sender Address** _(str)_ -> mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC **[required]**<br/>
**Transaction Id** _(str)_ -> 161da7d35fc7ec2f9a3b5f6469b2d3526d3a72ad7c4b124aae5838245a8bc64a **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned refund transaction raw.

```shell script
$ swap bitcoin refund --address mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC --transaction-id 161da7d35fc7ec2f9a3b5f6469b2d3526d3a72ad7c4b124aae5838245a8bc64a --max-amount True --network testnet --version 2
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMDAwMDAwMDAwZmZmZmZmZmYwMTM2NWE5OTAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDA1MDY3OCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
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

**Transaction Raw** _(str)_ -> eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTR... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin transaction json.

```shell script
$ swap bitcoin decode --transaction-raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMDAwMDAwMDAwZmZmZmZmZmYwMTM2NWE5OTAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDA1MDY3OCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 576,
    "type": "bitcoin_refund_unsigned",
    "tx": {
        "hex": "02000000014ac68b5a243858ae4a124b7cad723a6d52d3b269645f3b9a2fecc75fd3a71d160000000000ffffffff01365a9900000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000",
        "txid": "e1b89dae0285d4303d4c3adf529465a2c84a20c2b8ee30a5005f85d88fa8a0b0",
        "hash": "e1b89dae0285d4303d4c3adf529465a2c84a20c2b8ee30a5005f85d88fa8a0b0",
        "size": 85,
        "vsize": 85,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "161da7d35fc7ec2f9a3b5f6469b2d3526d3a72ad7c4b124aae5838245a8bc64a",
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
                "value": "0.10050102",
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

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret-key` option.

> **Example** -> swap bitcoin `sign` command

**Root XPrivate Key** _(str)_ -> tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4Y... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin signed transaction raw.

```shell script
$ swap bitcoin sign --root-xprivate-key tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR --transaction-raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMTAwMDAwMDAwZmZmZmZmZmYwMjgwOTY5ODAwMDAwMDAwMDAxN2E5MTQ5NDE4ZmVlZDQ2NDdlMTU2ZDY2NjNkYjNlMGNlZjdjMDUwZDAzODY3ODdmZDg4YzYwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDIzMDExODc1LCAidHhfb3V0cHV0X24iOiAxLCAic2NyaXB0IjogIjc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjIn1dLCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3Vuc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMTAwMDAwMDZhNDczMDQ0MDIyMDczZjFiODVmMGQzZWYwMmU1YjhkOTRjNzc4NzhiOWQzYzUzZjIyMGNjNmZiMjMyNDc0MDgxYzlmNTdhOTdmMzgwMjIwMTFhZjQ2MDU3ODU1NTVhMDgwNjRjOTJkZjVhOGE1NzM4OTQzNTRlMWI4M2NiM2Y2Njk0YmE5NWVlZGU1NDFkODAxMjEwMjM5Y2ZkODg2NTQyOGYxMjQ4YzVlNDIzNTc4ZWIwYzk4NzE1OTk0NDFiZDJmNzdkODNiNmQ1NGIzMzliN2RhNWNmZmZmZmZmZjAyODA5Njk4MDAwMDAwMDAwMDE3YTkxNDk0MThmZWVkNDY0N2UxNTZkNjY2M2RiM2UwY2VmN2MwNTBkMDM4Njc4N2ZkODhjNjAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAiZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9
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
$ swap bitcoin submit --transaction-raw eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTRhYzY4YjVhMjQzODU4YWU0YTEyNGI3Y2FkNzIzYTZkNTJkM2IyNjk2NDVmM2I5YTJmZWNjNzVmZDNhNzFkMTYwMDAwMDAwMDAwZmZmZmZmZmYwMTM2NWE5OTAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDA1MDY3OCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
e1b89dae0285d4303d4c3adf529465a2c84a20c2b8ee30a5005f85d88fa8a0b0
```
</details>
