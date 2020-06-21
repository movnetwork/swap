#!/usr/bin/env python3

from shuttle.cli.__main__ import main as cli_main


refund_transaction_raw = \
     "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVk" \
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


def test_bytom_cli_submit(cli_tester):

    submit = cli_tester.invoke(
        cli_main, [
            "bytom",
            "submit",
            "--raw", refund_transaction_raw
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: finalize tx fail" + "\n"

    submit = cli_tester.invoke(
        cli_main, [
            "bytom",
            "submit",
            "--raw", "asdfasdfasdfasdfasdfsdfasdf"
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: invalid Bytom signed transaction raw" + "\n"
