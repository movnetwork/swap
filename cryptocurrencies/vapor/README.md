# CLI - Vapor Commands

<img align="right" height="80" src="https://github.com/meherett/swap/blob/master/docs/static/svg/vapor.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Withdraw Command](#withdraw-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `vapor` command

```shell script
swap vapor --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode    Select Vapor Transaction raw decoder.
  fund      Select Vapor Fund transaction builder.
  htlc      Select Vapor Hash Time Lock Contract (HTLC) builder.
  refund    Select Vapor Refund transaction builder.
  sign      Select Vapor Transaction raw signer.
  submit    Select Vapor Transaction raw submitter.
  withdraw  Select Vapor Withdraw transaction builder.
```
</details>

## HTLC Command

> $ swap vapor `htlc` command

```shell script
swap vapor htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT         Set secret 256 hash.  [required]
  -rpk, --recipient-public-key TEXT
                                  Set Vapor recipient public key.  [required]
  -spk, --sender-public-key TEXT  Set Vapor sender public key.  [required]
  -e, --endblock INTEGER          Set Vapor expiration block height.
                                  [required]

  -n, --network TEXT              Set Vapor network.  [default: mainnet]
  -i, --indent INTEGER            Set json indent.  [default: 4]
  -h, --help                      Show this message and exit.
```
</details>

> **Example** -> swap vapor `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212 **[required]**<br/>
**Endblock** _(int)_ -> 120723497 **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor Hash Time Lock Contract (HTLC) bytecode.

```shell script
swap vapor htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public-key 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public-key fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212 --endblock 120723497 --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
{
    "secret_hash": "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
    "recipient": {
        "public_key": "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e",
        "address": "vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h"
    },
    "sender": {
        "public_key": "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212",
        "address": "vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs"
    },
    "endblock": 120723497,
    "bytecode": "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0",
    "contract_address": "vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc"
}
```
</details>

## Fund Command

> $ swap vapor `fund` command

```shell script
swap vapor fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor fund [OPTIONS]

Options:
  -a, --address TEXT            Set Vapor sender address.  [required]
  -ca, --contract-address TEXT  Set Vapor Hash Time Lock Contract (HTLC)
                                address.  [required]

  -am, --amount FLOAT           Set Vapor fund amount.  [required]
  -u, --unit TEXT               Set Vapor amount unit.  [default: NEU]
  -as, --asset TEXT             Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Vapor network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap vapor `fund` command

**Sender Address** _(str)_ -> vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs **[required]**<br/>
**Contract Address** _(str)_ -> vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc **[required]**<br/>
**Amount** _(int, float)_ -> 0.1 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Unit** _(str)_ -> BTM **[default: `NEU`]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned fund transaction raw.

```shell script
swap vapor fund --address vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs --contract-address vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc --amount 0.1 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --unit BTM --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0=
```
</details>

## Withdraw Command

> $ swap vapor `withdraw` command

```shell script
swap vapor withdraw --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor withdraw [OPTIONS]

Options:
  -a, --address TEXT            Set Vapor recipient address.  [required]
  -th, --transaction-hash TEXT  Set Vapor funded transaction hash/id.
                                [required]

  -as, --asset TEXT             Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Vapor network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap vapor `withdraw` command

**Recipient Address** _(str)_ -> vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h **[required]**<br/>
**Transaction Hash** _(str)_ -> 37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned withdraw transaction raw.

```shell script
swap vapor withdraw --address vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h --transaction-hash 37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZGY4MmNmN2M3OTI3Nzg2YTY5NTY5Mzc3NDRlZTgyMzU0YzQ4MWIwZjIxMWFjNTJhNWMxZDc0NGM0ZTNlNzg2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogIjkwNGFlZGExOTlmMDVjYmI3NjcxZTBkOWVjOTViMzA5MWYzYzEzMWNlZjhkNjM0YWUxNzIxNmI5YzJmZWE0OGMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiM2ExMjNmZDgwOWQzYWQ4NDVhOTJhZDNlNWExZjBjYzEwM2RlNTExYWRmOTVjZjMwMjQwZDkxNjRkNmZmMTk2NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl93aXRoZHJhd191bnNpZ25lZCJ9
```
</details>

## Refund Command

> $ swap vapor `refund` command

```shell script
swap vapor refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor refund [OPTIONS]

Options:
  -a, --address TEXT            Set Vapor sender address.  [required]
  -th, --transaction-hash TEXT  Set Vapor funded transaction id/hash.
                                [required]

  -as, --asset TEXT             Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Vapor network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap vapor `refund` command

**Sender Address** _(str)_ -> vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs **[required]**<br/>
**Transaction Hash** _(str)_ -> 37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned refund transaction raw.

```shell script
swap vapor refund --address vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs --transaction-hash 37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgImhhc2giOiAiNmQ5NjQyMjIyYmFmYjlkNjk2OGVlMmVlZDk4OGM4MzdiMWRhNTZmY2VjNmZkOTYzMjlmZmY4YzBkNTUxOGY5MiIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwMzRhM2RiNTAzMDFiOTQxYjhlZDQzZGNmZGJkMzM4MWRmMWI3MzlmYTY0YWI3N2U0MjY0ZjcwM2E0NWUwYmUzMTAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmI4YTRjMzA0MDExNjAwMTRiMTU5MmFjYmI5MTdmMTM5MzcxNjZjMmE5YjZjZTk3MzI5NmViYjYwMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNmIyNGM0NDM4OTY2MWY4YzU3MDE0NmVjNGNjOGQzYWQzZjJkN2YxNjA3MTM2MjBiZTc0MzgwZTQwYmMwNmMwYyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ==
```
</details>

## Decode Command

> $ swap vapor `decode` command

```shell script
swap vapor decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor decode [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set Vapor transaction raw.  [required]
  -i, --indent INTEGER         Set json indent.  [default: 4]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap vapor `decode` command

**Transaction Raw** _(str)_ -> eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnB... **[required]**<br/>

> **Returns** _(str)_ -> Vapor transaction json.

```shell script
swap vapor decode --transaction-raw eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZGY4MmNmN2M3OTI3Nzg2YTY5NTY5Mzc3NDRlZTgyMzU0YzQ4MWIwZjIxMWFjNTJhNWMxZDc0NGM0ZTNlNzg2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogIjZkOTY0MjIyMmJhZmI5ZDY5NjhlZTJlZWQ5ODhjODM3YjFkYTU2ZmNlYzZmZDk2MzI5ZmZmOGMwZDU1MThmOTIiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNmIyNGM0NDM4OTY2MWY4YzU3MDE0NmVjNGNjOGQzYWQzZjJkN2YxNjA3MTM2MjBiZTc0MzgwZTQwYmMwNmMwYyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW1siNWFmNzE0NWYwOWY0M2ZhYzI4ZmZiOTE1M2QxNmQ2YzQwZGM2MTA3MzU2NjRlN2YxN2MyNmRmNTFmZGZhNDQ1MGIyN2QwZTlhMWJmNzA3MDk0MzczYWYwZmJiOTAyZTI2YjU2ZTk1ZjY5Y2RmZWMwMDI0Mjc4ZTc1ZjhhY2UwMDUiLCAiMDEiLCAiMDQyY2NmMzAwNzIwZmU2YjNmZDQ0NTgyOTFiMTk2MDVkOTI4MzdhZTEwNjBjYzAyMzdlNjgwMjJiMmViOWZhZjAxYTExODIyNjIxMjIwM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTIwM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjc0MWY1NDdhNjQxNjAwMDAwMDU1N2FhODg4NTM3YTdjYWU3Y2FjNjMxZjAwMDAwMDUzN2FjZDlmNjk3MmFlN2NhYzAwYzAiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfc2lnbmVkIn0
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "fee": 509000,
    "address": "vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc",
    "type": "vapor_refund_signed",
    "tx": {
        "tx_id": "6d9642222bafb9d6968ee2eed988c837b1da56fcec6fd96329fff8c0d5518f92",
        "version": 1,
        "size": 181,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000000,
                "control_program": "002034a3db50301b941b8ed43dcfdbd3381df1b739fa64ab77e4264f703a45e0be31",
                "address": "vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc",
                "spent_output_id": "144dd8355cae0d9aea6ca3fb1ff685fb7b455b1f9cb0c5992c9035844c664ad1",
                "input_id": "576edbd5cf8682fb82eb8fb61ba3d6f25a9490777be607d2e75b2dbcbbceb89e",
                "witness_arguments": null
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "b6a843f8257fc06ad922a69fa2cfa413277703ffb04512a35799d3c8a2c5d7a2",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 9491000,
                "control_program": "0014b1592acbb917f13937166c2a9b6ce973296ebb60",
                "address": "vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs"
            }
        ],
        "fee": 509000
    },
    "unsigned_datas": [
        {
            "datas": [
                "6b24c44389661f8c570146ec4cc8d3ad3f2d7f160713620be74380e40bc06c0c"
            ],
            "network": "mainnet",
            "path": null
        }
    ],
    "signatures": [
        [
            "5af7145f09f43fac28ffb9153d16d6c40dc610735664e7f17c26df51fdfa4450b27d0e9a1bf707094373af0fbb902e26b56e95f69cdfec0024278e75f8ace005",
            "01",
            "042ccf300720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        ]
    ],
    "network": "mainnet"
}
```
</details>

## Sign Command

> $ swap vapor `sign` command

```shell script
swap vapor sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor sign [OPTIONS]

Options:
  -xpk, --xprivate-key TEXT    Set Vapor xprivate key.  [required]
  -tr, --transaction-raw TEXT  Set Vapor unsigned transaction raw.  [required]
  -b, --bytecode TEXT          Set Vapor witness HTLC bytecode.  [default:
                               None]

  -sk, --secret-key TEXT       Set secret key.  [default: None]
  -ac, --account INTEGER       Set Vapor derivation from account.  [default:
                               1]

  -ch, --change BOOLEAN        Set Vapor derivation from change.  [default:
                               False]

  -ad, --address INTEGER       Set Vapor derivation from address.  [default:
                               1]

  -p, --path TEXT              Set Vapor derivation from path.  [default:
                               None]

  -i, --indexes LIST           Set Vapor derivation from indexes.  [default:
                               None]

  -h, --help                   Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `withdraw` transaction you have to be use `--secret-key` option.

> **Example** -> swap vapor `sign` command

**XPrivate Key** _(str)_ -> 58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZX... **[required]**<br/>

> **Returns** _(str)_ -> Vapor signed transaction raw.

```shell script
swap vapor sign --xprivate-key 58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMGQyZTRlNDJmY2VlODYzZTc0MTk1ZGNlYWIxZGZjY2YzNjgwNTViMTcxMTk2ZmFhOTBjNTNlYWEyY2VhNjQ5YmI0M2NjMTMyMzU0ZWRhZDk3MGIzNTZhYWU1ZDYyOGRkMDE2MGU3ODdhYzE3NGFmODljYTUzNGQxNGRiNzFlMDAiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3NpZ25lZCJ9
```
</details>

## Submit Command

> $ swap vapor `submit` command

```shell script
swap vapor submit --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor submit [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set signed Vapor transaction raw.  [required]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap vapor `submit` command

**Signed Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25... **[required]**<br/>

> **Returns** _(str)_ -> Vapor blockchain transaction id.

```shell script
swap vapor submit --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMGQyZTRlNDJmY2VlODYzZTc0MTk1ZGNlYWIxZGZjY2YzNjgwNTViMTcxMTk2ZmFhOTBjNTNlYWEyY2VhNjQ5YmI0M2NjMTMyMzU0ZWRhZDk3MGIzNTZhYWU1ZDYyOGRkMDE2MGU3ODdhYzE3NGFmODljYTUzNGQxNGRiNzFlMDAiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3NpZ25lZCJ9
```

<details open>
  <summary>Output</summary><br/>

```shell script
a09f3093aaff6c8c8f1a372eac68571ceea4928ccc8b9b54954863758447dec1
```
</details>
