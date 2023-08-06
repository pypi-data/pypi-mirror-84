import subprocess

from . import config
from subprocess import PIPE
import logging
import psutil


class Snx:

    def __init__(self):
        self.no_snx = b"no snx process running."
        self.disconnect_ok = b"done."
        self.connect_ok = b"SNX - connected."

    def check_if_snx_is_running(self, name):
        for proc in psutil.process_iter():
            try:
                if name.lower() == proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def is_connect_successfully(self, out):
        if self.connect_ok in out:
            return True
        else:
            logging.error(out)
            return False

    def is_disconnect_successfully(self, out):
        if self.no_snx in out or self.disconnect_ok in out:
            return True
        return False

    def is_running(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass


class SnxExecutable(Snx):

    def __init__(self, executable='snx'):
        Snx.__init__(self)
        self.executable = executable
        print(self)


    def connect(self, passwd):
        passwd += "\n"
        command = [self.executable, '-s', config.server, '-c', config.cert]
        if config.elevate:
            command.insert(0, config.elevate)
        snx = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, _ = snx.communicate(input=bytes(passwd, "utf-8"))
        return self.is_connect_successfully(out)

    def disconnect(self):
        command = [self.executable, '-d']
        if config.elevate:
            command.insert(0, config.elevate)
        snx = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, _ = snx.communicate()
        return self.is_disconnect_successfully(out)

    def is_running(self):
        return self.check_if_snx_is_running(self.executable)


class SnxHooks(Snx):

    def __init__(self):
        Snx.__init__(self)
        pass

    def connect(self, passwd):
        passwd += "\n"
        snx = subprocess.Popen(['pkexec', '/etc/snxtray/up'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, _ = snx.communicate(input=bytes(passwd, "utf-8"))
        if self.is_connect_successfully(out):
            self.post_up_hook()
            return True
        return False

    def disconnect(self):
        command = ['pkexec', '/etc/snxtray/down']
        snx = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, _ = snx.communicate()
        if self.is_disconnect_successfully(out):
            self.post_down_hook()
            return True
        return False

    def is_running(self):
        return self.check_if_snx_is_running('snx')

    def post_up_hook(self):
        self._userspace_hook(config.USER_POST_UP)

    def post_down_hook(self):
        self._userspace_hook(config.USER_POST_DOWN)

    def _userspace_hook(self, commands):
        if commands:
            for command in commands:
                p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                p.communicate(timeout=60)
