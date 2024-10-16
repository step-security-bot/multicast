# tests/test_hear_socket_errors.py
import unittest
from unittest.mock import patch
from multicast.hear import McastHEAR

class TestHearSocketErrors(unittest.TestCase):
	@patch('multicast.skt.McastSocket')
	def test_socket_operation_error(self, mock_socket):
		mock_socket_instance = mock_socket.return_value
		mock_socket_instance.recvfrom.side_effect = OSError("Mocked receive error")
		hear_instance = McastHEAR()
		result = hear_instance.doStep(group='224.0.0.1', port=59259)
		self.assertFalse(result[0])