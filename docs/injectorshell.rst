Injectorshell
===============



.. note::
    It should also be noted that shell environment can be affected by any injector shell and is not accounted for when
    considering stealth. This means environment variables or the working directory for example can be changed by any
    injector shell and will alert the original shells owner of faulty operation.

.. important::
    It is also important to mention that when multiple injector shells are inserting commands into the same hijacked ssh
    session at the same time discrepancies are not accounted for. Keystrokes are collectively merged at the server and the
    responses are served accordingly. This is also true for the clients interactive ssh session. A advanced edition of the
    injectorshell fixes both these problems.