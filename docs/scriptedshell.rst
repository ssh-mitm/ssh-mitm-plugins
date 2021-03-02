scriptedshell
===============

When working through a security audit gathering information is one of the most important steps.

The scriptedshell ssh interface is first and foremost an information gathering tool but due to its
functionality it can also be used for different use cases. This plugin will execute a shell script
when a new ssh session is opened by a client. The output of the script will be stored locally on the
ssh-mitm machine under their respective session name.

.. note::
    Stored script output is taken from the server as-is with some ANSI control characters removed.

The ``--ssh-script SCRIPT`` parameter declares the location of the script.

The ``--ssh-out-dir DIR`` parameter indicates where the output of each session script execution should be stored.