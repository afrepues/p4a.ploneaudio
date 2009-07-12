from p4a.audio import interfaces
from p4a.ploneaudio import content
from p4a.common import site
from p4a.z2utils import indexing
from p4a.z2utils import utils

from Products.CMFCore.utils import getToolByName

import logging
logger = logging.getLogger('p4a.ploneaudio.sitesetup')

try:
    import five.localsitemanager
    five.localsitemanager # pyflakes
    HAS_FLSM = True
    logger.info('Using five.localsitemanager')
except ImportError, err:
    HAS_FLSM = False

def setup_portal(portal):
    site.ensure_site(portal)
    setup_site(portal)
    indexing.ensure_object_provides(portal)

    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProducts(['CMFonFive'])

def setup_site(site):
    """Install all necessary components and configuration into the
    given site.

    """

    sm = site.getSiteManager()
    if not sm.queryUtility(interfaces.IAudioSupport):
        # registerUtility api changed between Zope 2.9 and 2.10
        if HAS_FLSM:
            sm.registerUtility(content.AudioSupport('audio_support'),
                               interfaces.IAudioSupport)
        else:
            sm.registerUtility(interfaces.IAudioSupport,
                               content.AudioSupport('audio_support'))

def _cleanup_utilities(site):
    raise NotImplementedError('Current ISiteManager support does not '
                              'include ability to clean up')

def unsetup_portal(portal):
    count = utils.remove_marker_ifaces(portal, \
        [interfaces.IAudioEnhanced, interfaces.IAudioContainerEnhanced])
    logger.warn('Removed IAudioEnhanced and IAudioContainerEnhanced '
                'interfaces from %i objects for cleanup' % count)
