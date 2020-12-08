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
  -n, --network TEXT        Set Vapor network.  [default: mainnet]
  -h, --help                Show this message and exit.
```
</details>

> **Example** -> swap vapor `fund` command

**Sender Address** _(str)_ -> vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag **[required]**<br/>
**HTLC Address** _(str)_ -> vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned fund transaction raw.

```shell script
$ swap vapor fund --address vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag --htlc-address vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37 --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiNGJjMDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDgwMDQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjg4YjJhMDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICIwM2U1ZDkzZWExZmUzODMzMzk0NjZiMGMyMzc2MzNjNDY2NjBkZmYzOTAwYzI4ZWE3YWQwZDU5NzQwYzZiYWRhIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImZlZmZmZGZhNTQ4NmY1YWJhNzlkNTIwMjY0NTg4YWI2NzNmMGU3Y2MzNjM3YzYwZGZhMmEwYTVkNWY0NGNiYTYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogInZhcG9yX2Z1bmRfdW5zaWduZWQifQ==
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
  -n, --network TEXT          Set Vapor network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `claim` command

**Recipient Address** _(str)_ -> vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h **[required]**<br/>
**Transaction Id** _(str)_ -> 675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned claim transaction raw.

```shell script
$ swap vapor claim --address vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h --transaction-id 675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474 --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXEzcGx3dm12eTRxaGptcDV6ZmZ6bWs1MGFhZ3B1anQ2ZmxuZjYzaCIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDEwMDAxNWUwMTVjZmFiZTY1ZTNlZDFkMGE4NGE4ZTQzZTZkM2RlMWI0NmZkNGM5ZmE0N2YyZjA0NGU5NGU4NGUwZWM5YWU0MGE1ZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkOGQwMjEwMTAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTIyMDEyMDNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UwMjAxM2MwMDNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2QwMDNiZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYwOWMwNjAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiNTAwYzEyMWU5N2ZmMWM0Y2ZjMmUzYWFiMDBkZDYzODQ0YTIzNjYzNWY2YmE2Yjk0MWM5MmQ5MGE1ZjhiZGJiNCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI2NzQ0YzA0NmU2MzgzOWE3MGVjMWQ4ZmE4Zjg5NjM4ZTAyNTE5M2QyYTIxZjI5MTkzNzg5MjQ3NDE1NDVlN2UzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9LCB7ImRhdGFzIjogWyI3ODAwMzk5ODc2MGExZDVjYzJmZGZlYzQ3NTc5MjcwMTY1MGFlN2Y1MGMzOGQ5MTg2N2NkYzg0ZDUzODBlM2Q5Il0sICJwdWJsaWNfa2V5IjogIjNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9jbGFpbV91bnNpZ25lZCJ9
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
  -n, --network TEXT          Set Vapor network.  [default: mainnet]
  -h, --help                  Show this message and exit.
```
</details>

> **Example** -> swap vapor `refund` command

**Sender Address** _(str)_ -> vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag **[required]**<br/>
**Transaction Id** _(str)_ -> 675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474 **[required]**<br/>
**Amount** _(int)_ -> 10000 **[required]**<br/>
**Asset Id** _(str)_ -> ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff **[required]**<br/>
**Network** _(str)_ -> mainnet **[default: `solonet`]**<br/>

> **Returns** _(str)_ -> Vapor unsigned refund transaction raw.

```shell script
$ swap vapor refund --address vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag --transaction-id 675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474 --amount 10000 --asset ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff --network mainnet
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJoYXNoIjogIjc3YWM3NjljZTFhNmJmZDJmMWE4ZjE0YzBlNmJlNjY4ZDE4M2VmYTY0NjEwZjUxMzIyZTdjOWVjNTYwMmNhZmQiLCAicmF3IjogIjA3MDEwMDAyMDE2OTAxNjczMjQ3OWQ4MjE2NWZmZTkyNDYyODk4OWJkNDM4MGMxOTI2MWQyN2E0MWJjNTYwZTFhZmVjMTAzYTZhN2M5NGYxZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMDAxMjIwMDIwNGY4ZjBlODhkMGE0NGIzZDg4NGIwN2I2ZGQ0NTM2NTE4ZmZjYmI1OTZhOTFjYTBlNmIyZjM3ZTk2NDYzYmJmYzAxMDAwMTVmMDE1ZDMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiNGJjMDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2MwMDNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMDAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjk4ODBhMTAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZDdhYTRjYWFmODgyM2ZhMDA1NTYwOTJlZDA1MTE1YzY2NjViNDdiNjkyZDBkNmQwNDFkYmE2NjNkOTVkZGNjZSJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiMTMwMmY4NmFlMzhmYzUyMzQ5NjBhNjA0OTMzMmQwZTczMDllYmExMDlkODhhMGI0ODk3Zjc2NGJlODA4M2Q1MSJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAidmFwb3JfcmVmdW5kX3Vuc2lnbmVkIn0=
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
$ swap vapor decode --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXEzcGx3dm12eTRxaGptcDV6ZmZ6bWs1MGFhZ3B1anQ2ZmxuZjYzaCIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDEwMDAxNWUwMTVjZmFiZTY1ZTNlZDFkMGE4NGE4ZTQzZTZkM2RlMWI0NmZkNGM5ZmE0N2YyZjA0NGU5NGU4NGUwZWM5YWU0MGE1ZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZkOGQwMjEwMTAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTIyMDEyMDNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UwMjAxM2MwMDNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2QwMDNiZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYwOWMwNjAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiNTAwYzEyMWU5N2ZmMWM0Y2ZjMmUzYWFiMDBkZDYzODQ0YTIzNjYzNWY2YmE2Yjk0MWM5MmQ5MGE1ZjhiZGJiNCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI2NzQ0YzA0NmU2MzgzOWE3MGVjMWQ4ZmE4Zjg5NjM4ZTAyNTE5M2QyYTIxZjI5MTkzNzg5MjQ3NDE1NDVlN2UzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9LCB7ImRhdGFzIjogWyI3ODAwMzk5ODc2MGExZDVjYzJmZGZlYzQ3NTc5MjcwMTY1MGFlN2Y1MGMzOGQ5MTg2N2NkYzg0ZDUzODBlM2Q5Il0sICJwdWJsaWNfa2V5IjogIjNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9jbGFpbV91bnNpZ25lZCJ9
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "fee": 449000,
    "address": "vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h",
    "type": "vapor_claim_unsigned",
    "tx": {
        "tx_id": "500c121e97ff1c4cfc2e3aab00dd63844a236635f6ba6b941c92d90a5f8bdbb4",
        "version": 1,
        "size": 372,
        "time_range": 0,
        "inputs": [
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000,
                "control_program": "00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc",
                "address": "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37",
                "spent_output_id": "633f8d82662748eac2a9b390fbcfe3e1ba2ba8605b75bfbc59c5c95ce0ab2d96",
                "input_id": "15f576af7a3650c95663dcd645875d38305ff0733a34a4bcb441da0771a0ec88",
                "witness_arguments": null
            },
            {
                "type": "spend",
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 551000,
                "control_program": "0014887ee66d84a82f2d86824a45bb51fdea03c92f49",
                "address": "vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h",
                "spent_output_id": "2320f0d706bcffdd22719ce5e8eb4bce0a26eae6f5526c401bcb45b897dcae6b",
                "input_id": "2b88a1c0330354a1f7669dc2097eb8e21ce667f8b4c7e925d94a9b872566e191",
                "witness_arguments": [
                    "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e"
                ]
            }
        ],
        "outputs": [
            {
                "type": "control",
                "id": "89312c42d42e6d1a34cc49bfda29afa4f7c350c58443cf3c308c18b2d7e71204",
                "position": 0,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 10000,
                "control_program": "0014887ee66d84a82f2d86824a45bb51fdea03c92f49",
                "address": "vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h"
            },
            {
                "type": "control",
                "id": "e274d46ced83654ddf32e72eda2a237643fe040c720c7089d42dc1686a9a74ca",
                "position": 1,
                "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "asset_definition": {},
                "amount": 102000,
                "control_program": "0014887ee66d84a82f2d86824a45bb51fdea03c92f49",
                "address": "vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h"
            }
        ],
        "fee": 449000
    },
    "unsigned_datas": [
        {
            "datas": [
                "6744c046e63839a70ec1d8fa8f89638e025193d2a21f2919378924741545e7e3"
            ],
            "network": "mainnet",
            "path": null
        },
        {
            "datas": [
                "78003998760a1d5cc2fdfec475792701650ae7f50c38d91867cdc84d5380e3d9"
            ],
            "public_key": "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e",
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

**Note**: Don't forget when you are signing `claim` transaction you have to be use `--secret-key` option.

> **Example** -> swap vapor `sign` command

**XPrivate Key** _(str)_ -> 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b **[required]**<br/>
**Unsigned Transaction Raw** _(str)_ -> eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTlu... **[required]**<br/>

> **Returns** _(str)_ -> Vapor signed transaction raw.

```shell script
$ swap vapor sign --xprivate-key 205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiNGJjMDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDgwMDQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjg4YjJhMDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICIwM2U1ZDkzZWExZmUzODMzMzk0NjZiMGMyMzc2MzNjNDY2NjBkZmYzOTAwYzI4ZWE3YWQwZDU5NzQwYzZiYWRhIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImZlZmZmZGZhNTQ4NmY1YWJhNzlkNTIwMjY0NTg4YWI2NzNmMGU3Y2MzNjM3YzYwZGZhMmEwYTVkNWY0NGNiYTYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogInZhcG9yX2Z1bmRfdW5zaWduZWQifQ
```

<details>
  <summary>Output</summary><br/>

```shell script
eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiNGJjMDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDgwMDQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjg4YjJhMDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICIwM2U1ZDkzZWExZmUzODMzMzk0NjZiMGMyMzc2MzNjNDY2NjBkZmYzOTAwYzI4ZWE3YWQwZDU5NzQwYzZiYWRhIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImZlZmZmZGZhNTQ4NmY1YWJhNzlkNTIwMjY0NTg4YWI2NzNmMGU3Y2MzNjM3YzYwZGZhMmEwYTVkNWY0NGNiYTYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbWyJjNGJhMGRhZGRkZTcxOTRkODQ5MWZhZmMwZGIzNzE5Zjg0ZDU1YzE5NDZhMDI1MjlmNjg5YzJjYTMxYjdhYWYyYWRjYTdkYzUxYjBmZWFkMmYzYjNiNjUzOTBjMjA1MmRlOTAwNWM4N2M5OWY3ZDQ0ZjVlZWVmZTNkOWQ4OWIwOCJdXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogInZhcG9yX2Z1bmRfc2lnbmVkIn0=
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
$ swap vapor submit --transaction-raw eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjopInZwMXE5bmR5bHgwMnN5ZndkN25wZWhmeHo0bGRkaHpxc3ZlMnphMjNhZyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZDMyNDc5ZDgyMTY1ZmZlOTI0NjI4OTg5YmQ0MzgwYzE5MjYxZDI3YTQxYmM1NjBlMWFmZWMxMDNhNmE3Yzk0ZjFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiNGJjMDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxNDgwMDQ2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTIyMDAyMDRmOGYwZTg4ZDBhNDRiM2Q4ODRiMDdiNmRkNDUzNjUxOGZmY2JiNTk2YTkxY2EwZTZiMmYzN2U5NjQ2M2JiZmMwMDAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjg4YjJhMDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICIwM2U1ZDkzZWExZmUzODMzMzk0NjZiMGMyMzc2MzNjNDY2NjBkZmYzOTAwYzI4ZWE3YWQwZDU5NzQwYzZiYWRhIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImZlZmZmZGZhNTQ4NmY1YWJhNzlkNTIwMjY0NTg4YWI2NzNmMGU3Y2MzNjM3YzYwZGZhMmEwYTVkNWY0NGNiYTYiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbWyJjNGJhMGRhZGRkZTcxOTRkODQ5MWZhZmMwZGIzNzE5Zjg0ZDU1YzE5NDZhMDI1MjlmNjg5YzJjYTMxYjdhYWYyYWRjYTdkYzUxYjBmZWFkMmYzYjNiNjUzOTBjMjA1MmRlOTAwNWM4N2M5OWY3ZDQ0ZjVlZWVmZTNkOWQ4OWIwOCJdXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogInZhcG9yX2Z1bmRfc2lnbmVkIn0
```

<details>
  <summary>Output</summary><br/>

```shell script
675392fcbc1867e247add457597611717229e5d2c46a53c44e3e61d6ce351474
```
</details>
