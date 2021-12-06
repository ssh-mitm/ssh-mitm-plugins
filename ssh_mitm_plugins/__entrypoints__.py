entry_points = {
    'SSHBaseForwarder': [
        'plugin-scriptedshell = ssh_mitm_plugins.ssh.scriptedshell:SSHScriptedForwarder',
        'plugin-stealthshell = ssh_mitm_plugins.ssh.stealthshell:SSHStealthForwarder',
        'plugin-injectorshell = ssh_mitm_plugins.ssh.injectorshell:SSHInjectableForwarder',
        'plugin-puttydos = ssh_mitm_plugins.ssh.putty_dos:SSHPuttyDoSForwarder'
    ],
    'LocalPortForwardingBaseForwarder': [
        'plugin-inject = ssh_mitm_plugins.tunnel.injectclienttunnel:InjectableClientTunnelForwarder'
    ],
}
