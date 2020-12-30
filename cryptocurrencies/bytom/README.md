# CLI - Bytom Commands

<img align="right" height="80" src="https://github.com/meherett/swap/blob/master/docs/static/svg/bytom.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Claim Command](#claim-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

> $ swap `bytom` command

```shell script
$ swap bytom --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  claim   Select Bytom Claim transaction builder.
  decode  Select Bytom Transaction raw decoder.
  fund    Select Bytom Fund transaction builder.
  htlc    Select Bytom Hash Time Lock Contract (HTLC) builder.
  refund  Select Bytom Refund transaction builder.
  sign    Select Bytom Transaction raw signer.
  submit  Select Bytom Transaction raw submitter.
```
</details>

## HTLC Command

> $ swap bytom `htlc` command

```shell script
$ swap bytom htlc --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom htlc [OPTIONS]

Options:
  -sh, --secret-hash TEXT           Set secret 256 hash.  [required]
  -rpk, --recipient-public-key TEXT Set Bytom recipient public key.  [required]
  -spk, --sender-public-key TEXT    Set Bytom sender public key.  [required]
  -s, --sequence INTEGER            Set Bytom sequence/expiration block.  [default: 1000]
  -n, --network TEXT                Set Bytom network.  [default: mainnet]
  -i, --indent INTEGER              Set json indent.  [default: 4]
  -h, --help                        Show this message and exit.
```
</details>

> **Example** -> swap bytom `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ swap bytom htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public-key 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public-key 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 --sequence 1000 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
{
    "bytecode": "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0",
    "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8"
}
```
</details>

## Fund Command

> $ swap bytom `fund` command

```shell script
$ swap bytom fund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom fund [OPTIONS]

Options:
  -a, --address TEXT        Set Bytom sender address.  [required]
  -ha, --htlc-address TEXT  Set Bytom Hash Time Lock Contract (HTLC) address.  [required]
  -am, --amount FLOAT       Set Bytom fund amount.  [required]
  -u, --unit TEXT           Set Bytom amount unit.  [default: NEU]
  -as, --asset TEXT         Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT        Set Bytom network.  [default: mainnet]
  -h, --help                Show this message and exit.
```
</details>

> **Example** -> swap bytom `fund` command

**Sender Address** _(str)_ -> bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 **[required]**<br/>
**HTLC Address** _(str)_ -> bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8 **[required]**<br/>
**Amount** _(int, float)_ -> 0.1 **[required]**<br/>
**Unit** _(str)_ -> BTM **[default: `NEU`]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned fund transaction raw.

```shell script
$ swap bytom fund --address bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 --htlc-address bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8 --amount 0.1 --unit BTM --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMmZ1NnZjNyIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDBiNzIwMjkxODUzYjdmYTY4MDAzOTI4NWRjNDRjMWUzM2VlMGQ1YmNhMDYzZWViYWMyMmVmM2M4NTlhZGEzZWNmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMTVmMDE1ZDBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjhiYWFkMGQwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA4NzkyMGQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogIjRlNTk3YmJmOGM1Y2JkNDQ2ZGE3NjU2YzlmMmUwMDUyZDc4NWIyZTkxMmMzOTI2ZGE5MjVhNjM0MGVkY2UwNDMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMTE0NjcwN2ZjYjEwNzFiNzg5YzViMTIzNDc3YzBjNzgyZTMxNTYzNDU1Y2VkZGMxZTUyYzM4NWZlNTBlZmIwYyJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn0sIHsiZGF0YXMiOiBbIjFhMGJmZGU5Y2MyYzhkODkxN2E3YjIxYmI2YmM5ZDhlMDg1ZDM4YTcwMjJmMTA5MGQ2M2QxYjU0M2E2OTg0NzYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfdW5zaWduZWQifQ==
```
</details>

## Claim Command

> $ swap bytom `claim` command

```shell script
$ swap bytom claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom claim [OPTIONS]

Options:
  -a, --address TEXT          Set Bytom recipient address.  [required]
  -ti, --transaction-id TEXT  Set Bytom funded transaction id/hash.  [required]
  -am, --amount FLOAT         Set Bytom withdraw amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Bytom withdraw max amount.  [default: True]
  -u, --unit TEXT             Set Bytom withdraw amount unit.  [default: NEU]
  -as, --asset TEXT           Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Bytom network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bytom `claim` command

**Recipient Address** _(str)_ -> bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p **[required]**<br/>
**Transaction Id** _(str)_ -> 0dbf27e5e0dcfff583e1db18265e367f7e66556979e194213ad859383ea3f6dc **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned claim transaction raw.

```shell script
$ swap bytom claim --address bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p --transaction-id 0dbf27e5e0dcfff583e1db18265e367f7e66556979e194213ad859383ea3f6dc --max-amount True --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxM3lmNXE4IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5MGZlMzBmMzhkM2NlMjIyYmQ2MzVmZmNiMzU4MGU2Yjg0YTA3NjY1MDM3N2JkOGUzYTAwYmZkZWY3MTZhMjYxZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5OGJjODQwNTAwMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkMGIzZTUwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZGU2YTkyMmM5Y2NkYTI1YjZhMzYyNzk1NDkxZTBlY2EyOTcyODllZmUxMTYwNjY2ZmU0YmRjNmE5ZTdjMTA2YyIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJhN2I4M2Y4NTkzNGQ4ODhlNTljMjkyNTA0MWE3MWExOWExNTg4YTcxZTc3ZjEzNzQxOTM0ZTU3YjA3Zjc0M2YwIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0=
```
</details>

## Refund Command

> $ swap bytom `refund` command

```shell script
$ swap bytom refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom refund [OPTIONS]

Options:
  -a, --address TEXT          Set Bytom sender address.  [required]
  -ti, --transaction-id TEXT  Set Bytom funded transaction id/hash.  [required]
  -am, --amount FLOAT         Set Bytom refund amount.  [default: None]
  -ma, --max-amount BOOLEAN   Set Bytom refund max amount.  [default: True]
  -u, --unit TEXT             Set Bytom refund amount unit.  [default: NEU]
  -as, --asset TEXT           Set Bytom asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Bytom network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap bytom `refund` command

**Sender Address** _(str)_ -> bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 **[required]**<br/>
**Transaction Id** _(str)_ -> 0dbf27e5e0dcfff583e1db18265e367f7e66556979e194213ad859383ea3f6dc **[required]**<br/>
**Max Amount** _(bool)_ -> True **[default: `True`]**
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `mainnet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned refund transaction raw.

```shell script
$ swap bytom refund --address bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 --transaction-id 0dbf27e5e0dcfff583e1db18265e367f7e66556979e194213ad859383ea3f6dc --max-amount True --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxM3lmNXE4IiwgImhhc2giOiAiMjcyYTQ4NmFlZWEzYzBhYWM1NjlmNjExNzE1ZTI5ZDQ5NDEzNDYxNGI1MTEzM2NhMDM4NGYxM2EyNmIwYTY2NCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OTBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThiYzg0MDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZDBiM2U1MDQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI4ZjNjZTZjYzBiYWExYTcwMDNiZTUyNmQzODMzMzNjZTM2OTNmYzUyOGNmZTJhYzc1MzYzYmE2YTdjN2E5YTkxIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

## Decode Command

> $ swap bytom `decode` command

```shell script
$ swap bytom decode --help
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

**Transaction Raw** _(str)_ -> eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhz... **[required]**<br/>

> **Returns** _(str)_ -> Bytom transaction json.

```shell script
$ swap bytom decode --transaction-raw eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxM3lmNXE4IiwgImhhc2giOiAiMjcyYTQ4NmFlZWEzYzBhYWM1NjlmNjExNzE1ZTI5ZDQ5NDEzNDYxNGI1MTEzM2NhMDM4NGYxM2EyNmIwYTY2NCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OTBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThiYzg0MDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZDBiM2U1MDQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI4ZjNjZTZjYzBiYWExYTcwMDNiZTUyNmQzODMzMzNjZTM2OTNmYzUyOGNmZTJhYzc1MzYzYmE2YTdjN2E5YTkxIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 509000,
    "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8",
    "type": "bytom_refund_unsigned",
    "tx": {
        "tx_id": "272a486aeea3c0aac569f611715e29d494134614b51133ca0384f13a26b0a664",
        "version": 1,
        "size": 179,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10559000,
                "control_program": "00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc",
                "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8",
                "spent_output_id": "b7e91c227e5d42a38719605e56c991896ef0862398620f22382919090b0fa8a1",
                "input_id": "ec845e583a315a7cab48e17cdb8688483edef7a540c62f848a6e19757ba445c7",
                "witness_arguments": null,
                "sign_data": "8f3ce6cc0baa1a7003be526d383333ce3693fc528cfe2ac75363ba6a7c7a9a91"
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "066872b5644365c2a7fca350a374361fef3c8582333be71a0f9db76e85116b13",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10050000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
            }
        ],
        "fee": 509000
    },
    "unsigned_datas": [
        {
            "datas": [
                "8f3ce6cc0baa1a7003be526d383333ce3693fc528cfe2ac75363ba6a7c7a9a91"
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

> $ swap bytom `sign` command

```shell script
$ swap bytom sign --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: swap bytom sign [OPTIONS]

Options:
  -xk, --xprivate-key TEXT     Set Bytom xprivate key.  [required]
  -tr, --transaction-raw TEXT  Set Bytom unsigned transaction raw.  [required]
  -b, --bytecode TEXT          Set Bytom witness HTLC bytecode.  [default: None]
  -sk, --secret-key TEXT       Set secret key.  [default: None]
  -ac, --account INTEGER       Set Bytom derivation from account.  [default: 1]
  -ch, --change BOOLEAN        Set Bytom derivation from change.  [default: False]
  -ad, --address INTEGER       Set Bytom derivation from address.  [default: 1]
  -p, --path TEXT              Set Bytom derivation from path.  [default: None]
  -i, --indexes LIST           Set Bytom derivation from indexes.  [default: None]
  -h, --help                   Show this message and exit.
```
</details>

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret-key` option.

> **Example** -> swap bytom `sign` command

**XPrivate Key** _(str)_ -> 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXE5bmR5bHg... **[required]**<br/>

> **Returns** _(str)_ -> Bytom signed transaction raw.

```shell script
$ swap bytom sign --xprivate-key 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMmZ1NnZjNyIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDBiNzIwMjkxODUzYjdmYTY4MDAzOTI4NWRjNDRjMWUzM2VlMGQ1YmNhMDYzZWViYWMyMmVmM2M4NTlhZGEzZWNmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMTVmMDE1ZDBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjhiYWFkMGQwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA4NzkyMGQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogIjRlNTk3YmJmOGM1Y2JkNDQ2ZGE3NjU2YzlmMmUwMDUyZDc4NWIyZTkxMmMzOTI2ZGE5MjVhNjM0MGVkY2UwNDMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMTE0NjcwN2ZjYjEwNzFiNzg5YzViMTIzNDc3YzBjNzgyZTMxNTYzNDU1Y2VkZGMxZTUyYzM4NWZlNTBlZmIwYyJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn0sIHsiZGF0YXMiOiBbIjFhMGJmZGU5Y2MyYzhkODkxN2E3YjIxYmI2YmM5ZDhlMDg1ZDM4YTcwMjJmMTA5MGQ2M2QxYjU0M2E2OTg0NzYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfdW5zaWduZWQifQ
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMmZ1NnZjNyIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDBiNzIwMjkxODUzYjdmYTY4MDAzOTI4NWRjNDRjMWUzM2VlMGQ1YmNhMDYzZWViYWMyMmVmM2M4NTlhZGEzZWNmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMTVmMDE1ZDBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjhiYWFkMGQwMjAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA4NzkyMGQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogIjRlNTk3YmJmOGM1Y2JkNDQ2ZGE3NjU2YzlmMmUwMDUyZDc4NWIyZTkxMmMzOTI2ZGE5MjVhNjM0MGVkY2UwNDMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiMTE0NjcwN2ZjYjEwNzFiNzg5YzViMTIzNDc3YzBjNzgyZTMxNTYzNDU1Y2VkZGMxZTUyYzM4NWZlNTBlZmIwYyJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn0sIHsiZGF0YXMiOiBbIjFhMGJmZGU5Y2MyYzhkODkxN2E3YjIxYmI2YmM5ZDhlMDg1ZDM4YTcwMjJmMTA5MGQ2M2QxYjU0M2E2OTg0NzYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbWyI4ODAzYzIzMTQzYWQ0NDlmY2JkMTJiMmIyMWM1ODdlNGM1NzE1MTg0MDlhZWEzOGNkOTBkZTgwMDU4ZmJkNGFiNmE5MzYyZDgzYzFmYjQ2YjBlNTUyYTJmNzc3OTdiY2Q5ODQxYmQxMDcxOTM3OTg2NmQ5MWE3MTdiZjBjODcwYiJdLCBbIjY0MDFkMjU4ZDY1MmExNzczYjQ3OGMyNjRkZjYyNmRkMjk0MDRlN2U0ZmMxYjBmYTgzMTNlMzkwODliMTVhZWU2NGYwZDg5N2Y2NjgzNGU4NmJkYjkyNWJlMDY0ODQ5NDM3NjlmNjdjMDYwODczNTk4NDcyMDY1YjIxMzgxMjA2Il1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ==
```
</details>

## Submit Command

> $ swap bytom `submit` command

```shell script
$ swap bytom submit --help
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
$ swap bytom submit --transaction-raw eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXFmNzhzYXp4czUzOW5tenp0cTdtZDYzZmsyeDhsZXc2ZWQyZ3U1cm50OXVtN2plcnJoMDdxM3lmNXE4IiwgImhhc2giOiAiMjcyYTQ4NmFlZWEzYzBhYWM1NjlmNjExNzE1ZTI5ZDQ5NDEzNDYxNGI1MTEzM2NhMDM4NGYxM2EyNmIwYTY2NCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OTBmZTMwZjM4ZDNjZTIyMmJkNjM1ZmZjYjM1ODBlNmI4NGEwNzY2NTAzNzdiZDhlM2EwMGJmZGVmNzE2YTI2MWRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThiYzg0MDUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZDBiM2U1MDQwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI4ZjNjZTZjYzBiYWExYTcwMDNiZTUyNmQzODMzMzNjZTM2OTNmYzUyOGNmZTJhYzc1MzYzYmE2YTdjN2E5YTkxIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
272a486aeea3c0aac569f611715e29d494134614b51133ca0384f13a26b0a664
```
</details>
