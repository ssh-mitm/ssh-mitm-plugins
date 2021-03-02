# SSH-MITM Plugins

![SSH-MITM example](https://ssh-mitm.at/img/mitm-example.png)



After working on features and functionality of the
[ssh-mitm](http://ssh-mitm.at/)
project it was decided that the features of the ssh-mitm version 0.4.0
should be locked and any further additions to its feature-set should be
made externally.
This was done to keep the ssh-mitm project to its core functionality.
The ssh-mitm plugins are advanced features that should enhance the capabilities of the ssh-mitm server.
Here you will find detailed feature-oriented documentation of the creators
additions to the ssh-mitm project.

## Installation

Installing the ssh-mitm server including these plugins is very simple:

    $ pip install ssh-mitm-plugins
    
The current version of the ssh-mitm server will be installed and additional advanced features
will be available through these plugins. The ssh-mitm server will operate normally as described
by the [ssh-mitm project](#ssh-mitm).

## Plugins

Following advanced features will be made available through the modular runtime compilation of 
the ssh-mitm server.

#### SSH 
* stealthshell - improving on the injectorshell, this ssh interface will
make hijacking of a ssh session undetectable
* scriptedshell - perfect for security audits and information gathering, this ssh interface executes
a script on the remote machine and stores the output on the ssh-mitm server

## SSH-MITM

**For more information about the core functionality of the ssh-mitm server visit:**

* Github        - https://github.com/ssh-mitm/ssh-mitm
* Website       - http://ssh-mitm.at
* Documentation - http://docs.ssh-mitm.at