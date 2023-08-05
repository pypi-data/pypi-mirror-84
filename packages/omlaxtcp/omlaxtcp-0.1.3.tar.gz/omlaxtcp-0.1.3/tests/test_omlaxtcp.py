#!/usr/bin/env python

"""Tests for `omlaxtcp` package."""


import unittest
from click.testing import CliRunner

from omlaxtcp import *
from omlaxtcp import cli

class TestOmlaxtcp(unittest.TestCase):
    """Tests for `omlaxtcp` package."""

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
        assert 'omlaxtcp.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
    
    """
    All the tests below require PIR motion sensor to be connected
    
    def test_motionSensor_setup(self):
        result = motionSensor.setup(1)
        assert result == None
    
    def test_motion_detect(self):
        result = motionSensor.motion_detect(1)
        assert result == None
        
    def test_direc_detect(self):
        result = motionSensor.direc_detect(0, 1)
        assert result == None
        
    def test_speed(self):
        result = motionSensor.speed(5, 5)
        assert result == None
    """
    """
    All tests below require both a server and client to communicate between one another
    
    def test_client(self):
        result = TCP.client("test")
        assert result == None
    
    def test_server_setup(self):
        result = TCP.server_setup(1)
        assert result == None
        
    def test_setHostIP(self):
        TCP.setHostIP("10.0.0.16")
        assert TCP.hostIP == "10.0.0.16"
        
    def test_setPort(self):
        TCP.setPort(12345)
        assert TCP.port == 12345
    """
