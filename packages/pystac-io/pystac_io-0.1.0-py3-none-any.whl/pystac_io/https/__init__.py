from urllib.parse import urlparse
import requests
from pystac import STAC_IO

from .. import add, IoReadWrite


def https_read_text_method(uri):
    parsed = urlparse(uri)
    if parsed.scheme.startswith("http"):
        return requests.get(uri).text
    else:
        return STAC_IO.default_read_text_method(uri)


add("https", IoReadWrite(https_read_text_method, None))
