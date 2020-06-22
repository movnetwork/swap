# CLI - Bytom Commands

<img align="right" height="75" src="https://github.com/meherett/shuttle/blob/master/docs/static/svg/bytom.svg">

  - [HTLC Command](#htlc-command)
  - [Fund Command](#fund-command)
  - [Claim Command](#claim-command)
  - [Refund Command](#refund-command)
  - [Decode Command](#decode-command)
  - [Sign Command](#sign-command)
  - [Submit Command](#submit-command)

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

## HTLC Command

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
  -sq, --sequence INTEGER       Set Bytom sequence/expiration block.
  -n, --network TEXT            Set Bytom network.
  -h, --help                    Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Bytom Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ shuttle bytom htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 --sequence 1000 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0
```
</details>

## Fund Command

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
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**bytecode** _(str)_ -> 02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0 **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned fund transaction raw.

```shell script
$ shuttle bytom fund --sender-guid f0ed6ddd-9d6b-49fd-8866-a52d1083a13b --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --bytecode 02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZhZDZlZjJiNzg2Yjc4MGRhMTEwYTZjYTNjOGJlMGM3YmNkZDQ4OGY4ZDcyYzEwYmMwMWIyZGQzYjk1YTRiNDAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogIjVlYzI1NDdjN2FlY2U0NWFmNmI0Yjk3ZmFiY2M0MmNiNmIxZWNmYTljN2QzMGEwYjNjNDY1NTg4ODI4NGIxYmQiLCAicmF3IjogIjA3MDEwMDAxMDE1ZjAxNWQ3ZjJkN2VjZWMzZjYxZDMwZDBiMjk2ODk3M2EzYWM4NDQ4ZjA1OTllYTIwZGNlODgzYjQ4YzkwM2M0ZDZlODdmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMwZjJmZDE2MDAwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkyMjAxMjA2OTI5N2U5Yjc1ZWM4OGE0Y2E3ZjBjN2ExYmI2MWQ2NGVhOTM5MWIxNGE5MDJjZGE0ODU4MGZlM2UxMmE4MmFiMDIwMTQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBmNzlhMTIwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0=
```
</details>

## Claim Command

> $ shuttle bytom `claim` command

```shell script
$ shuttle bytom claim --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom claim [OPTIONS]

Options:
  -t, --transaction TEXT      Set Bytom fund transaction id.  [required]
  -rg, --recipient-guid TEXT  Set Bytom recipient GUID.  [required]
  -a, --amount INTEGER        Set Bytom amount to claim.  [required]
  -as, --asset TEXT           Set Bytom asset id.  [required]
  -n, --network TEXT          Set Bytom network.
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `claim` command

**Transaction Id** _(str)_ -> 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd **[required]**<br/>
**Recipient GUID** _(str)_ -> 571784a8-0945-4d78-b973-aac4b09d6439 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned claim transaction raw.

```shell script
$ shuttle bytom claim --transaction 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd --recipient-guid 571784a8-0945-4d78-b973-aac4b09d6439 --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjgxY2VjMjM0N2E5MmVmM2M1YjAyZDg2MDUzZjFiMWZhYTY0Mjg0M2UzODFkMWM3NTdiMzliNmI4ZDJkN2FkOTUiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc4YmNlMWYzZDNiNWRkMjdlODdlNGNiYWIwM2NjN2I0ODFjNTNmYzEyZTliYjc4M2Y4ZmM1OWM0NGQyYzhkMjQiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMmNhNDU2NjM5NWIwMWE0ODJiMzc4ZmY4ZWJhNzlhNTk3MGFhZDQ2NWNmYmEyNWZlNzUzOGYxNzhmMTNjZWE0MCIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzY1ZmI2MmFiNDA5NzY2YzAyN2JkZDVlNzllYmM0NjhmMmI2ZWRiMzYyYWQ5MzkwY2IzMTM5YjM1ZDE5YjI2NWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDEwMDAxNjAwMTVlMDJlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMDk4ODhkODAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0=
```
</details>

## Refund Command

> $ shuttle bytom `refund` command

```shell script
$ shuttle bytom refund --help
```

<details>
  <summary>Output</summary><br/>

```shell script
Usage: shuttle bytom refund [OPTIONS]

Options:
  -t, --transaction TEXT   Set Bytom fund transaction id.  [required]
  -sg, --sender-guid TEXT  Set Bytom sender GUID.  [required]
  -a, --amount INTEGER     Set Bytom amount to refund.  [required]
  -as, --asset TEXT        Set Bytom asset id.  [required]
  -n, --network TEXT       Set Bytom network.
  -h, --help               Show this message and exit.
```
</details>

> **Example** -> shuttle bytom `refund` command

**Transaction Id** _(str)_ -> 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd **[required]**<br/>
**Sender GUID** _(str)_ -> f0ed6ddd-9d6b-49fd-8866-a52d1083a13b **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Bytom unsigned refund transaction raw.

```shell script
$ shuttle bytom refund --transaction 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd --sender-guid f0ed6ddd-9d6b-49fd-8866-a52d1083a13b --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjY1MWQ5Nzg3MTIzMzNlMWQ0YjI1YWFmZjM2YTJiZjU2YTJmZTQzN2NjYjJmNGJiMGI1NDFlOGRkNjllODVmOTUiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjk4NTI2NDdlYzdiMGEwNGM5N2I4ZDQ3NDZkMTU1MmE3ZWNiYjJkZmEyYWZiMDM5YWIwM2M2ZmE1MmI2Mjk3ZjAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogImY5NTgxM2U4YmFkNjZhNmY1Yzg0ZTQzMmUxMWU4ZmY0MWJhNTdlMTdmNjVhMGQ1NmE0ZDJlODExMGZmY2E0NjAiLCAicmF3IjogIjA3MDEwMDAyMDE2OTAxNjc2NWZiNjJhYjQwOTc2NmMwMjdiZGQ1ZTc5ZWJjNDY4ZjJiNmVkYjM2MmFkOTM5MGNiMzEzOWIzNWQxOWIyNjVhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTVmMDE1ZDY1ZmI2MmFiNDA5NzY2YzAyN2JkZDVlNzllYmM0NjhmMmI2ZWRiMzYyYWQ5MzkwY2IzMTM5YjM1ZDE5YjI2NWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBmNzlhMTIwMTAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTIyMDEyMDY5Mjk3ZTliNzVlYzg4YTRjYTdmMGM3YTFiYjYxZDY0ZWE5MzkxYjE0YTkwMmNkYTQ4NTgwZmUzZTEyYTgyYWIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiMGNhYjgwZDAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```
</details>

## Decode Command

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
$ shuttle bytom decode --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZhZDZlZjJiNzg2Yjc4MGRhMTEwYTZjYTNjOGJlMGM3YmNkZDQ4OGY4ZDcyYzEwYmMwMWIyZGQzYjk1YTRiNDAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogIjVlYzI1NDdjN2FlY2U0NWFmNmI0Yjk3ZmFiY2M0MmNiNmIxZWNmYTljN2QzMGEwYjNjNDY1NTg4ODI4NGIxYmQiLCAicmF3IjogIjA3MDEwMDAxMDE1ZjAxNWQ3ZjJkN2VjZWMzZjYxZDMwZDBiMjk2ODk3M2EzYWM4NDQ4ZjA1OTllYTIwZGNlODgzYjQ4YzkwM2M0ZDZlODdmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMwZjJmZDE2MDAwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkyMjAxMjA2OTI5N2U5Yjc1ZWM4OGE0Y2E3ZjBjN2ExYmI2MWQ2NGVhOTM5MWIxNGE5MDJjZGE0ODU4MGZlM2UxMmE4MmFiMDIwMTQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBmNzlhMTIwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0=
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 10000000,
    "guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
    "type": "bytom_fund_unsigned",
    "tx": {
        "tx_id": "5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd",
        "version": 1,
        "size": 273,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 48200000,
                "control_program": "00142b5d110a89d193ea8f2f1e553a8920849a58e689",
                "address": "bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl",
                "spent_output_id": "7e86b3f635595de17686c6d8d9d4f0281239d0db6af0bf0eaca763c46c2d455b",
                "input_id": "5c49cf1f42e72aa418cd143628fcd321557fdda52da5249eb13cb2c57eb8d76e",
                "witness_arguments": [
                    "69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab"
                ],
                "sign_data": "6ad6ef2b786b780da110a6ca3c8be0c7bcdd488f8d72c10bc01b2dd3b95a4b40"
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "8a0d861767240a284ebed0320b11b81253727ecdac0c80bc6a88127327c0d8a1",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000,
                "control_program": "00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc",
                "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8"
            },
            {
                "type": "control",
                "id": "9a0565edd82b0460760eaecbc0b3539a5e9a3e89c760f3f6bce4b4726e5a2e56",
                "position": 1,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 38190000,
                "control_program": "00142b5d110a89d193ea8f2f1e553a8920849a58e689",
                "address": "bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl"
            }
        ],
        "fee": 10000000
    },
    "unsigned_datas": [
        {
            "datas": [
                "6ad6ef2b786b780da110a6ca3c8be0c7bcdd488f8d72c10bc01b2dd3b95a4b40"
            ],
            "public_key": "69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab",
            "network": "mainnet",
            "path": "m/44/153/1/1/12"
        }
    ],
    "signatures": [],
    "network": "mainnet"
}
```
</details>

## Sign Command

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
  -b, --bytecode TEXT     Set Bitcoin witness HTLC bytecode.  [required for claim/refund]
  -s, --secret TEXT       Set secret key. [required for claim]
  -ac, --account INTEGER  Set Bytom derivation from account.  [default: 1]
  -c, --change BOOLEAN    Set Bytom derivation from change.  [default: False]
  -ad, --address INTEGER  Set Bytom derivation from address.  [default: 1]
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
$ shuttle bytom sign --xprivate 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZhZDZlZjJiNzg2Yjc4MGRhMTEwYTZjYTNjOGJlMGM3YmNkZDQ4OGY4ZDcyYzEwYmMwMWIyZGQzYjk1YTRiNDAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogIjVlYzI1NDdjN2FlY2U0NWFmNmI0Yjk3ZmFiY2M0MmNiNmIxZWNmYTljN2QzMGEwYjNjNDY1NTg4ODI4NGIxYmQiLCAicmF3IjogIjA3MDEwMDAxMDE1ZjAxNWQ3ZjJkN2VjZWMzZjYxZDMwZDBiMjk2ODk3M2EzYWM4NDQ4ZjA1OTllYTIwZGNlODgzYjQ4YzkwM2M0ZDZlODdmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMwZjJmZDE2MDAwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkyMjAxMjA2OTI5N2U5Yjc1ZWM4OGE0Y2E3ZjBjN2ExYmI2MWQ2NGVhOTM5MWIxNGE5MDJjZGE0ODU4MGZlM2UxMmE4MmFiMDIwMTQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBmNzlhMTIwMTE2MDAxNDJiNWQxMTBhODlkMTkzZWE4ZjJmMWU1NTNhODkyMDg0OWE1OGU2ODkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0=
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAxMDAwMTAxNWYwMTVkN2YyZDdlY2VjM2Y2MWQzMGQwYjI5Njg5NzNhM2FjODQ0OGYwNTk5ZWEyMGRjZTg4M2I0OGM5MDNjNGQ2ZTg3ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjMGYyZmQxNjAwMDExNjAwMTQyYjVkMTEwYTg5ZDE5M2VhOGYyZjFlNTUzYTg5MjA4NDlhNThlNjg5MjIwMTIwNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmIwZjc5YTEyMDExNjAwMTQyYjVkMTEwYTg5ZDE5M2VhOGYyZjFlNTUzYTg5MjA4NDlhNThlNjg5MDAiLCAiaGFzaCI6ICI1ZWMyNTQ3YzdhZWNlNDVhZjZiNGI5N2ZhYmNjNDJjYjZiMWVjZmE5YzdkMzBhMGIzYzQ2NTU4ODgyODRiMWJkIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZhZDZlZjJiNzg2Yjc4MGRhMTEwYTZjYTNjOGJlMGM3YmNkZDQ4OGY4ZDcyYzEwYmMwMWIyZGQzYjk1YTRiNDAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAic2lnbmF0dXJlcyI6IFtbIjk5NWE4MGMwZTk1MDUxNDg5YzFmOGQwYmQxMWM4YWI4ZDMzZjRjMTIxNDQ1NzY0NDQ0NGUxN2VhYjkxMzA1MDY0YWE2OGY5NjIzMTlkNDQ3NDIwODI1YjI3OWYzODBmZGVlMDUyNTkwYTg5N2MxYzY4MzcxZDVjNWYwZGIwNjBkIl1dLCAidHlwZSI6ICJieXRvbV9mdW5kX3NpZ25lZCJ9
```
</details>

## Submit Command

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
$ shuttle bytom submit --raw eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAxMDAwMTAxNWYwMTVkN2YyZDdlY2VjM2Y2MWQzMGQwYjI5Njg5NzNhM2FjODQ0OGYwNTk5ZWEyMGRjZTg4M2I0OGM5MDNjNGQ2ZTg3ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjMGYyZmQxNjAwMDExNjAwMTQyYjVkMTEwYTg5ZDE5M2VhOGYyZjFlNTUzYTg5MjA4NDlhNThlNjg5MjIwMTIwNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmIwZjc5YTEyMDExNjAwMTQyYjVkMTEwYTg5ZDE5M2VhOGYyZjFlNTUzYTg5MjA4NDlhNThlNjg5MDAiLCAiaGFzaCI6ICI1ZWMyNTQ3YzdhZWNlNDVhZjZiNGI5N2ZhYmNjNDJjYjZiMWVjZmE5YzdkMzBhMGIzYzQ2NTU4ODgyODRiMWJkIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZhZDZlZjJiNzg2Yjc4MGRhMTEwYTZjYTNjOGJlMGM3YmNkZDQ4OGY4ZDcyYzEwYmMwMWIyZGQzYjk1YTRiNDAiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAic2lnbmF0dXJlcyI6IFtbIjk5NWE4MGMwZTk1MDUxNDg5YzFmOGQwYmQxMWM4YWI4ZDMzZjRjMTIxNDQ1NzY0NDQ0NGUxN2VhYjkxMzA1MDY0YWE2OGY5NjIzMTlkNDQ3NDIwODI1YjI3OWYzODBmZGVlMDUyNTkwYTg5N2MxYzY4MzcxZDVjNWYwZGIwNjBkIl1dLCAidHlwZSI6ICJieXRvbV9mdW5kX3NpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```shell script
5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd
```
</details>
