entry_points = {
    'SSHBaseForwarder': [
        'scriptedshell = ssh_mitm_plugins.ssh.scriptedshell:SSHScriptedForwarder',
        'stealthshell = ssh_mitm_plugins.ssh.stealthshell:SSHStealthForwarder',
        'injectorshell = ssh_mitm_plugins.ssh.injectorshell:SSHInjectableForwarder',
        'puttydos = ssh_mitm_plugins.ssh.putty_dos:SSHPuttyDoSForwarder'
    ],
    'SCPBaseForwarder': [

    ],
    'BaseSFTPServerInterface': [

    ],
    'SFTPHandlerBasePlugin': [

    ]
}
