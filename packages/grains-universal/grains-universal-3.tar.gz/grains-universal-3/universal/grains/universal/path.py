import os
import sys


def load_os_vars(hub):
    hub.grains.GRAINS.pardir = os.pardir
    hub.grains.GRAINS.sep = os.sep
    hub.grains.GRAINS.altsep = os.altsep
    hub.grains.GRAINS.extsep = os.extsep
    hub.grains.GRAINS.pathsep = os.pathsep
    hub.grains.GRAINS.pathsep = os.pathsep
    hub.grains.GRAINS.linesep = os.linesep
    hub.grains.GRAINS.devnull = os.devnull
    hub.grains.GRAINS.supports_unicode_filenames = os.path.supports_unicode_filenames


def load_cwd(hub):
    """
    Current working directory
    """
    hub.grains.GRAINS.cwd = os.getcwd()


def load_path(hub):
    """
    Return the path
    """
    # Provides:
    #   path
    hub.grains.GRAINS.path = os.environ.get("PATH", "")


def load_pythonpath(hub):
    """
    Return the Python path
    """
    # Provides:
    #   pythonpath
    hub.grains.GRAINS.pythonpath = sorted((str(p) for p in sys.path), key=str.casefold)


def load_executable(hub):
    """
    Return the python executable in use
    """
    # Provides:
    #   pythonexecutable
    hub.grains.GRAINS.pythonexecutable = sys.executable
