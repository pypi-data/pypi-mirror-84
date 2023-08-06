****************
GRAINS_UNIVERSAL
****************
**Grains, execution modules, and state modules common to all systems**

INSTALLATION
============

Install with pip::

    pip install grains-universal

DEVELOPMENT INSTALLATION
========================


Clone the `grains-universal` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/grains-universal.git grains_universal
    pip install -e grains_universal

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r grains-universal/requirements-test.txt
    pytest grains-universal/tests

VERTICAL APP-MERGING
====================
Instructions for extending grains-universal into an OS or distro specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem-{specific_platform}
    cd idem-{specific_platform}


Use `pop-seed` to generate the structure of a project that extends `grains` and `idem`::

    pop-seed -t v idem-{specific_platform} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "grains-universal" to the requirements.txt::

    echo grains-universal >> requirements.txt

And that's it!  Go to town making grains, execution modules, and state modules specific to your specific platform.
Follow the conventions you see in grains-universal.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
