from p4a.audio import interfaces
from p4a.ploneaudio import content
from p4a.common import site

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName 

from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from zope.component.exceptions import ComponentLookupError
from p4a.audio.interfaces import IAudio

def setup_portal(portal):
    site.ensure_site(portal)
    setup_site(portal)
    setup_indexes(portal)
    setup_metadata(portal)
    setup_smartfolder_indexes(portal)
    
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProducts(['CMFonFive'])


def audio_artist(object, portal, **kwargs):
    try:
        audiofile = IAudio(object)
        return audiofile.artist
    except (ComponentLookupError, TypeError, ValueError):
        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

registerIndexableAttribute('audio_artist', audio_artist)

def audio_genre_id(object, portal, **kwargs):
    try:
        audiofile = IAudio(object)
        return audiofile.genre
    except (ComponentLookupError, TypeError, ValueError):
        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

registerIndexableAttribute('audio_genre_id', audio_genre_id)

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

def setup_indexes(portal):
    """Install specific indexes for the audio metadata fields
    so they are searchable."""
    
    out = StringIO()
    pc = getToolByName(portal, 'portal_catalog')

    if not 'audio_genre_id' in pc.indexes():
        pc.addIndex('audio_genre_id', 'FieldIndex')
        pc.manage_reindexIndex('audio_genre_id')
        print >>out, 'The FieldIndex "audio_genre_id" was successfully created'

    if not 'audio_artist' in pc.indexes():

        extra = cmfutils.SimpleRecord(lexicon_id='plaintext_lexicon',
        	                          index_type='Okapi BM25 Rank')
        
        pc.addIndex('audio_artist', 'ZCTextIndex', extra)
        pc.manage_reindexIndex('audio_artist')
        print >>out, 'The ZCTextIndex "audio_artist" was successfully created'

    if not 'Format' in pc.indexes():
        pc.addIndex('Format', 'FieldIndex')
        pc.manage_reindexIndex('Format')
        print >>out, 'The FieldIndex "Format" was successfully created'
    
def setup_metadata(portal):
    """Adds the specified columns to the catalog specified,
       which must inherit from CMFPlone.CatalogTool.CatalogTool, or otherwise
       use the Plone ExtensibleIndexableObjectWrapper."""
       
    out = StringIO()
    
    pc = getToolByName(portal, 'portal_catalog', None)

    try:
        pc.delColumn('audio_artist')
    except:
        pass

    reindex = []
        
    pc.manage_addColumn('audio_artist')
    reindex.append('audio_artist')
    
    if reindex:
        pc.refreshCatalog()
        
    print >>out, 'The metadata "audio_artist" was successfully added.'


def setup_smartfolder_indexes(portal):
    """Set up the smart folder indexes so that you can create smart folders
    of the MP3s added to the site."""
    
    out = StringIO()
    
    sft = getToolByName(portal, 'portal_atct')

    print >>out, 'enabling the Metadata to appear in the smart folder settings'

    if 'Format' not in sft.getIndexes(enabledOnly=True):
        sft.addIndex("Format", "Mime Types", "The type of the Item", enabled=True)
    elif 'Format' not in sft.getIndexes():
    # index exists, but is disabled 
        sft.updateIndex('Format', enabled=True)

    if 'Format' not in sft.getAllMetadata(enabledOnly=True):
        sft.addMetadata("Format", "Mime Types", "The type of the Item", enabled=True)
    elif 'Format' not in sft.getAllMetadata():     
    # metadata exist, but are disabled     
        sft.updateMetadata('Format', enabled=True) 


def _cleanup_utilities(site):
    raise NotImplementedError('Current ISiteManager support does not '
                              'include ability to clean up')
