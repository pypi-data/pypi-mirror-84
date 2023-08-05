"""Creates the Request and Response sub class that are used by each entry"""
from cached_property import cached_property
from .mixins import HttpTransaction


class Request(HttpTransaction):
    # pylint: disable=invalid-name
    """Request object for an HarEntry"""

    def __str__(self):
        return "HarEntry.Request for %s" % self.raw_entry["url"]

    def __repr__(self):
        return "HarEntry.Request for %s" % self.raw_entry["url"]

    # Root Level values

    @cached_property
    def method(self) -> str:
        """:returns HTTP method"""
        return self.raw_entry["method"]

    @cached_property
    def queryString(self) -> dict:
        """:returns query string"""
        return self.raw_entry["queryString"]

    @cached_property
    def url(self) -> str:
        """:returns URL"""
        return self.raw_entry["url"]

    # Header Values

    @cached_property
    def accept(self):
        """:returns accept header"""
        return self.get_header_value("Accept")

    @cached_property
    def encoding(self):
        """:returns accept-encoding header"""
        return self.get_header_value("Accept-Encoding")

    @cached_property
    def host(self):
        """:returns Host header"""
        return self.get_header_value("Host")

    @cached_property
    def language(self):
        """:returns language-accept header"""
        return self.get_header_value("Accept-Language")

    @cached_property
    def userAgent(self):
        """:returns user agent"""
        return self.get_header_value("User-Agent")


class Response(HttpTransaction):
    # pylint: disable=invalid-name
    """Response object for a HarEntry"""

    # Root Level values

    @cached_property
    def redirectURL(self) -> [str, None]:
        """:returns redirect URL if there is any"""
        if self.raw_entry["redirectURL"]:
            return self.raw_entry["redirectURL"]
        return None

    @cached_property
    def status(self) -> int:
        """:returns HTTP status"""
        return int(self.raw_entry["status"])

    @cached_property
    def statusText(self) -> str:
        """Returns HTTP status text"""
        return self.raw_entry["statusText"]

    # Header Values

    @cached_property
    def contentSecurityPolicy(self) -> str:
        """:returns contentSecurityPolicy header"""
        return self.get_header_value("content-security-policy")

    @cached_property
    def contentSize(self) -> int:
        """:returns content size"""
        return int(self.raw_entry["content"]["size"])

    @cached_property
    def contentType(self) -> str:
        """:returns content type header"""
        return self.get_header_value("content-type")

    @cached_property
    def date(self) -> str:
        """:returns date header"""
        return self.get_header_value("date")

    @cached_property
    def lastModified(self) -> str:
        """:returns last-modifed header"""
        return self.get_header_value("last-modified")

    @cached_property
    def mimeType(self) -> str:
        """:returns content mimeType"""
        return self.raw_entry["content"]["mimeType"]

    @cached_property
    def text(self) -> str:
        """:returns the content text"""
        return self.raw_entry["content"]["text"]
