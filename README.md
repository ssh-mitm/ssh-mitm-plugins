# SSH-MITM Plugins

SSH-MITM plugins are extensions for SSH-MITM 0.6.3.

**Note:** This plugins are not compatible with SSH-MITM >= 1.0.0!

With version 0.4.0 the [ssh-mitm projects](http://ssh-mitm.at/) locks the features
shipping with the core functionality of the program. It is now preferred that any additions to the
feature-set is made through the modular capabilities that the ssh-mitm project is built upon. Using
entrypoints in combination with modules anyone can make their own ssh-mitm plugins.

This projects adds some advanced features to the ssh-mitm server that furthers its capabilities
to realise security audits.

## Installation

Installing the ssh-mitm server including these plugins is very simple:

    $ pip install ssh-mitm-plugins

The ssh-mitm 0.6.3 will be installed and additional advanced features
will be available through these plugins. The ssh-mitm server will operate normally as described
by the [ssh-mitm project](#ssh-mitm).

## Plugins

Following advanced features will be made available through the modular runtime compilation of
the ssh-mitm server.

#### SSH
* injectorshell - a way to hijack a ssh session and execute commands on an separated shell
* stealthshell - improving on the *injectorshell*, this ssh interface will
make hijacking of a ssh session undetectable
* scriptedshell - perfect for security audits and information gathering, this ssh interface executes
a script on the remote machine and stores the output on the ssh-mitm server

For a more detailed look at the plugins usage and operation refer to the
[documentation](http://ssh-mitm-plugins.readthedocs.io).

## SSH-MITM

**For more information about the core functionality of the ssh-mitm server visit:**

* Github        - https://github.com/ssh-mitm/ssh-mitm
* Website       - http://www.ssh-mitm.at
* Documentation - http://docs.ssh-mitm.at
