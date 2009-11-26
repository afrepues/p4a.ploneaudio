import os, tempfile

from zope import interface, component

from Products.ATContentTypes import interface as atctifaces
from plone.app.blob import interfaces as pa_blob_ifaces

from p4a.fileimage import utils as fileutils
from p4a.audio import interfaces as audio_ifaces
from p4a.ploneaudio import atct as atct_audio

import interfaces

class Filename(object):
    interface.implements(interfaces.IFilename)

    def __init__(self, filename):
        self.filename = filename

@interface.implementer(interfaces.IFilename)
@component.adapter(atctifaces.IATFile)
def getATCTFileFilename(context):
    field = context.getPrimaryField()
    filename = fileutils.write_ofsfile_to_tempfile(
        field.getEditAccessor(context)(),
        context.getId())
    return Filename(filename)

@interface.implementer(interfaces.IFilename)
@component.adapter(pa_blob_ifaces.IATBlob)
def getATBlobFilename(context):
    field = context.getPrimaryField()
    blob = field.getEditAccessor(context)()
    id = context.getId()

    fd, filename = tempfile.mkstemp('_'+id)
    os.close(fd)
    fout = open(filename, 'wb')
    opened = blob.blob.open()
    fout.write(opened.read())
    opened.close()
    fout.close()

    return Filename(filename)

def _load_metadata(self, accessor_iface):
    mime_type = self.context.get_content_type()
    accessor = component.queryAdapter(
        self.context, accessor_iface, unicode(mime_type))
    if accessor is not None:
        filename = interfaces.IFilename(
            self.context).filename
        accessor.load(filename)
        os.remove(filename)

class _ATCTFileAudio(atct_audio._ATCTFileAudio):
    def _load_audio_metadata(self):
        return _load_metadata(self, audio_ifaces.IAudioDataAccessor)

    def _save_audio_metadata(self):
        mime_type = self.context.get_content_type()
        accessor = component.queryAdapter(
            self.context, audio_ifaces.IAudioDataAccessor,
            unicode(mime_type))
        if accessor is not None:
            filename = interfaces.IFilename(
                self.context).filename
            accessor.store(filename)

            field = self.context.getPrimaryField()
            wrapper = field.getEditAccessor(self.context)()
            wrapper.blob.consumeFile(filename)

@interface.implementer(audio_ifaces.IAudio)
@component.adapter(pa_blob_ifaces.IATBlob)
def ATCTFileAudio(context):
    if not audio_ifaces.IAudioEnhanced.providedBy(context):
        return None
    return _ATCTFileAudio(context)

