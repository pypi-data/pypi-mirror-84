import unittest
from unittest import mock

#from test.mock_popen import MockPopenConnect, MockPopenFail, MockPopenDisconnect, MockPopenNoInstanceRunning
from test.mock_popen import MockPopenConnect, MockPopenFail, MockPopenDisconnect, MockPopenNoInstanceRunning
from utils.snx import SnxExecutable


class TestSnxExecutable(unittest.TestCase):
    no_snx = b"no snx process running."
    disconnect_ok = b"done."
    connect_ok = b"SNX - connected."

    def test_connect_ok(self):
        with mock.patch("subprocess.Popen", MockPopenConnect):
            snx = SnxExecutable()
            result = snx.connect("passwd")
            self.assertTrue(result)

    def test_connect_no(self):
        with mock.patch("subprocess.Popen", MockPopenFail):
            snx = SnxExecutable()
            result = snx.connect("password")
            self.assertFalse(result)

    def test_disconnect_ok(self):
        with mock.patch("subprocess.Popen", MockPopenDisconnect):
            snx = SnxExecutable()
            result = snx.disconnect()
            self.assertTrue(result)

    def test_disconnect_ok_not_running(self):
        with mock.patch("subprocess.Popen", MockPopenNoInstanceRunning):
            snx = SnxExecutable()
            result = snx.disconnect()
            self.assertTrue(result)

    def test_disconnect_no(self):
        with mock.patch("subprocess.Popen", MockPopenFail):
            snx = SnxExecutable()
            result = snx.disconnect()
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
