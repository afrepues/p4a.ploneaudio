from zope import interface

class IFilename(interface.Interface):

    filename = interface.Attribute('Filename')
