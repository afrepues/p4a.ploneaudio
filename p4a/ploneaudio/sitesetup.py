from p4a.audio import interfaces
from p4a.ploneaudio import content
from p4a.common import site

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName, SimpleRecord 

from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from zope.component.exceptions import ComponentLookupError
from p4a.audio.interfaces import IAudio

def setup_portal(portal):
    site.ensure_site(portal)
    setup_site(portal)
    setup_indexes(portal)
    setup_metadata(portal)
    addSmartFolderIndexAndMetadata(portal)
    
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProducts(['CMFonFive'])


def audio_artist(object, portal, **kwargs):
    """Return the name of the artist in the audio file for use in searching the catalog."""
    try:
        audiofile = IAudio(object)
        return audiofile.artist
    except (ComponentLookupError, TypeError, ValueError):
        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

registerIndexableAttribute('audio_artist', audio_artist)

def audio_genre_id(object, portal, **kwargs):
    """Return the genre id of the audio file for use in searching the catalog."""
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

        extra = SimpleRecord(lexicon_id='plaintext_lexicon',
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
            
index_mapping = {'audio_artist':
                    {'name': 'Artist name',
                     'description': 'The name of the artist.',
                     'enabled': True,
                     'criteria': ('ATSimpleStringCriterion',)},
                 'audio_genre_id':
                    {'name': 'Genre',
                     'description': 'The genre id of the song.'
                                    'this is a number 0-147. '
                                    'See genre.py for the genre names.',
                     'enabled': True,
                     'criteria': ('ATSimpleIntCriterion',)},
                 'Format':
                    {'name': 'MIME Types',
                     'description': 'The MIME type of the file. '
                                 'For an MP3 file, this is audio/mpeg.',
                     'enabled': True,
                     'criteria': ('ATSimpleStringCriterion',)},
                 }

def addSmartFolderIndexAndMetadata(portal,
                                   indexes=('audio_artist',
                                            'audio_genre_id',
                                            'Format')):
    """Adds the default indexes to be available from smartfolders"""
    atct_config = getToolByName(portal, 'portal_atct', None)
    if atct_config is not None:
        for index in indexes:
            index_info=index_mapping[index]
            atct_config.updateIndex(index, friendlyName=index_info['name'],
                                 description=index_info['description'],
                                 enabled=index_info['enabled'],
                                 criteria=index_info['criteria'])
            atct_config.updateMetadata(index, friendlyName=index_info['name'],
                                 description=index_info['description'],
                                 enabled=True)
                                     
def _cleanup_utilities(site):
    raise NotImplementedError('Current ISiteManager support does not '
                              'include ability to clean up')
