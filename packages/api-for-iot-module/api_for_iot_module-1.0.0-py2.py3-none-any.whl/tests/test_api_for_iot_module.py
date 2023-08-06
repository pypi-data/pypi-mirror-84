#!/usr/bin/env python

"""Tests for `api_for_iot_module` package."""


import unittest
from click.testing import CliRunner

from api_for_iot_module import api_for_iot_module
from api_for_iot_module import cli


class TestApi_for_iot_module(unittest.TestCase):
    """Tests for `api_for_iot_module` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'api_for_iot_module.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
