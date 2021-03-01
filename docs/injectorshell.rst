injectorshell
===============

Included in the original `ssh-mitm <http://ssh-mitm.at/>`_ suit this is a detailed documentation
by its creator.

The injectorshell ssh interface allows the operator of the ssh-mitm server to serve out shell access over
the network that correspond to a hijacked ssh session. Within these injected shells one is able to
execute commands on the remote host using the ssh session created by the original client. Contrary to the
mirrorshell there can be multiple injected shells per ssh session. All these shells - including the client itself -
share their environment but are served answers individually.

Using the ``--ssh-injector-enable-mirror`` option injected shells can print the input of the user to their screen.
This differs from the mirrorshell which always displays every keystroke on both terminals. The injectorshell
tries its best to not leak any unwanted output to the users session so that they can operate normally.

By default injector shell access is limited to the local maschine ``localhost`` but can be opened up to any
network using the ``--ssh-injector-net NET/IF`` parameter. Due to the fact that access to the injector shells is
not authenticated doing this should be thoroughly thought through.

For ease of use a private key can be used for a more consistent integrity check. It can be set with the
``--ssh-injector-key ID`` parameter. If this is not done a new one will be generated each time the server is spun up.

.. note::
    It should also be noted that shell environment can be affected by any injector shell and is not accounted for when
    considering stealth. This means environment variables or the working directory for example can be changed by any
    injector shell and will alert the original shells owner of faulty operation.

.. important::
    It is also important to mention that when multiple injector shells are inserting commands into the same hijacked ssh
    session at the same time discrepancies are not accounted for. Keystrokes are collectively merged at the server and the
    responses are served accordingly. This is also true for the clients interactive ssh session. A advanced edition of the
    injectorshell - the :ref:`stealthshell` - fixes both these problems.