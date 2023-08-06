
import importlib

__all__ = ["getdebugger"]


def getdebugger(type, *args, **kwargs):
    """Return debugger instance."""

    supported = {
        "jlink": "jlink.JLINK",
        "pyocd": "pyocd.PYOCD",
        "redlink": "redlink.RedLink",
        'ide': "ide.IDE",
        'blhost': "blhost.Blhost"
    }
    try:
        importlib.import_module("mcutk.debugger.%s" % type)
        return eval(supported[type])(*args, **kwargs)
    except KeyError:
        raise ValueError("not supported debugger: %s" % type)
