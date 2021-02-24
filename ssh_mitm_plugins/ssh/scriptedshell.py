import logging
import os

from ssh_proxy_server.forwarders.ssh import SSHForwarder


class SSHScriptedForwarder(SSHForwarder):

    @classmethod
    def parser_arguments(cls):
        cls.parser().add_argument(
            '--ssh-script',
            dest='ssh_script',
            help='script to execute on ssh connection',
            required=True
        )
        cls.parser().add_argument(
            '--ssh-out-dir',
            dest='ssh_out_dir',
            help='script output directory',
            default='.'
        )

    def __init__(self, session):
        super(SSHScriptedForwarder, self).__init__(session)
        self.executing = False
        self.script = open(os.path.expanduser(self.args.ssh_script), "r")
        self.output = open(os.path.expanduser(os.path.join(self.args.ssh_out_dir, str(self.session))), "w+")

    def forward_stdin(self):
        if self.executing:
            line = self.script.readline()
            logging.debug(line)
            if line == "" and not self.server_channel.recv_ready():
                logging.debug("Script: Shutting down")
                self.executing = False
                self.script.close()
                self.output.close()
                super(SSHScriptedForwarder, self).forward_stdin()
            elif line != "":
                self.server_channel.sendall(line)
            return
        if not self.executing and not self.script.closed and self.server_channel.recv_ready():
            logging.debug("Script: Starting")
            self.executing = True
        super(SSHScriptedForwarder, self).forward_stdin()

    def stdout(self, text):
        if self.executing:
            self.output.write(text.decode('utf-8'))
            return ""
        return text

    def close_session(self, channel):
        super().close_session(channel)