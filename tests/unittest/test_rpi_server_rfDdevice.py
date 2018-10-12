'''Tests for rfDevice.py'''
from unittest import TestCase
from unittest.mock import (
    patch, 
    Mock,
)

import pytest

# Needed so you can run unittests even if you are not on a Raspberry PI
from surrogate import surrogate
with surrogate('RPi.GPIO'):
    from rpi_server.rfDevice import RFDevice


# For patches
GPIO = 'rpi_server.rfDevice.GPIO'
RFDEVICE = 'rpi_server.rfDevice.RFDevice'

# Dummy vars
DUMMY_GPIO = 'dummy_gpio'
DUMMY_PIN = 'dummy_pin'


@pytest.mark.unittest
class TestRfDevice(TestCase):
    '''Unittests for rfDevice module'''

    @patch(GPIO)
    def setUp(self, gpio_mock):
        self.rfdevice = RFDevice(DUMMY_GPIO)

    def reset(self):
        self.setUp()

    @patch(GPIO)
    def test_rfdevice_init(self, gpio_mock):
        '''Test RFDevice.__init__'''
        # Make sure creating instances work without exceptions
        self.assertIsInstance(RFDevice(DUMMY_GPIO), RFDevice)
        gpio_mock.setmode.assert_called_once_with(gpio_mock.BCM)
        self.reset()

    @patch.object(RFDevice, 'disable_rx')
    @patch.object(RFDevice, 'disable_tx')
    @patch(GPIO)
    def test_rfdevice_cleanup_all_pins(self, gpio_mock, disable_tx_mock, disable_rx_mock):
        '''Test RFDevice.cleanup'''
        self.rfdevice.tx_enabled = True
        self.rfdevice.rx_enabled = True
        self.assertIsNone(self.rfdevice.cleanup())
        disable_tx_mock.assert_called_once_with()
        disable_rx_mock.assert_called_once_with()
        gpio_mock.cleanup.assert_called_once_with()
        self.reset()


    @patch(GPIO)
    def test_rfdevice_cleanup_one_pin(self, gpio_mock):
        '''Test RFDevice.cleanup'''
        self.rfdevice.tx_enabled = True
        self.rfdevice.rx_enabled = True
        self.assertIsNone(self.rfdevice.cleanup(DUMMY_PIN))
        gpio_mock.setup.assert_called_once_with(DUMMY_PIN, gpio_mock.IN)
        self.reset()

