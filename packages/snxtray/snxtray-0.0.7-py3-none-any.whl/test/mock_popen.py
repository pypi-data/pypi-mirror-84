class MockPopen():

    def __init__(self, command, stdin=None, stdout=None, stderr=None, return_val=None, input=None):
        self.timeout = None
        self.expected_input = None
        self.command = command
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.return_val = return_val

    def set_return_val(self, return_val):
        self.return_val = return_val

    def set_expected_input(self, input):
        self.expected_input = input

    def check_input(self):
        if self.expected_input == self.got_input:
            return True
        return False

    def communicate(self, timeout=None, input=None):
        self.timeout = timeout

        self.got_input = input

        return self.return_val, None


class MockPopenFail():

    def __init__(self, command, stdin=None, stdout=None, stderr=None, return_val=None, input=None):
        pass

    def communicate(self, timeout=None, input=None):
        return b"mock byte string  fail mock.", None


class MockPopenNoInstanceRunning():

    def __init__(self, command, stdin=None, stdout=None, stderr=None, return_val=None, input=None):
        pass

    def communicate(self, timeout=None, input=None):
        return b"no snx process running.", None


class MockPopenDisconnect():

    def __init__(self, command, stdin=None, stdout=None, stderr=None, return_val=None, input=None):
        pass

    def communicate(self, timeout=None, input=None):
        return b"mock byte string done.", None


class MockPopenConnect():

    def __init__(self, command, stdin=None, stdout=None, stderr=None, return_val=None, input=None):
        pass

    def communicate(self, timeout=None, input=None):
        return b"mock byte string SNX - connected.", None
