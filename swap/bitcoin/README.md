# CLI - Bitcoin Commands

<img align="right" height="75" src="https://github.com/meherett/shuttle/blob/master/docs/static/svg/bitcoin.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Claim Command](#claim-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

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

## HTLC Command

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
  -sq, --sequence INTEGER        Set Bitcoin sequence/expiration block.
  -n, --network TEXT             Set Bitcoin network.
  -h, --help                     Show this message and exit.
```
</details>

> **Example** -> shuttle bitcoin `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Address** _(str)_ -> mwHXvCcug5Rn24c2rpgcRDSo3PyfxZJQQT **[required]**<br/>
**Sender Address** _(str)_ -> miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ shuttle bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-address mwHXvCcug5Rn24c2rpgcRDSo3PyfxZJQQT --sender-address miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ --sequence 1000 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac68
```
</details>

## Fund Command

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

**Sender Address** _(str)_ -> miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**bytecode** _(str)_ -> 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac68 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned fund transaction raw.

```shell script
$ shuttle bitcoin fund --sender-address miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ --amount 10000 --bytecode 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac68 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWQ1ODYyMDNiNWZhZjhmZGMyMTVhMDVkYWI3NGFhNTc5M2MyMWM0Mjk1NmEzM2RkMjQ1MDlhNTM4ZWI5YzJhMjgwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODc5NjlhNGQwMDAwMDAwMDAwMTk3NmE5MTQxZDBmNjcxYzI2YTNlZjdhODY1ZDFlZGEwZmJkMDg1ZTk4YWRjYzIzODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA1MDk2NTI0LCAibiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0MWQwZjY3MWMyNmEzZWY3YTg2NWQxZWRhMGZiZDA4NWU5OGFkY2MyMzg4YWMifV0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ==
```
</details>

## Claim Command

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

**Transaction Id** _(str)_ -> 31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135 **[required]**<br/>
**Recipient Address** _(str)_ -> mwHXvCcug5Rn24c2rpgcRDSo3PyfxZJQQT **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned claim transaction raw.

```shell script
$ shuttle bitcoin claim --transaction 31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135 --recipient-address mwHXvCcug5Rn24c2rpgcRDSo3PyfxZJQQT --amount 10000 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTM1NzEzYjIwODllOGIyOWI1N2Q5YWQzMzczN2YwMTIyNGU4ZjgyOWYzMmUyNWQ0ZjMzMGY0YWMxZWM3ZDUwMzEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNGFjZjg0MTllZWNhYjU3NGM0OTRmZWJiZTAzZmQwN2ZkYWU3YmYyZjQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0NDY5NTEyN2IxZDE3YzQ1NGY0YmFlOWM0MWNiOGUzY2RiNWU4OWQyNDg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0=
```
</details>

## Refund Command

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

**Transaction Id** _(str)_ -> 31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135 **[required]**<br/>
**Sender Address** _(str)_ -> miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Version** _(int)_ -> 2 **[default: `2`]**<br/>
**Network** _(str)_ -> testnet **[default: `testnet`]**<br/>

> **Returns** _(str)_ -> Bitcoin unsigned refund transaction raw.

```shell script
$ shuttle bitcoin refund --transaction 31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135 --sender-address miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ --amount 10000 --version 2 --network testnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTM1NzEzYjIwODllOGIyOWI1N2Q5YWQzMzczN2YwMTIyNGU4ZjgyOWYzMmUyNWQ0ZjMzMGY0YWMxZWM3ZDUwMzEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDFkMGY2NzFjMjZhM2VmN2E4NjVkMWVkYTBmYmQwODVlOThhZGNjMjM4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0NDY5NTEyN2IxZDE3YzQ1NGY0YmFlOWM0MWNiOGUzY2RiNWU4OWQyNDg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

## Decode Command

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
$ shuttle bitcoin decode --raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWQ1ODYyMDNiNWZhZjhmZGMyMTVhMDVkYWI3NGFhNTc5M2MyMWM0Mjk1NmEzM2RkMjQ1MDlhNTM4ZWI5YzJhMjgwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODc5NjlhNGQwMDAwMDAwMDAwMTk3NmE5MTQxZDBmNjcxYzI2YTNlZjdhODY1ZDFlZGEwZmJkMDg1ZTk4YWRjYzIzODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA1MDk2NTI0LCAibiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0MWQwZjY3MWMyNmEzZWY3YTg2NWQxZWRhMGZiZDA4NWU5OGFkY2MyMzg4YWMifV0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ==
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 678,
    "type": "bitcoin_fund_unsigned",
    "tx": {
        "hex": "0200000001d586203b5faf8fdc215a05dab74aa5793c21c42956a33dd24509a538eb9c2a280100000000ffffffff0210210000000000000017a9144695127b1d17c454f4bae9c41cb8e3cdb5e89d2487969a4d00000000001976a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac00000000",
        "txid": "4d9a6993307b96d7b1ba665fd18bc2479ff7371d5847f625c6eed9c234f76658",
        "hash": "4d9a6993307b96d7b1ba665fd18bc2479ff7371d5847f625c6eed9c234f76658",
        "size": 117,
        "vsize": 117,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "282a9ceb38a50945d23da35629c4213c79a54ab7da055a21dc8faf5f3b2086d5",
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
                    "asm": "OP_HASH160 4695127b1d17c454f4bae9c41cb8e3cdb5e89d24 OP_EQUAL",
                    "hex": "a9144695127b1d17c454f4bae9c41cb8e3cdb5e89d2487",
                    "type": "p2sh",
                    "address": "2MygRsRs6En1RCj8a88FfsK1QBeissBTswL"
                }
            },
            {
                "value": "0.05085846",
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 1d0f671c26a3ef7a865d1eda0fbd085e98adcc23 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac",
                    "type": "p2pkh",
                    "address": "miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ"
                }
            }
        ]
    },
    "network": "testnet"
}
```
</details>

## Sign Command

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
  -b, --bytecode TEXT    Set Bitcoin witness HTLC bytecode.  [required for claim/refund]
  -s, --secret TEXT      Set secret key. [required for claim]
  -sq, --sequence TEXT   Set sequens/expriration block. [optinal for refund]
  -v, --version INTEGER  Set Bitcoin transaction version.  [default: 2]
  -h, --help             Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing unsigned `claim` transaction you have to be use `--secret` option it's required.

> **Example** -> shuttle bitcoin `sign` command

**Private Key** _(str)_ -> 0a4628c5ae0771b1d27ac71e2d2574dec4174f35fa0a6c5e7e0f98871fbcc657 **[required]**<br/>
**Raw** _(str)_ -> eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4O... **[required]**<br/>

> **Returns** _(str)_ -> Bitcoin signed transaction raw.

```shell script
$ shuttle bitcoin sign --private 0a4628c5ae0771b1d27ac71e2d2574dec4174f35fa0a6c5e7e0f98871fbcc657 --raw eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWQ1ODYyMDNiNWZhZjhmZGMyMTVhMDVkYWI3NGFhNTc5M2MyMWM0Mjk1NmEzM2RkMjQ1MDlhNTM4ZWI5YzJhMjgwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODc5NjlhNGQwMDAwMDAwMDAwMTk3NmE5MTQxZDBmNjcxYzI2YTNlZjdhODY1ZDFlZGEwZmJkMDg1ZTk4YWRjYzIzODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA1MDk2NTI0LCAibiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0MWQwZjY3MWMyNmEzZWY3YTg2NWQxZWRhMGZiZDA4NWU5OGFkY2MyMzg4YWMifV0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ==
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJyYXciOiAiMDIwMDAwMDAwMWQ1ODYyMDNiNWZhZjhmZGMyMTVhMDVkYWI3NGFhNTc5M2MyMWM0Mjk1NmEzM2RkMjQ1MDlhNTM4ZWI5YzJhMjgwMTAwMDAwMDZhNDczMDQ0MDIyMDQzMmI1ZTdlNWIyNDBiYzY0MjFjN2RlN2ZiMTlmZDMzNWE2ZGU3MWNjNGFjNTNiMWE5NjYxN2QxNWQ3YzJlODkwMjIwN2RlZmZkMmNiMzE1NGNmMmYxMjA2ZDI5YWEyZjRhY2FkZDljOTdiNjFhZWVjNjM0OTYyN2QxYjU0NzZjOTlhZjAxMjEwMzM3M2EwMTMwNDRiYjllODYwMmNlN2UyYWUyN2M3NjVmNTUwNDQ3YzI0ODJmZGVhNjc1NzRjNTkyZjVlNjU1NGVmZmZmZmZmZjAyMTAyNzAwMDAwMDAwMDAwMDE3YTkxNDQ2OTUxMjdiMWQxN2M0NTRmNGJhZTljNDFjYjhlM2NkYjVlODlkMjQ4Nzk2OWE0ZDAwMDAwMDAwMDAxOTc2YTkxNDFkMGY2NzFjMjZhM2VmN2E4NjVkMWVkYTBmYmQwODVlOThhZGNjMjM4OGFjMDAwMDAwMDAiLCAiZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9
```
</details>

## Submit Command

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
$ shuttle bitcoin submit --raw eyJyYXciOiAiMDIwMDAwMDAwMWQ1ODYyMDNiNWZhZjhmZGMyMTVhMDVkYWI3NGFhNTc5M2MyMWM0Mjk1NmEzM2RkMjQ1MDlhNTM4ZWI5YzJhMjgwMTAwMDAwMDZhNDczMDQ0MDIyMDQzMmI1ZTdlNWIyNDBiYzY0MjFjN2RlN2ZiMTlmZDMzNWE2ZGU3MWNjNGFjNTNiMWE5NjYxN2QxNWQ3YzJlODkwMjIwN2RlZmZkMmNiMzE1NGNmMmYxMjA2ZDI5YWEyZjRhY2FkZDljOTdiNjFhZWVjNjM0OTYyN2QxYjU0NzZjOTlhZjAxMjEwMzM3M2EwMTMwNDRiYjllODYwMmNlN2UyYWUyN2M3NjVmNTUwNDQ3YzI0ODJmZGVhNjc1NzRjNTkyZjVlNjU1NGVmZmZmZmZmZjAyMTAyNzAwMDAwMDAwMDAwMDE3YTkxNDQ2OTUxMjdiMWQxN2M0NTRmNGJhZTljNDFjYjhlM2NkYjVlODlkMjQ4Nzk2OWE0ZDAwMDAwMDAwMDAxOTc2YTkxNDFkMGY2NzFjMjZhM2VmN2E4NjVkMWVkYTBmYmQwODVlOThhZGNjMjM4OGFjMDAwMDAwMDAiLCAiZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135
```
</details>
