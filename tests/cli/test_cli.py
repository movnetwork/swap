#!/usr/bin/env python3
# coding=utf-8

import pytest


@pytest.mark.script_launch_mode('subprocess')
def test_shuttle_cli(script_runner):
    assert script_runner.run("shuttle").success
    version = script_runner.run("shuttle", "--version")
    assert version.success

    assert version.stdout == "PyShuttle version 0.1.3\n"
    assert version.stderr == ""
