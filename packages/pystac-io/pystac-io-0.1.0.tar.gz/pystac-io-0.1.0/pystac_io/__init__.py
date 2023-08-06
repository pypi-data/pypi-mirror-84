from collections import namedtuple
from contextlib import AbstractContextManager
from typing import Dict, List

from pystac import STAC_IO

"""Container for PSTAC_IO read write methods

read: pystac.STAC_IO.read_text_method or None
write: pystac.STAC_IO.write_text_method or None

"""
IoReadWrite = namedtuple("IoReadWrite", ["read", "write"])


""" Private dict of registered IO modules """
PYSTAC_IO: Dict[str, IoReadWrite] = {}


def add(module_name, io_read_write):
    """Add a new pystac_io module

    This method should be called by any module that implements new read and write IO methods
    during init so that they're added to the list of avaiable IO modules.

    See pystac_io.https for an example.

    """
    if module_name in PYSTAC_IO:
        raise ValueError("pystac_io.{} already loaded!".format(module_name))
    PYSTAC_IO.update({module_name: io_read_write})


def loaded_modules() -> List[str]:
    """ Return a list of available pystac_io modules that can be enabled with register() """
    return PYSTAC_IO.keys()


class PyStacIoContextManager(AbstractContextManager):
    """ Manages loading and unloading of custom IO methods for pystac.STAC_IO """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        unregister()
        return None

    def __call__(self, module_name):
        """Register module_name and return a context manager object

        Perform register here rather than in __enter__ so that we register for both
        context manager and regular function invocations

        """
        if module_name in PYSTAC_IO.keys():
            io = PYSTAC_IO[module_name]
            if io.read is not None:
                STAC_IO.read_text_method = io.read
            if io.write is not None:
                STAC_IO.write_text_method = io.write
        else:
            err_str = "pystac_io.register(module_name) must be one of {}".format(
                PYSTAC_IO.keys()
            )
            raise ValueError(err_str)
        return self


""" Replace pystac.STAC_IO handlers with handlers provided by pystac_io.{module_name} """
register = PyStacIoContextManager()


def unregister():
    """ Reset any registered pystac_io handlers to the default pystac.STAC_IO handlers """
    STAC_IO.read_text_method = STAC_IO.default_read_text_method
    STAC_IO.write_text_method = STAC_IO.default_write_text_method
