"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEeaApiObjectprovidesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
