import unittest
from unittest import mock

from test.mock_popen import MockPopenConnect, MockPopenFail, MockPopenDisconnect, MockPopenNoInstanceRunning
from utils.snx import SnxHooks


class TestSnxHooks(unittest.TestCase):
    no_snx = b"no snx process running."
    disconnect_ok = b"done."
    connect_ok = b"SNX - connected."

    def test_connect_ok(self):
        with mock.patch("subprocess.Popen", MockPopenConnect):
            snx = SnxHooks()
            result = snx.connect("passwd")
            self.assertTrue(result)

    def test_connect_no(self):
        with mock.patch("subprocess.Popen", MockPopenFail):
            snx = SnxHooks()
            result = snx.connect("password")
            self.assertFalse(result)

    def test_disconnect_ok(self):
        with mock.patch("subprocess.Popen", MockPopenDisconnect):
            snx = SnxHooks()
            result = snx.disconnect()
            self.assertTrue(result)

    def test_disconnect_ok_not_running(self):
        with mock.patch("subprocess.Popen", MockPopenNoInstanceRunning):
            snx = SnxHooks()
            result = snx.disconnect()
            self.assertTrue(result)

    def test_disconnect_no(self):
        with mock.patch("subprocess.Popen", MockPopenFail):
            snx = SnxHooks()
            result = snx.disconnect()
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
