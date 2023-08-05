"""Mixin Objects that allow for shared methods"""
from cached_property import cached_property
from six.moves.collections_abc import MutableMapping


def iteritems(dic: dict):
    """
    Shared function that returns and iter of dic items
    :param dic: Dict to iterate
    :return: Iterator of dict items
    """
    return iter(dic.items())


class GetHeaders:
    # pylint: disable=invalid-name,too-few-public-methods
    """Mixin to get a header"""

    def get_header_value(self, name: str) -> str:
        """
        Returns the header value of the header defined in ``name``

        :param name: ``str`` name of the header to get the value of
        """
        for x in self.raw_entry["headers"]:
            if x["name"].lower() == name.lower():
                return x["value"]


class MimicDict(MutableMapping):
    # pylint: disable=invalid-name
    """Mixin for functions to mimic a dictionary for backward compatibility"""

    def __getitem__(self, item):
        return self.raw_entry[item]

    def __len__(self):
        return len(self.raw_entry)

    def __delitem__(self, key):
        del self.raw_entry[key]

    def __iter__(self):
        return iter(self.raw_entry)

    def __setitem__(self, key, value):
        self.raw_entry[key] = value


class HttpTransaction(GetHeaders, MimicDict):
    """Class that is used to make a Request or Response object as a dict with headers"""

    # pylint: disable=invalid-name
    def __init__(self, entry):
        super().__init__()
        self.raw_entry = entry

    # Base class gets properties that belong to both request/response
    @cached_property
    def headers(self) -> list:
        """Returns a list of headers"""
        return self.raw_entry["headers"]

    @cached_property
    def bodySize(self) -> int:
        """:returns request bodySize"""
        return int(self.raw_entry["bodySize"])

    @cached_property
    def cookies(self) -> dict:
        """:returns list of cookies"""
        return self.raw_entry["cookies"]

    @cached_property
    def headersSize(self):
        """:returns request headerSize"""
        return int(self.raw_entry["headersSize"])

    @cached_property
    def httpVersion(self) -> str:
        """:returns HTTP version """
        return self.raw_entry["httpVersion"]

    @cached_property
    def cacheControl(self):
        """:returns cache-control"""
        return self.get_header_value("Cache-Control")
