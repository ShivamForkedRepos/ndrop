
import os
import cmd

from .about import version
from .netdrop import NetDropServer, NetDropClient


class NetDropShell(cmd.Cmd):
    intro = f'Welcome to NDrop shell v{version}. Type help or ? to list commands.'
    prompt = '(ndrop)$ '
    _mode = None
    _server = None

    def close(self):
        'Close server'
        for transport in self._server._transport:
            transport.request_finish()
            transport.quit_request()
        self._server = None

    def precmd(self, line):
        line = line.lower()
        return line

    def preloop(self):
        pass

    def do_quit(self, arg):
        'Close ndrop shell and exit.'
        print('Thank you for using NDrop')
        self.close()
        return True

    def do_mode(self, arg):
        'Set client mode: "dukto" or "nitroshare"'
        if arg and arg in ['dukto', 'nitroshare']:
            self._mode = arg
        print(f'Mode: {self._mode}')

    def do_nodes(self, arg):
        'List online nodes.'
        for node in self._server.get_nodes():
            print(node)

    def do_send_text(self, arg):
        'Send TEXT. "<ip> <TEXT>"'
        ip, message = arg.split(' ')
        mode = self._mode or 'dukto'
        client = NetDropClient(ip, mode=mode)
        client.send_text('hello')

    def do_send_file(self, arg):
        'Send FILE. "<ip> <file name>"'
        ip, fname = arg.split(' ')
        if not os.path.exists(fname):
            print(f'Could not find file "{fname}"')
            return
        mode = self._mode or 'dukto'
        client = NetDropClient(ip, mode=mode)
        client.send_file(fname)

    def do_ls(self, arg):
        'List files in local directory.'
        with os.scandir() as it:
            for entry in sorted(it, key=lambda x: (x.is_file(), x.name)):
                name = entry.name + '/' if entry.is_dir() else entry.name
                print(name)

    def do_pwd(self, arg):
        'Echo local current directory.'
        print(os.getcwd())

    def do_cd(self, arg):
        'change local directory.'
        if arg and os.path.exists(arg):
            os.chdir(arg)
            self._server.saved_to(arg)
