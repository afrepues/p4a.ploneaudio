from p4a.audio import interfaces
from p4a.ploneaudio import content
from p4a.common import site

from Products.CMFCore import utils as cmfutils 

def setup_portal(portal):
    site.ensure_site(portal)
    setup_site(portal)

    qi = cmfutils.getToolByName(portal, 'portal_quickinstaller')
    qi.installProducts(['CMFonFive'])

def setup_site(site):
    """Install all necessary components and configuration into the
    given site.

      >>> from p4a.audio import interfaces
      >>> from p4a.common.testing import MockSite

      >>> site = MockSite()
      >>> site.queryUtility(interfaces.IAudioSupport) is None
      True

      >>> setup_site(site)
      >>> site.getUtility(interfaces.IAudioSupport)
      <AudioSupport ...>

    """
    
    sm = site.getSiteManager()
    if not sm.queryUtility(interfaces.IAudioSupport):
        sm.registerUtility(interfaces.IAudioSupport,
                           content.AudioSupport('audio_support'))

def _cleanup_utilities(site):
    raise NotImplementedError('Current ISiteManager support does not '
                              'include ability to clean up')
