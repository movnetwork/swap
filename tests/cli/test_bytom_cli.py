#!/usr/bin/env python3
# coding=utf-8

from shuttle.cli.__main__ import main as cli_main

XPRIVATE_KEY = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830d" \
               "e09518e6bd5958d5d5dd97624cfa4b"

HTLC_BYTECODE = "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182" \
                "d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e" \
                "45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"

FUND_RAW = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIj" \
           "ogW3siZGF0YXMiOiBbImIxYzVlYTFkNjAwNjY0Y2U4MTAwNzMxNmQ2Zjg5NThlMjQ4ZWZhNjk3YWRhN2Q0M2E4YzI2YjJkNjE1NjAx" \
           "NDgiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYj" \
           "Y0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyIyNTFm" \
           "YmQ4YTAzMmM3MmJmMjkwN2VjNGFmYzk1ZGYxZTE2Mzg5NDZiODE5MGQwYjIxZTk1MjA2YmU2YzZhOTYyIl0sICJwdWJsaWNfa2V5Ij" \
           "ogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29y" \
           "ayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogImM2YjMyYjk1ODEwYTEwMDIzZDA3ODk2OD" \
           "czNTI3NGQwMWU4YjVmZjhjNTU3NjNkODM3OGZhZjZhZjI5YTY2NjYiLCAicmF3IjogIjA3MDEwMDAyMDE2MTAxNWY4MWU1MGUxMmY4" \
           "MjM2ZjkxYzg4NDJkM2Y0OTU1MDJiOTc1MmZjMzVkMDE1MDA5MWVhNWIyYzI2NjA1MTVjM2I1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0Ym" \
           "JiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZmE4Y2JkYmMzZjQwMjAxMDExNjAwMTQyY2RhNGY5OWVhODEx" \
           "MmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OW" \
           "FkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5" \
           "ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1" \
           "MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDMwMWFjMDFmMzdkZWE2MmVmZD" \
           "I5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmNjQwMTg4MDEwMTY0MjA5MWZmN2Y1MjVm" \
           "ZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNz" \
           "U0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAzYTI2ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0" \
           "YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMD" \
           "AwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3" \
           "MzAzZmZkNzdjMWI0ODJiODRiZGZjNGNhZGJjM2Y0MDIwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwOD" \
           "MzMmEwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBi" \
           "MGI0ZjgwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgInNpZ25hdHVyZXMiOiBbXS" \
           "wgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfdW5zaWduZWQifQ"

FUND_SIGNED = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICI" \
              "wNzAxMDAwMjAxNjEwMTVmODFlNTBlMTJmODIzNmY5MWM4ODQyZDNmNDk1NTAyYjk3NTJmYzM1ZDAxNTAwOTFlYTViMmMyNjYwNT" \
              "E1YzNiNWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGZhOGNiZ" \
              "GJjM2Y0MDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZm" \
              "NDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMTYwMDE1ZTNmYmYyNGI0MGM5YTc" \
              "4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
              "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExM" \
              "mU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1" \
              "OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAzMDFhYzAxZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTc" \
              "zMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDE4ODAxMDE2NDIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYW" \
              "Q1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjIwYWMxM2MwYmIxNDQ1NDIzYTY0MTc1NDE4MmQ1M2YwNjc3Y2Q0MzUxYTBlNzQzZTZmM" \
              "TBiMzUxMjJjM2Q3ZWEwMTIwM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0" \
              "NTgyMGVlYjc0MWY1NDdhNjQxNjAwMDAwMDU1N2FhODg4NTM3YTdjYWU3Y2FjNjMxZjAwMDAwMDUzN2FjZDlmNjk3MmFlN2NhYzA" \
              "wYzAwMDAxM2VmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmYz" \
              "RjYWRiYzNmNDAyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAwMTNkZmZmZmZmZmZmZ" \
              "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJj" \
              "ZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogImM2YjMyYjk1ODEwYTEwMDIzZDA3ODk" \
              "2ODczNTI3NGQwMWU4YjVmZjhjNTU3NjNkODM3OGZhZjZhZjI5YTY2NjYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiYjFjNW" \
              "VhMWQ2MDA2NjRjZTgxMDA3MzE2ZDZmODk1OGUyNDhlZmE2OTdhZGE3ZDQzYThjMjZiMmQ2MTU2MDE0OCJdLCAicHVibGljX2tle" \
              "SI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5l" \
              "dHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn0sIHsiZGF0YXMiOiBbIjI1MWZiZDhhMDMyYzcyYmY" \
              "yOTA3ZWM0YWZjOTVkZjFlMTYzODk0NmI4MTkwZDBiMjFlOTUyMDZiZTZjNmE5NjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNT" \
              "I1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1ha" \
              "W5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW1si" \
              "ZGZkYTRhN2E3Mzk1MDhlYWZiNjc4NDZhYWEyOGJlOTcwMTdjNTY0MmQ1ZDNjNWNlMzY4NjA1ZTExZTBmY2ExZTM1OWQ0ZWRmMmM" \
              "xMTJhNTI4NjIyZDRmYzc1OTQxMTFjNWFkOTIxY2VlNjczNzhjNjJhNmMwZGIyZGQzNzkyMDEiXSwgWyI4Y2ZlNWRmYTM5ZmIyM2" \
              "VlNmMxNWViNWNjYjgwMDlmMzI5NDhjMmMxNTliMTZiNWNhYjhiN2IxNzk5MzZhZTU5MDAxNzNmOTZmZjc2YjdmYjBiNDU4Y2RiN" \
              "zAyMzBhYmFkYjhmNjlkNmY2ZWU4NDIyMjM5ZWNiOTA0OWNlYTMwZiJdXSwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ=="

CLAIM_RAW = \
      "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3s" \
      "iZGF0YXMiOiBbIjg0MGYwZjM5MTFiOTllY2NlODk0MjA0OWFhYjY4NjEzMmE5MTAzNTBiZTAxNDY0MTU1YzkzM2ZjMWE5Y2NmZjQiXSwgIm" \
      "5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjg2ZGFiNjAwZWFjMDMxYjM4YjE2YmQ1NGQzMjMwYjgyN" \
      "WUwYjI2YmNkZGZkZGJhNTdjODBhZDNmNjI4YTllYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0" \
      "NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzA" \
      "vMSJ9XSwgImhhc2giOiAiZTg5OWVjNzlhN2IxYTk0MzFjYjczNWMxYmMxYmNhYzg1MDJjZjZkYmY3NTA0ODdjMzcxYjQ0NDFkNTUyNmVjNi" \
      "IsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4N" \
      "DQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0" \
      "MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjB" \
      "hYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2Zj" \
      "YzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN" \
      "2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQy" \
      "OGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
      "mZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMj" \
      "IwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlY" \
      "TYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MTFiYzE5MGY0ZWJl" \
      "M2E2ZGRjYmM3YWVmNjk3M2FjNGE4OTNiNDQ1NjAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
      "mZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLC" \
      "Aic2VjcmV0IjogIkhlbGxvIE1laGVyZXQhIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5d" \
      "G9tX2NsYWltX3Vuc2lnbmVkIn0="

CLAIM_SIGNED = \
         "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAx" \
         "MDAwMjAxZDAwMTAxY2QwMTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAz" \
         "NjVmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmNjQwMDAxODgwMTAx" \
         "NjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJi" \
         "MTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5ZjU1NDZmNjNhMjUz" \
         "ZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2Fl" \
         "N2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDEwMDAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4" \
         "YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
         "ZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMz" \
         "MmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDIwMTM5" \
         "ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDExNjAwMTQxMWJj" \
         "MTkwZjRlYmUzYTZkZGNiYzdhZWY2OTczYWM0YTg5M2I0NDU2MDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
         "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZk" \
         "YzQwODMzMmEwMCIsICJoYXNoIjogImU4OTllYzc5YTdiMWE5NDMxY2I3MzVjMWJjMWJjYWM4NTAyY2Y2ZGJmNzUwNDg3YzM3MWI0NDQx" \
         "ZDU1MjZlYzYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiODQwZjBmMzkxMWI5OWVjY2U4OTQyMDQ5YWFiNjg2MTMyYTkxMDM1MGJl" \
         "MDE0NjQxNTVjOTMzZmMxYTljY2ZmNCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiODZk" \
         "YWI2MDBlYWMwMzFiMzhiMTZiZDU0ZDMyMzBiODI1ZTBiMjZiY2RkZmRkYmE1N2M4MGFkM2Y2MjhhOWVhMiJdLCAicHVibGljX2tleSI6" \
         "ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsi" \
         "OiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInNpZ25hdHVyZXMiOiBb" \
         "WyI0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxIiwgIjdjNjA5OWY1MTIzYWIwZThjZTgzYWZmNDVmZTgxMWVmNmI0OTBjNjg3YWU3" \
         "ZWQ0NTc5ZDQ3NDhjMzk2ZjM5MGNjMDE4Mzk5NjRmYTU2MmFhMzg0M2IwMDBhYzIzOTcxZjEzNWJiMDczMDBiMDI2YjQ1OTdjNWMyNGNj" \
         "ZGJiNDA5IiwgIiJdLCBbIjRiYTFiZDA5NjYyMmJiNjdjMmU3MGI0ZDlmZDhhOWU5MmNiMjk5YjM4MDRlZTQzNzNhMzU3Y2FhMjNkNWMz" \
         "NDQ5MzJjNjM4ZmU4OGM4MDA3NDEzNTMyYWRjMjgyZWVkYzQyNjg2NjZiMDg3ODk2ZWExYWFjNTFlNWNhODQyODA3Il1dLCAidHlwZSI6" \
         "ICJieXRvbV9jbGFpbV9zaWduZWQifQ=="

REFUND_RAW = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVk" \
             "IjogW3siZGF0YXMiOiBbIjQ5NGVlNzc2OTBhYzJhYjUxZTZkZTRkYWMyZWJhMmQzNTc3MTc0MzEyZWQwYTIyMjQ5NGE5OTVlMjhm" \
             "ZmY4NDYiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImVjYWJhNDAxYTZkZjljZmZi" \
             "ZWQzN2QxYWJjZjIzYjkxYjNjODRlYzdhYTk0MTFkNDgxY2JlZjJlNDM3ZWY3YjEiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1" \
             "ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5u" \
             "ZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMDY5YWU0NDg2MDQ3ZWQzMTQzMjkxYWFjNzVkM2FmNDhk" \
             "MTI4MzZkMGI1ODEyNzg3MTc3ZGM0MGJiOTY1YzkwZiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3" \
             "OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJi" \
             "NTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRm" \
             "NDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUz" \
             "ZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3" \
             "Mjg4YTdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAw" \
             "NTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0" \
             "MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
             "ZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIw" \
             "MTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYz" \
             "N2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MmNk" \
             "YTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
             "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2" \
             "MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21f" \
             "cmVmdW5kX3Vuc2lnbmVkIn0="

REFUND_SIGNED = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6I" \
                "CIwNzAxMDAwMjAxZDAwMTAxY2QwMTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0ND" \
                "A5NjI0MWEyYzAzNjVmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg" \
                "0YmRmNjQwMDAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFk" \
                "MWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN" \
                "2VhMDEyMDJiOWE1OTQ5ZjU1NDZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3ND" \
                "FmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDEwMDA" \
                "xNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZm" \
                "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4M" \
                "DEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0Yz" \
                "RmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDIwMTM5ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg" \
                "0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2" \
                "MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                "mZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwOD" \
                "MzMmEwMCIsICJoYXNoIjogIjA2OWFlNDQ4NjA0N2VkMzE0MzI5MWFhYzc1ZDNhZjQ4ZDEyODM2ZDBiNTgxMjc4NzE3N2RjNDB" \
                "iYjk2NWM5MGYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiNDk0ZWU3NzY5MGFjMmFiNTFlNmRlNGRhYzJlYmEyZDM1Nzcx" \
                "NzQzMTJlZDBhMjIyNDk0YTk5NWUyOGZmZjg0NiJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkY" \
                "XRhcyI6IFsiZWNhYmE0MDFhNmRmOWNmZmJlZDM3ZDFhYmNmMjNiOTFiM2M4NGVjN2FhOTQxMWQ0ODFjYmVmMmU0MzdlZjdiMS" \
                "JdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDF" \
                "iNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAibmV0d29yayI6" \
                "ICJtYWlubmV0IiwgInNpZ25hdHVyZXMiOiBbWyI2NWI0ZmNkOWU2ZDU4ZTJhYjlkZGFkYzZmMzMwYzUxOWQzZmNlY2ZlM2QzM" \
                "GE0ZTQ4NDE5OTIwYzlkYmE5ZGM4OGJlNTAzZDdjOWE4MjVkMDliZWNkNjgzODBiNmM0ZTNhZGIwNTQ1ZDg1MWI5NjgxMjhjMD" \
                "hkZGIwMWNkZTcwZCIsICIwMSJdLCBbIjViZDkwNmQ2ODI5YjE2NzljMWI2ZTk4Nzg0OWU1Zjg0MzJhMWRkNzExNGIwMjY5MDh" \
                "mNjc1ZGFmYjlhOTUyNmUyNWE3YTIzZjQ1MWUwODY5NWMxMzNlNjdhODk5MDc5Y2Y3NTQxMGNjMDU1YjkzNzE1OGZjNDczZTgx" \
                "NTQxMzBhIl1dLCAidHlwZSI6ICJieXRvbV9yZWZ1bmRfc2lnbmVkIn0="


def test_bytom_cli(cli_tester):
    assert cli_tester.invoke(cli_main,
                             ["bytom"]).exit_code == 0

    # Testing bytom htlc command.
    htlc = cli_tester.invoke(cli_main,
                             "bytom htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e4"
                             "5820eeb --recipient-public ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b3512"
                             "2c3d7ea01 --sender-public 91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6"
                             "448f22e2 --sequence 100 --network testnet".split(" "))
    assert htlc.exit_code == 0
    assert htlc.output != HTLC_BYTECODE + "\n"

    # Testing bitcoin fund command.
    fund = cli_tester.invoke(cli_main,
                             ["bytom", "fund", "--sender-guid", "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "--amount",
                              10000, "--asset", "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf",
                              "--bytecode", HTLC_BYTECODE, "--network", "mainnet"])
    assert fund.exit_code == 0
    assert fund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiw" \
                          "gInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjViZTliNWIxYjE4YzdhMjMxMjFhMGQ0MzEyZDcyZWIyN2ZhY2M1Ym" \
                          "NiY2VlMGNmZmVlNDU5ZWVlNGRmYmFmNDAiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3Z" \
                          "jBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQi" \
                          "LCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyI4MTgxZTFhYzViMDA2NjA1MDQ5ZDZhZDg" \
                          "zNjg4Y2EyYTU4N2I0NTc0ZDVmZTQxYjY2ZmU3NDQ3MjczMGQ4OGM4Il0sICJwdWJsaWNfa2V5IjogIjkxZmY3Zj" \
                          "UyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d" \
                          "29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogImI5OTgxMDI1ZGYw" \
                          "OGM4ZmQ2ZTI5NzY2NTZjMjkyZjIyMTlmMTA4Y2U1ZjA4ZmZlODVkMzNlMjhmMjM4NTlmYTIiLCAicmF3IjogIjA" \
                          "3MDEwMDAyMDE2MTAxNWY4MWU1MGUxMmY4MjM2ZjkxYzg4NDJkM2Y0OTU1MDJiOTc1MmZjMzVkMDE1MDA5MWVhNW" \
                          "IyYzI2NjA1MTVjM2I1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N" \
                          "2MxYjQ4MmI4NGJkZmE4Y2JkYmMzZjQwMjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2" \
                          "ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU" \
                          "4YWQxYjY0NDhmMjJlMjAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwND" \
                          "k1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                          "mZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYx" \
                          "NTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWR" \
                          "lZjk1NThhZDFiNjQ0OGYyMmUyMDMwMWFkMDFmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNW" \
                          "ZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmOTA0ZTAxODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY" \
                          "2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQx" \
                          "ODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDNhMjZkYTgyZWFkMTVhODA1MzNhMDI" \
                          "2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWI3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYT" \
                          "g4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDAwMTNlZjM3ZGVhNjJlZmQyO" \
                          "TY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjk4ZmRkYWMzZjQwMjAx" \
                          "MTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzZGZmZmZmZmZmZmZmZmZ" \
                          "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNj" \
                          "AwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdL" \
                          "CAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9" + "\n"

    # Testing bitcoin claim command.
    claim = cli_tester.invoke(cli_main,
                              ["bytom", "claim", "--transaction", "8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d0"
                                                                  "57ea4e587f7db0cbe",
                               "--recipient-guid", "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "--recipient-public",
                               "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01", "--amount", 100,
                               "--asset", "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf",
                               "--network", "mainnet"])
    assert claim.exit_code == 0
    assert claim.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIi" \
                           "wgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjg0MGYwZjM5MTFiOTllY2NlODk0MjA0OWFhYjY4NjEzMmE5MTAz" \
                           "NTBiZTAxNDY0MTU1YzkzM2ZjMWE5Y2NmZjQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH" \
                           "0sIHsiZGF0YXMiOiBbIjg2ZGFiNjAwZWFjMDMxYjM4YjE2YmQ1NGQzMjMwYjgyNWUwYjI2YmNkZGZkZGJhNTdj" \
                           "ODBhZDNmNjI4YTllYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0Nm" \
                           "UzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6" \
                           "ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiZTg5OWVjNzlhN2IxYTk0MzFjYjczNWMxYmMxYmNhYzg1MD" \
                           "JjZjZkYmY3NTA0ODdjMzcxYjQ0NDFkNTUyNmVjNiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJm" \
                           "MjRiNDBjOWE3OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZG" \
                           "VhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAw" \
                           "MTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZD" \
                           "FiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIz" \
                           "NTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2" \
                           "Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3" \
                           "YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZW" \
                           "M1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMm" \
                           "U2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUz" \
                           "YmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YT" \
                           "BiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MTFiYzE5MGY0ZWJlM2E2ZGRj" \
                           "YmM3YWVmNjk3M2FjNGE4OTNiNDQ1NjAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2" \
                           "MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2VjcmV0IjogbnVsbCwgIm5ldHdvcmsiOiAibWFpbm5ldCIsIC" \
                           "JzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0=" + "\n"

    # Testing bitcoin refund command.
    refund = cli_tester.invoke(cli_main,
                               ["bytom", "refund", "--transaction", "8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d0"
                                                                    "57ea4e587f7db0cbe",
                                "--sender-guid", "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
                                "--sender-public", "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01",
                                "--amount", 100, "--asset",
                                "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "--network",
                                "mainnet"])

    assert refund.exit_code == 0
    assert refund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiI" \
                            "iwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjg0MGYwZjM5MTFiOTllY2NlODk0MjA0OWFhYjY4NjEzMmE5MT" \
                            "AzNTBiZTAxNDY0MTU1YzkzM2ZjMWE5Y2NmZjQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnV" \
                            "sbH0sIHsiZGF0YXMiOiBbIjg2ZGFiNjAwZWFjMDMxYjM4YjE2YmQ1NGQzMjMwYjgyNWUwYjI2YmNkZGZkZGJh" \
                            "NTdjODBhZDNmNjI4YTllYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0M" \
                            "mU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicG" \
                            "F0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiZTg5OWVjNzlhN2IxYTk0MzFjYjczNWMxYmMxYmN" \
                            "hYzg1MDJjZjZkYmY3NTA0ODdjMzcxYjQ0NDFkNTUyNmVjNiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNk" \
                            "MDEzZmJmMjRiNDBjOWE3OGI1Zjc2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwM" \
                            "zY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NG" \
                            "JkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWR" \
                            "lZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3" \
                            "NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4Y" \
                            "TdlMjRlZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2Mz" \
                            "FmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU" \
                            "1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                            "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY" \
                            "2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0Zj" \
                            "Q3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk" \
                            "2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MTFi" \
                            "YzE5MGY0ZWJlM2E2ZGRjYmM3YWVmNjk3M2FjNGE4OTNiNDQ1NjAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                            "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2" \
                            "RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dXJlcyI6IFtdLCAibmV" \
                            "0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fcmVmdW5kX3Vuc2lnbmVkIn0=" + "\n"

    # Testing bytom decode command.
    decode = cli_tester.invoke(cli_main,
                               ["bytom", "decode", "--raw", FUND_RAW])
    assert decode.exit_code == 0
    assert decode.output != "\n"

    decode = cli_tester.invoke(cli_main,
                               ["bytom", "decode", "--raw", "asdfjhasdjkhfjasdhfkjahsdkljfhk"])
    assert decode.exit_code == 0
    assert decode.output

    decode = cli_tester.invoke(cli_main,
                               ["bytom", "decode", "--raw", "eyJtZWhlcmV0dA=="])
    assert decode.exit_code == 0
    assert decode.output

    decode = cli_tester.invoke(cli_main,
                               ["bytom", "decode", "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ=="])
    assert decode.exit_code == 0
    assert decode.output

    # Testing bitcoin sign command.
    fund_sign = cli_tester.invoke(cli_main,
                                  ["bytom", "sign", "--raw", FUND_RAW, "--xprivate", XPRIVATE_KEY])
    assert fund_sign.exit_code == 0
    assert fund_sign.output == FUND_SIGNED + "\n"

    # Testing bitcoin sign command.
    claim_sign = cli_tester.invoke(cli_main,
                                   ["bytom", "sign", "--raw", CLAIM_RAW, "--xprivate", XPRIVATE_KEY])
    assert claim_sign.exit_code == 0
    assert claim_sign.output == CLAIM_SIGNED + "\n"

    # Testing bitcoin sign command.
    refund_sign = cli_tester.invoke(cli_main,
                                    ["bytom", "sign", "--raw", REFUND_RAW, "--xprivate", XPRIVATE_KEY])
    assert refund_sign.exit_code == 0
    assert refund_sign.output == REFUND_SIGNED + "\n"

    # Testing bytom submit command.
    submit = cli_tester.invoke(cli_main,
                               ["bytom", "submit", "--raw", REFUND_RAW])
    assert submit.exit_code == 0
    assert submit.output == "Error: finalize tx fail" + "\n"

    submit = cli_tester.invoke(cli_main,
                               ["bytom", "submit", "--raw", "asdfgjasdgjkfgaskdjfsadg"])
    assert submit.exit_code == 0
    assert submit.output
