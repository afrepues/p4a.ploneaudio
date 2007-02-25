import os
import unittest
import doctest
from zope.testing import doctestunit
from p4a import ploneaudio
from p4a.ploneaudio import testing
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from App import Common
from Products.PloneTestCase import layer

def test_suite():
    suite = unittest.TestSuite((
        doctestunit.DocTestSuite('p4a.ploneaudio.atct')
        ))
    
    if ploneaudio.has_ataudio_support():
        from p4a.ploneaudio.ataudio import tests
        suite.addTest(tests.test_suite())

    if ploneaudio.has_fatsyndication_support():
        suite.addTest(ZopeDocFileSuite(
            'syndication.txt',
            package='p4a.ploneaudio',
            test_class=testing.IntegrationTestCase,
            optionflags=doctest.ELLIPSIS,
            )
        )

    suite.addTest(ZopeDocFileSuite(
        'plone-audio.txt',
        package='p4a.ploneaudio',
        test_class=testing.testclass_builder(file_type='File')
        )
    )

    suite.addTest(FunctionalDocFileSuite(
        'plone-audio-functional.txt',
        package='p4a.ploneaudio',
        test_class=testing.testclass_builder()
        )
    )
    
    pkg_home = Common.package_home({'__name__': 'p4a.audio.tests'})
    samplesdir = os.path.join(pkg_home, 'samples')
    
    fields = dict(
        title=u'Test of the Emercy Broadcast System',
        artist=u'Rocky Burt',
        album=u'Emergencies All Around Us',
        )
    SAMPLES = (
        (os.path.join(samplesdir, 'test-full.mp3'), 'audio/mpeg', fields),
        (os.path.join(samplesdir, 'test-full.ogg'), 'application/ogg', fields),
        (os.path.join(samplesdir, 'test-no-images.mp3'), 'audio/mpeg', fields),
    )

    for samplefile, mimetype, fields in SAMPLES:
        suite.addTest(ZopeDocFileSuite(
            'plone-audio-impl.txt',
            package='p4a.ploneaudio',
            test_class=testing.testclass_builder(samplefile=samplefile,
                                                 required_mimetype=mimetype,
                                                 file_content_type='File',
                                                 fields=fields)
            )
        )

    if ploneaudio.has_blobfile_support():
        # setup the same test to run against BlobFile if available
        samplefile, mimetype, fields = SAMPLES[0]
        suite.addTest(ZopeDocFileSuite(
            'plone-audio-impl.txt',
            package='p4a.ploneaudio',
            test_class=testing.testclass_builder(samplefile=samplefile,
                                                 required_mimetype=mimetype,
                                                 file_content_type='BlobFile',
                                                 fields=fields)
            )
        )

    suite.layer = layer.ZCMLLayer

    return suite
