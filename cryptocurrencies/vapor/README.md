# CLI - Vapor Commands

<img align="right" height="70" src="https://github.com/meherett/swap/blob/vapor/docs/static/svg/vapor.svg">

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
  decode  Select Vapor transaction raw decoder.
  fund    Select Vapor Fund transaction builder.
  htlc    Select Vapor Hash Time Lock Contract (HTLC) builder.
  refund  Select Vapor Refund transaction builder.
  sign    Select Vapor transaction raw signer.
  submit  Select Vapor transaction raw submitter.
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
  -h, --help                        Show this message and exit.
```
</details>

> **Example** -> swap vapor `htlc` command

**Secret Hash** _(str)_ -> 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb **[required]**<br/>
**Recipient Public Key** _(str)_ -> 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e **[required]**<br/>
**Sender Public Key** _(str)_ -> 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 **[required]**<br/>
**Sequence** _(int)_ -> 1000 **[default: `1000`]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor Hash Time Lock Contract (HTLC) bytecode.

```shell script
$ swap vapor htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb --recipient-public-key 3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e --sender-public-key 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 --sequence 1000 --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0
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
  -am, --amount INTEGER     Set Vapor amount (NEU).  [required]
  -as, --asset TEXT         Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT        Set Bitcoin network.  [default: mainnet]
  -h, --help                Show this message and exit.
```
</details>

> **Example** -> swap vapor `fund` command

**Sender Address** _(str)_ -> bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 **[required]**<br/>
**HTLC Address** _(str)_ -> bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned fund transaction raw.

```shell script
$ swap vapor fund --address bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 --htlc-address bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8 --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0=
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
  -am, --amount INTEGER       Set Vapor amount (NEU).  [required]
  -as, --asset TEXT           Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `claim` command

**Recipient Address** _(str)_ -> bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p **[required]**<br/>
**Transaction Id** _(str)_ -> 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned claim transaction raw.

```shell script
$ swap vapor claim --address bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p --transaction-id 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTNwbHd2bXZ5NHFoam1wNXpmZnptazUwYWFncHVqdDZmNWplODVwIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWQwMTViMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBkZWUxMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogImQ1NDRhZDJkMDhmOWRkYTMzYjc4OTUzYzc0ZWVkZTljOWViNWQ4MDgzNTY5NTMxMGIyNDJkNTc5NmNmYjkxZDYiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNTE3MjI5MGE5ODU4YTRhMDdjNjAzYzc0MWY2ZmQ4ZTg2NzE1YThhNDQ3MGViMjM3ZDBhMmQ4MzI1YzE3MDZiNyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZTQxYWI5NjQ3MDFmMjBhMjM0NzMzNDBiMTFkNWNiY2ZiYTlhMzczY2VkZjI4NGY4MDljMGM2MWNlN2Q3MTVkYSJdLCAicHVibGljX2tleSI6ICIzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fY2xhaW1fdW5zaWduZWQifQ==
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
  -am, --amount INTEGER       Set Vapor amount (NEU).  [required]
  -as, --asset TEXT           Set Vapor asset id.  [default: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
  -n, --network TEXT          Set Bitcoin network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `refund` command

**Sender Address** _(str)_ -> bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 **[required]**<br/>
**Transaction Id** _(str)_ -> 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned refund transaction raw.

```shell script
$ swap vapor refund --address bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7 --transaction-id 5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgImhhc2giOiAiNjlhNWYzMDI4ODBhNzNkMzYzZWNiMzkyYzgyZGNkMzMyODNiZDFiYmU1NmFhMzAyODU4NzMzZTc5ZTE2Mzc5OCIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDMwNWEyOGQ4ZDM0YjQwYzY1OTM2ODEwZjllOWMxZjhiYzljNzkzZWMyZTcyYzcwZjkyMDNmYmJlYjBhNTZkYjlmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTAxMTYwMDE0MGU0M2E5MmE5ZThhY2E3ODhlYjE1NTFjMzE2NDQ4YzJlM2Y3ODIxNTAxMDAwMTVmMDE1ZDgyZTY1Zjk2NGQzYzM1MzI1NDhkZmRlOTM4NDYyZjU2NmM5NWQzYzkwZTZhM2ExODJhMGIzYmRhZTQ2YWE3OTBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODA4NmYyMDMwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk2ZDMwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjY0ODJiMmRmZTliM2U3NjY0MzVlMDQ4MmI2MDAzN2FmYWVhYmFhYWExMDg5Mzc0OGEyODhiY2EwMjlmZjFjNTIiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjBhNDY3NmE3MzI0MmNkMTI2NjFkYjBmM2Y3Mzc5NGQ0OWI3Nzc1NTBiZDk4MTc2YThkODhlYTg3NTVlNDE3ZjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
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

**Transaction Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZ... **[required]**<br/>

> **Returns** _(str)_ -> Vapor transaction json.

```shell script
$ swap vapor decode --transaction-raw eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgImhhc2giOiAiNjlhNWYzMDI4ODBhNzNkMzYzZWNiMzkyYzgyZGNkMzMyODNiZDFiYmU1NmFhMzAyODU4NzMzZTc5ZTE2Mzc5OCIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDMwNWEyOGQ4ZDM0YjQwYzY1OTM2ODEwZjllOWMxZjhiYzljNzkzZWMyZTcyYzcwZjkyMDNmYmJlYjBhNTZkYjlmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTAxMTYwMDE0MGU0M2E5MmE5ZThhY2E3ODhlYjE1NTFjMzE2NDQ4YzJlM2Y3ODIxNTAxMDAwMTVmMDE1ZDgyZTY1Zjk2NGQzYzM1MzI1NDhkZmRlOTM4NDYyZjU2NmM5NWQzYzkwZTZhM2ExODJhMGIzYmRhZTQ2YWE3OTBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODA4NmYyMDMwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk2ZDMwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjY0ODJiMmRmZTliM2U3NjY0MzVlMDQ4MmI2MDAzN2FmYWVhYmFhYWExMDg5Mzc0OGEyODhiY2EwMjlmZjFjNTIiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjBhNDY3NmE3MzI0MmNkMTI2NjFkYjBmM2Y3Mzc5NGQ0OWI3Nzc1NTBiZDk4MTc2YThkODhlYTg3NTVlNDE3ZjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 10000000,
    "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
    "type": "vapor_refund_unsigned",
    "tx": {
        "tx_id": "69a5f302880a73d363ecb392c82dcd33283bd1bbe56aa302858733e79e163798",
        "version": 1,
        "size": 360,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000000,
                "control_program": "00140e43a92a9e8aca788eb1551c316448c2e3f78215",
                "address": "bm1qpep6j2573t983r4325wrzezgct3l0qs4q04pem",
                "spent_output_id": "84287fb5b2b461dbd3b937a9013d89c0d54a21768e31fb8345b02d57a7992533",
                "input_id": "e63cd066b4fa58db7d8e3d93e77b40cbabff485d282d578bf31817c760ddd4f6",
                "witness_arguments": null,
                "sign_data": "6482b2dfe9b3e766435e0482b60037afaeabaaaa10893748a288bca029ff1c52"
            },
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 8160000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7",
                "spent_output_id": "88289fa4c7633574931be7ce4102aeb24def0de20e38e7d69a5ddd6efc116b95",
                "input_id": "49e97e1685d5b08b82713e6acb6747bd176177141cb5618aeecca418c3afd03a",
                "witness_arguments": [
                    "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
                ],
                "sign_data": "0a4676a73242cd12661db0f3f73794d49b777550bd98176a8d88ea8755e417f2"
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "37142f84fb8eb218b5585560ecbccb39b5c3de472de3ec611c74fb54d5773dcf",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
            },
            {
                "type": "control",
                "id": "4a82420ac0738a3e9932bf7aa30cd2cfbb1c1ee0236a12255559ebc34112da92",
                "position": 1,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 18140000,
                "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
            }
        ],
        "fee": 10000
    },
    "unsigned_datas": [
        {
            "datas": [
                "6482b2dfe9b3e766435e0482b60037afaeabaaaa10893748a288bca029ff1c52"
            ],
            "network": "mainnet",
            "path": null
        },
        {
            "datas": [
                "0a4676a73242cd12661db0f3f73794d49b777550bd98176a8d88ea8755e417f2"
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

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret` option.

> **Example** -> swap vapor `sign` command

**XPrivate Key** _(str)_ -> 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTlu... **[required]**<br/>

> **Returns** _(str)_ -> Vapor signed transaction raw.

```shell script
$ swap vapor sign --xprivate-key 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --transaction-raw eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMDBjMDA1YmMxMTRlYzVmODliNDllNDg1MjZmOTAzMTJiNmYxYTUyNzRlZmQyNTIwNDk4ODAwMjNhZWI4ZTc5OThjMTVlMGJhYTRmZjEwZmFiYmRhZTcwMmYyNDU0MDVhMzYwMjJlM2M5YWNjNWU1ZTZjOWFjNGI5ZDkzN2E4MDEiXSwgWyJmYmZiMTIzZWYwNjJjOTA2OGRhZDIyY2UyOGRlMmE0ZTcyZjgyMDc2YjZmOThjYjdlMDkwOWMxMTg1NjI2MGU3MDIwYWVjYmRjYTYzOWYwYjZlMzlkMzQ1YzA1OTEzZDJjOTI5MWRiMTMwYjUzZDViMmJjNTlmNjFhZGZjMTQwNiJdXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfc2lnbmVkIn0=
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

**Signed Transaction Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTl... **[required]**<br/>

> **Returns** _(str)_ -> Vapor blockchain transaction id.

```shell script
$ swap vapor submit --transaction-raw eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMDBjMDA1YmMxMTRlYzVmODliNDllNDg1MjZmOTAzMTJiNmYxYTUyNzRlZmQyNTIwNDk4ODAwMjNhZWI4ZTc5OThjMTVlMGJhYTRmZjEwZmFiYmRhZTcwMmYyNDU0MDVhMzYwMjJlM2M5YWNjNWU1ZTZjOWFjNGI5ZDkzN2E4MDEiXSwgWyJmYmZiMTIzZWYwNjJjOTA2OGRhZDIyY2UyOGRlMmE0ZTcyZjgyMDc2YjZmOThjYjdlMDkwOWMxMTg1NjI2MGU3MDIwYWVjYmRjYTYzOWYwYjZlMzlkMzQ1YzA1OTEzZDJjOTI5MWRiMTMwYjUzZDViMmJjNTlmNjFhZGZjMTQwldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd
```
</details>
