import aiofiles

import os
import pathlib
import re
import sys

from pip._internal.operations import freeze as pip


async def load_python_version(hub):
    hub.grains.GRAINS.pythonversion = list(sys.version_info)


async def load_pip_versions(hub):
    """
    Get the versions of required pip packages
    """
    root_dir = pathlib.Path(
        os.path.join(os.path.dirname(__file__))
    ).parent.parent.parent
    requirements = os.path.join(root_dir, "requirements.txt")
    reqs = {}

    if os.path.isfile(requirements):
        async with aiofiles.open(requirements, "r") as _fh:
            async for line in _fh:
                split = re.split("[ <>=]", line.strip())
                name = split[0].lower()
                version = split[-1].lower()
                if name == version:
                    version = None
                reqs[name] = version
    else:
        for line in pip.freeze():
            if line.startswith("Requires:"):
                reqs = {x.strip(", "): "unknown" for x in line.split()[1:]}
                break
        else:
            reqs = {
                "grainsv2": "unknown",
                "idem": "unknown",
                "pop": "unknown",
                "pop-config": "unknown",
                "rend": "unknown",
            }
    try:
        modules = {}
        for x in pip.freeze():
            if "==" in x:
                name, version = x.split("==")
            elif "#egg=" in x:
                version, name = x.split("#egg=")
            else:
                name = x
                version = None

            # pip is agnostic about case so we will prefer lower
            name = name.lower()
            if name in reqs or name.startswith("idem") or name.startswith("pop"):
                modules[name] = version

        hub.grains.GRAINS.requirement_versions = modules
    except OSError as e:  # pylint: disable=broad-exception
        hub.log.error(f"Error running pip command: {e}")
        hub.grains.GRAINS.requirement_versions = reqs
