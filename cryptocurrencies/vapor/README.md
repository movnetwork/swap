# CLI - Vapor Commands

<img align="right" height="70" src="https://github.com/meherett/swap/blob/master/docs/static/svg/vapor.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Claim Command](#claim-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `vapor` command

```shell script
$ swap vapor --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  claim   Select Vapor Claim transaction builder.
  decode  Select Vapor Transaction raw decoder.
  fund    Select Vapor Fund transaction builder.
  htlc    Select Vapor Hash Time Lock Contract (HTLC) builder.
  refund  Select Vapor Refund transaction builder.
  sign    Select Vapor Transaction raw signer.
  submit  Select Vapor Transaction raw submitter.
```
</details>

## HTLC Command

> $ swap vapor `htlc` command

```shell script
$ swap vapor htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT           Set secret 256 hash.  [required]
  -rpk, --recipient-public-key TEXT Set Vapor recipient public key.  [required]
  -spk, --sender-public-key TEXT    Set Vapor sender public key.  [required]
  -s, --sequence INTEGER            Set Vapor sequence/expiration block.  [default: 1000]
  -n, --network TEXT                Set Vapor network.  [default: mainnet]
  -i, --indent INTEGER              Set json indent.  [default: 4]
  -h, --help                        Show this message and exit.
```
</details>

> **Example** -> swap vapor `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ swap vapor htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public-key 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public-key 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 --sequence 1000 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
{
    "bytecode": "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0",
    "address": "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37"
}
```
</details>

## Fund Command

> $ swap vapor `fund` command

```shell script
$ swap vapor fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor fund [OPTIONS]

Options:
  -a, --address TEXT        Set Vapor sender address.  [required]
  -ha, --htlc-address TEXT  Set Vapor Hash Time Lock Contract (HTLC) address.  [required]
  -am, --amount FLOAT       Set Vapor fund amount.  [required]
  -u, --unit TEXT           Set Vapor amount unit.  [default: NEU]
  -as, --asset TEXT         Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT        Set Vapor network.  [default: mainnet]
  -h, --help                Show this message and exit.
```
</details>

> **Example** -> swap vapor `fund` command

**Sender Address** _(str)_ -> vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag **[required]**<br/>
**HTLC Address** _(str)_ -> vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37 **[required]**<br/>
**Amount** _(int, float)_ -> 0.1 **[required]**<br/>
**Unit** _(str)_ -> BTM **[default: `NEU`]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned fund transaction raw.

```shell script
$ swap vapor fund --address vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag --htlc-address vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37 --amount 0.1 --unit BTM --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDJlMWY1Njc2YTc3ZjE1M2U0MTI5MDUzMTVmZTgyMzNkYTU0ODRhZGViNjNlMDgwYTFjZTUxYjE0ODE0Mjc5NGFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzA4NGY4MTYwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkOGEzZmExMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgImhhc2giOiAiMDRmOGY2M2RjM2Y2NDIwNGI4MzdmYWQxNWE1MmM5ZjIxYTkxZjM0NGEyYzI1ZDYyN2RjMWQxMzdjOTU1Y2U0MiIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJiMGFiYTkxNDE2OWQxYmVlYWJhOGIzM2Y0YmI2YmMxZWJiMDUxYjUyZjI4YWVmN2EzNThkNjAwNDk0MzVmZmFiIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0=
```
</details>

## Claim Command

> $ swap vapor `claim` command

```shell script
$ swap vapor claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor claim [OPTIONS]

Options:
  -a, --address TEXT          Set Vapor recipient address.  [required]
  -ti, --transaction-id TEXT  Set Vapor funded transaction id/hash.  [required]
  -am, --amount FLOAT         Set Vapor withdraw amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Vapor withdraw max amount.  [default: True]
  -u, --unit TEXT             Set Vapor withdraw amount unit.  [default: NEU]
  -as, --asset TEXT           Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Vapor network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `claim` command

**Recipient Address** _(str)_ -> vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h **[required]**<br/>
**Transaction Id** _(str)_ -> 96db48d3f3a4d9f3e490bcb3e1ad1cc8b11f8e51ceee816ecf6085374c824f0e **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned claim transaction raw.

```shell script
$ swap vapor claim --address vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h --transaction-id 96db48d3f3a4d9f3e490bcb3e1ad1cc8b11f8e51ceee816ecf6085374c824f0e --max-amount True --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxY3l2azM3IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5Y2Y1NGU5NGIwMzQ5NTQ5YTU4NmJjMGE3MGNiNTZiZjJlZGExZDNlOWVjMjkwZjBiMzQ4OTg0MjQzNDAxNzZiZWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGU3ODAwNTAwMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZDBiM2U1MDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogIjk5OTkwNGZkYjdkOTgwNjNjYzdmZmVlNzgxN2U2NjVkMDZmNjdhYjM4MmRlM2IzZGU5YTQ4MmIxNDExMDNlZWUiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZWI4ZGU1ZGMxYzJkNjBhMjVjYTdjZjZlMzQwNjFmODc3ZjEzOWZmZjBiMmQ2NTg2YmU3MTYxZWZkMTQ2NmZjZSJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9jbGFpbV91bnNpZ25lZCJ9
```
</details>

## Refund Command

> $ swap vapor `refund` command

```shell script
$ swap vapor refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor refund [OPTIONS]

Options:
  -a, --address TEXT          Set Vapor sender address.  [required]
  -ti, --transaction-id TEXT  Set Vapor funded transaction id/hash.  [required]
  -am, --amount FLOAT         Set Vapor refund amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Vapor refund max amount.  [default: True]
  -u, --unit TEXT             Set Vapor refund amount unit.  [default: NEU]
  -as, --asset TEXT           Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Vapor network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `refund` command

**Sender Address** _(str)_ -> vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag **[required]**<br/>
**Transaction Id** _(str)_ -> 96db48d3f3a4d9f3e490bcb3e1ad1cc8b11f8e51ceee816ecf6085374c824f0e **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned refund transaction raw.

```shell script
$ swap vapor refund --address vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag --transaction-id 96db48d3f3a4d9f3e490bcb3e1ad1cc8b11f8e51ceee816ecf6085374c824f0e --max-amount True --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxY3l2azM3IiwgImhhc2giOiAiNjA5MDdlMjU5YWVjOTAwYmU4MzU3ZGJjNWYyOTY3ZjJhYmU4MThhYjU1OGViYjdmNDNlMTJlNjU0YWM3OTMzZSIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWNmNTRlOTRiMDM0OTU0OWE1ODZiYzBhNzBjYjU2YmYyZWRhMWQzZTllYzI5MGYwYjM0ODk4NDI0MzQwMTc2YmVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhlNzgwMDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwYjNlNTA0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMjcxMzM4NDY0NDlkODNjM2Q4Njc4MjA2YWFjNTYzM2FlMDNkNjAwZjc1YzU3OGY0MmFjM2Y4ZDgzNmE1MDc4NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ==
```
</details>

## Decode Command

> $ swap vapor `decode` command

```shell script
$ swap vapor decode --help
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

**Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzh... **[required]**<br/>

> **Returns** _(str)_ -> Vapor transaction json.

```shell script
$ swap vapor decode --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxY3l2azM3IiwgImhhc2giOiAiNjA5MDdlMjU5YWVjOTAwYmU4MzU3ZGJjNWYyOTY3ZjJhYmU4MThhYjU1OGViYjdmNDNlMTJlNjU0YWM3OTMzZSIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWNmNTRlOTRiMDM0OTU0OWE1ODZiYzBhNzBjYjU2YmYyZWRhMWQzZTllYzI5MGYwYjM0ODk4NDI0MzQwMTc2YmVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhlNzgwMDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwYjNlNTA0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMjcxMzM4NDY0NDlkODNjM2Q4Njc4MjA2YWFjNTYzM2FlMDNkNjAwZjc1YzU3OGY0MmFjM2Y4ZDgzNmE1MDc4NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ==
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 449000,
    "address": "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37",
    "type": "vapor_refund_unsigned",
    "tx": {
        "tx_id": "60907e259aec900be8357dbc5f2967f2abe818ab558ebb7f43e12e654ac7933e",
        "version": 1,
        "size": 181,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10499000,
                "control_program": "00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc",
                "address": "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37",
                "spent_output_id": "656b127a5888997322590f6d019586ae89f710450d068f02e0c9a87ba131814e",
                "input_id": "59c808cbf68151e5b7f7a7ff164ed34b4846d7794bc44f52ddf9dbc957ddb6cd",
                "witness_arguments": null
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "59552686f610494fbac851a40edaf32d1271d0131a1f10ca56e4f6e355e02736",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10050000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
            }
        ],
        "fee": 449000
    },
    "unsigned_datas": [
        {
            "datas": [
                "27133846449d83c3d8678206aac5633ae03d600f75c578f42ac3f8d836a50784"
            ],
            "network": "mainnet",
            "path": null
        }
    ],
    "signatures": [],
    "network": "mainnet"
}
```
</details>

## Sign Command

> $ swap vapor `sign` command

```shell script
$ swap vapor sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap vapor sign [OPTIONS]

Options:
  -xk, --xprivate-key TEXT     Set Vapor xprivate key.  [required]
  -tr, --transaction-raw TEXT  Set Vapor unsigned transaction raw.  [required]
  -b, --bytecode TEXT          Set Vapor witness HTLC bytecode.  [default: None]
  -sk, --secret-key TEXT       Set secret key.  [default: None]
  -ac, --account INTEGER       Set Vapor derivation from account.  [default: 1]
  -ch, --change BOOLEAN        Set Vapor derivation from change.  [default: False]
  -ad, --address INTEGER       Set Vapor derivation from address.  [default: 1]
  -p, --path TEXT              Set Vapor derivation from path.  [default: None]
  -i, --indexes LIST           Set Vapor derivation from indexes.  [default: None]
  -h, --help                   Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret-key` option.

> **Example** -> swap vapor `sign` command

**XPrivate Key** _(str)_ -> 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bH... **[required]**<br/>

> **Returns** _(str)_ -> Vapor signed transaction raw.

```shell script
$ swap vapor sign --xprivate-key 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDJlMWY1Njc2YTc3ZjE1M2U0MTI5MDUzMTVmZTgyMzNkYTU0ODRhZGViNjNlMDgwYTFjZTUxYjE0ODE0Mjc5NGFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzA4NGY4MTYwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkOGEzZmExMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgImhhc2giOiAiMDRmOGY2M2RjM2Y2NDIwNGI4MzdmYWQxNWE1MmM5ZjIxYTkxZjM0NGEyYzI1ZDYyN2RjMWQxMzdjOTU1Y2U0MiIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJiMGFiYTkxNDE2OWQxYmVlYWJhOGIzM2Y0YmI2YmMxZWJiMDUxYjUyZjI4YWVmN2EzNThkNjAwNDk0MzVmZmFiIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDJlMWY1Njc2YTc3ZjE1M2U0MTI5MDUzMTVmZTgyMzNkYTU0ODRhZGViNjNlMDgwYTFjZTUxYjE0ODE0Mjc5NGFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzA4NGY4MTYwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkOGEzZmExMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgImhhc2giOiAiMDRmOGY2M2RjM2Y2NDIwNGI4MzdmYWQxNWE1MmM5ZjIxYTkxZjM0NGEyYzI1ZDYyN2RjMWQxMzdjOTU1Y2U0MiIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJiMGFiYTkxNDE2OWQxYmVlYWJhOGIzM2Y0YmI2YmMxZWJiMDUxYjUyZjI4YWVmN2EzNThkNjAwNDk0MzVmZmFiIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siNTY5MDIyOGMwN2FmOTgxNjRmMjZhMGFkZWRlZGU0ZDllNDY4MDg0YmFlYmE3ODEyNzQyNTQ2ZTI5YmZhMTAxOTA0Mzc5MjI5ZWZhZGU0M2VkN2FkYTE2NjM0ZGFhNWNmOTFjYzA1MzIyOTJlOTQ3NThkNTdmMzk0MzJjMjlhMDEiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3NpZ25lZCJ9
```
</details>

## Submit Command

> $ swap vapor `submit` command

```shell script
$ swap vapor submit --help
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

**Signed Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzhzYXp... **[required]**<br/>

> **Returns** _(str)_ -> Vapor blockchain transaction id.

```shell script
$ swap vapor submit --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxY3l2azM3IiwgImhhc2giOiAiNjA5MDdlMjU5YWVjOTAwYmU4MzU3ZGJjNWYyOTY3ZjJhYmU4MThhYjU1OGViYjdmNDNlMTJlNjU0YWM3OTMzZSIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWNmNTRlOTRiMDM0OTU0OWE1ODZiYzBhNzBjYjU2YmYyZWRhMWQzZTllYzI5MGYwYjM0ODk4NDI0MzQwMTc2YmVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhlNzgwMDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwYjNlNTA0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMjcxMzM4NDY0NDlkODNjM2Q4Njc4MjA2YWFjNTYzM2FlMDNkNjAwZjc1YzU3OGY0MmFjM2Y4ZDgzNmE1MDc4NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ
```

<details>
  <summary>Output</summary><br/>

```shell script
60907e259aec900be8357dbc5f2967f2abe818ab558ebb7f43e12e654ac7933e
```
</details>
