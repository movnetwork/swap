# CLI - Bytom Commands

<img align="right" height="80" src="https://github.com/meherett/swap/blob/master/docs/static/svg/bytom.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Withdraw Command](#withdraw-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `bytom` command

```shell script
swap bytom --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode    Select Bytom Transaction raw decoder.
  fund      Select Bytom Fund transaction builder.
  htlc      Select Bytom Hash Time Lock Contract (HTLC) builder.
  refund    Select Bytom Refund transaction builder.
  sign      Select Bytom Transaction raw signer.
  submit    Select Bytom Transaction raw submitter.
  withdraw  Select Bytom Withdraw transaction builder.
```
</details>

## HTLC Command

> $ swap bytom `htlc` command

```shell script
swap bytom htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT         Set secret 256 hash.  [required]
  -rpk, --recipient-public-key TEXT
                                  Set Bytom recipient public key.  [required]
  -spk, --sender-public-key TEXT  Set Bytom sender public key.  [required]
  -e, --endblock INTEGER          Set Bytom expiration block height. [required]

  -n, --network TEXT              Set Bytom network.  [default: mainnet]
  -i, --indent INTEGER            Set json indent.  [default: 4]
  -h, --help                      Show this message and exit.
```
</details>

> **Example** -> swap bytom `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212 **[required]**<br/>
**Endblock** _(int)_ -> 679208 **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom Hash Time Lock Contract (HTLC) bytecode.

```shell script
swap bytom htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public-key 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public-key fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212 --endblock 679208 --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
{
    "secret_hash": "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
    "recipient": {
        "public_key": "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e",
        "address": "bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p"
    },
    "sender": {
        "public_key": "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212",
        "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx"
    },
    "endblock": 679208,
    "bytecode": "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0",
    "contract_address": "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy"
}
```
</details>

## Fund Command

> $ swap bytom `fund` command

```shell script
swap bytom fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom fund [OPTIONS]

Options:
  -a, --address TEXT            Set Bytom sender address.  [required]
  -ca, --contract-address TEXT  Set Bytom Hash Time Lock Contract (HTLC)
                                address.  [required]

  -am, --amount FLOAT           Set Bytom fund amount.  [required]
  -u, --unit TEXT               Set Bytom amount unit.  [default: NEU]
  -as, --asset TEXT             Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Bytom network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bytom `fund` command

**Sender Address** _(str)_ -> bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx **[required]**<br/>
**Contract Address** _(str)_ -> bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy **[required]**<br/>
**Amount** _(int, float)_ -> 0.1 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Unit** _(str)_ -> BTM **[default: `NEU`]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned fund transaction raw.

```shell script
swap bytom fund --address bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx --contract-address bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy --amount 0.1 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --unit BTM --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```
</details>

## Withdraw Command

> $ swap bytom `withdraw` command

```shell script
swap bytom withdraw --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom withdraw [OPTIONS]

Options:
  -a, --address TEXT            Set Bytom recipient address.  [required]
  -th, --transaction-hash TEXT  Set Bytom funded transaction hash/id.
                                [required]

  -as, --asset TEXT             Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Bytom network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bytom `withdraw` command

**Recipient Address** _(str)_ -> bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p **[required]**<br/>
**Transaction Hash** _(str)_ -> 59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned withdraw transaction raw.

```shell script
swap bytom withdraw --address bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p --transaction-hash 59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZDFlODRjMzdmNDEwNTZmNGRmMzk4NTIzZjg0ZWNmMDc5Mzc3ZmQ4NWU0NTYxYzEwZWMwMzgxOGNkNGRiN2VjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI0NWQxNzQ2YTFlYzA2OTVkM2UwNjA1OWM0MTM4NzIwNDBkMjRmODY0OTlkZGFmYWI0ODE3NzM2OGU1YzcyODgzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3dpdGhkcmF3X3Vuc2lnbmVkIn0=
```
</details>

## Refund Command

> $ swap bytom `refund` command

```shell script
swap bytom refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom refund [OPTIONS]

Options:
  -a, --address TEXT            Set Bytom sender address.  [required]
  -th, --transaction-hash TEXT  Set Bytom funded transaction id/hash.
                                [required]

  -as, --asset TEXT             Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

  -n, --network TEXT            Set Bytom network.  [default: mainnet]
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> swap bytom `refund` command

**Sender Address** _(str)_ -> bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx **[required]**<br/>
**Transaction Hash** _(str)_ -> 59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned refund transaction raw.

```shell script
swap bytom refund --address bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx --transaction-hash 59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgImhhc2giOiAiMTcyMmFhOTMwZjZmOTNiNGM4Nzc4OGVhNTVmNDkwNTVmMjZmODY4MjFiY2QxMWE2NGQ0MmJjYjllM2I4YTk2ZCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwZTdmNGE5ODE1ZjNhMzZjNjE2YzU2NjZiOTdmYjdmZGFjZDM3MjBjMTE3ZDA3OGM0Mjk0OTRkMWI2MTdmZTdkNDAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJjYzc4YzFmYjY0OGY4ODI2ZTRkZDRmODVmODg1YWM3NTg2NmMwMjMzYjBhZjY1ODE3NTNkODU4MzA0YjhlMDRiIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

## Decode Command

> $ swap bytom `decode` command

```shell script
swap bytom decode --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom decode [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set Bytom transaction raw.  [required]
  -i, --indent INTEGER         Set json indent.  [default: 4]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap bytom `decode` command

**Transaction Raw** _(str)_ -> eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybD... **[required]**<br/>

> **Returns** _(str)_ -> Bytom transaction json.

```shell script
swap bytom decode --transaction-raw eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiMTcyMmFhOTMwZjZmOTNiNGM4Nzc4OGVhNTVmNDkwNTVmMjZmODY4MjFiY2QxMWE2NGQ0MmJjYjllM2I4YTk2ZCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJjYzc4YzFmYjY0OGY4ODI2ZTRkZDRmODVmODg1YWM3NTg2NmMwMjMzYjBhZjY1ODE3NTNkODU4MzA0YjhlMDRiIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbWyI5NjcwOWJjYTA2MDllYTQ3ZGZiN2NhNmM3ODc0ZGNlZWY3MDZkMzVmOGMyYWExZDU4YjFmOGQzYWM2MjgwZjE4NTIxNjQzMzgyMDgyNmEyMTM3ZmZlMDRhNjE0ZDQwMGZlYThhNWRmMjljOTQ2ZTNhYThlOWQ1MmNhYzZmNmQwYyIsICIwMSIsICIwMzI4NWQwYTIwZmU2YjNmZDQ0NTgyOTFiMTk2MDVkOTI4MzdhZTEwNjBjYzAyMzdlNjgwMjJiMmViOWZhZjAxYTExODIyNjIxMjIwM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTIwM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjc0MWY1NDdhNjQxNjAwMDAwMDU1N2FhODg4NTM3YTdjYWU3Y2FjNjMxZjAwMDAwMDUzN2FjZDlmNjk3MmFlN2NhYzAwYzAiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9yZWZ1bmRfc2lnbmVkIn0
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "fee": 509000,
    "address": "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy",
    "type": "bytom_refund_signed",
    "tx": {
        "tx_id": "1722aa930f6f93b4c87788ea55f49055f26f86821bcd11a64d42bcb9e3b8a96d",
        "version": 1,
        "size": 179,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000000,
                "control_program": "0020e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d4",
                "address": "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy",
                "spent_output_id": "1aaf7df33c1d41bc6108c93d8b6da6af1d7f68632f54516408a03ff86494a1f0",
                "input_id": "6ccb3abb96d713fcaf27548ed76dadc695259fb7570b38ab9cde23f7ec261d60",
                "witness_arguments": null,
                "sign_data": "cc78c1fb648f8826e4dd4f85f885ac75866c0233b0af6581753d858304b8e04b"
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "6f831e2f958252a20b8d5aa9242c7bda229cb0e35bd2101978ea7df6cd7cc728",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 9491000,
                "control_program": "0014b1592acbb917f13937166c2a9b6ce973296ebb60",
                "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx"
            }
        ],
        "fee": 509000
    },
    "unsigned_datas": [
        {
            "datas": [
                "cc78c1fb648f8826e4dd4f85f885ac75866c0233b0af6581753d858304b8e04b"
            ],
            "network": "mainnet",
            "path": null
        }
    ],
    "signatures": [
        [
            "96709bca0609ea47dfb7ca6c7874dceef706d35f8c2aa1d58b1f8d3ac6280f185216433820826a2137ffe04a614d400fea8a5df29c946e3aa8e9d52cac6f6d0c",
            "01",
            "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        ]
    ],
    "network": "mainnet"
}
```
</details>

## Sign Command

> $ swap bytom `sign` command

```shell script
swap bytom sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom sign [OPTIONS]

Options:
  -xpk, --xprivate-key TEXT    Set Bytom xprivate key.  [required]
  -tr, --transaction-raw TEXT  Set Bytom unsigned transaction raw.  [required]
  -b, --bytecode TEXT          Set Bytom witness HTLC bytecode.  [default:
                               None]

  -sk, --secret-key TEXT       Set secret key.  [default: None]
  -ac, --account INTEGER       Set Bytom derivation from account.  [default:
                               1]

  -ch, --change BOOLEAN        Set Bytom derivation from change.  [default:
                               False]

  -ad, --address INTEGER       Set Bytom derivation from address.  [default:
                               1]

  -p, --path TEXT              Set Bytom derivation from path.  [default:
                               None]

  -i, --indexes LIST           Set Bytom derivation from indexes.  [default:
                               None]

  -h, --help                   Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `withdraw` transaction you have to be use `--secret-key` option.

> **Example** -> swap bytom `sign` command

**XPrivate Key** _(str)_ -> 58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXp... **[required]**<br/>

> **Returns** _(str)_ -> Bytom signed transaction raw.

```shell script
swap bytom sign --xprivate-key 58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9
```

<details open>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtbImI4MmU5N2FiYzRiNzBmN2ZmZTdmNzgzMjU0YzYzZTYxNDM2ZDZhN2FkMTVkYTg5YjFmYjc5MWY5MWQxZDZhYTBiYWI3ZmY4NjMyOGVhYmQyOTU5ZjU0NzVkZGU0NDNlNjEzY2U3ZGZlNzA0MTFiZTViNDY5YjAyMDY5MTY0YTA2Il1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ==
```
</details>

## Submit Command

> $ swap bytom `submit` command

```shell script
swap bytom submit --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom submit [OPTIONS]

Options:
  -tr, --transaction-raw TEXT  Set signed Bytom transaction raw.  [required]
  -h, --help                   Show this message and exit.
```
</details>

> **Example** -> swap bytom `submit` command

**Signed Transaction Raw** _(str)_ -> eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhzYXp4cz... **[required]**<br/>

> **Returns** _(str)_ -> Bytom blockchain transaction id.

```shell script
swap bytom submit --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtbImI4MmU5N2FiYzRiNzBmN2ZmZTdmNzgzMjU0YzYzZTYxNDM2ZDZhN2FkMTVkYTg5YjFmYjc5MWY5MWQxZDZhYTBiYWI3ZmY4NjMyOGVhYmQyOTU5ZjU0NzVkZGU0NDNlNjEzY2U3ZGZlNzA0MTFiZTViNDY5YjAyMDY5MTY0YTA2Il1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ
```

<details open>
  <summary>Output</summary><br/>

```shell script
a3078af0810c68a7bb6f2f42cd67dce9dea3d77028ca0c527224e4524038abc4
```
</details>
