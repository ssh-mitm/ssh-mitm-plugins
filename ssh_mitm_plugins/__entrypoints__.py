entry_points = {
    'SSHBaseForwarder': [
        'scriptedshell = ssh_mitm_plugins.ssh.scriptedshell:SSHScriptedForwarder',
        'stealthshell = ssh_mitm_plugins.ssh.stealthshell:SSHInjectableForwarder'
    ],
    'SCPBaseForwarder': [

    ],
    'BaseSFTPServerInterface': [

    ],
    'SFTPHandlerBasePlugin': [

    ]
}
