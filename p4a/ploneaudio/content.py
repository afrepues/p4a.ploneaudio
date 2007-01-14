from zope import interface
from p4a.audio import interfaces
from OFS.SimpleItem import SimpleItem

class AudioSupport(SimpleItem):
    """
    """

    interface.implements(interfaces.IAudioSupport)

    @property
    def support_enabled(self):
        return True
