#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tktl` package."""
import json
import os

import pytest
from click.testing import CliRunner
from tktl import main


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.cli)
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
    help_result = runner.invoke(main.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output


def test_ci_auth():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.login, ["--api-key", os.environ["TEST_USER_API_KEY"]])
    print(result.output)
    assert result.exit_code == 0
    assert result.output == f"Authentication successful for user: {os.environ['TEST_USER']}\n"

    result = runner.invoke(main.login, ["--api-key", "FAKEAPIKEY"])
    assert result.exit_code == 0
    assert result.output == "Authentication failed: Key format is invalid\n"
    with open(os.path.expanduser("~/.tktl/config.json"), "r") as j:
        d = json.load(j)
    assert d["api-key"] == "FAKEAPIKEY"
