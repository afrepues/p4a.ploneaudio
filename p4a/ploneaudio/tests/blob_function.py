from plone.app.blob.tests import db

import os
import doctest
import unittest
from App import Common

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def load_package_products():
    import p4a.z2utils
    import p4a.common
    import p4a.fileimage
    import p4a.audio
    import p4a.ploneaudio
    import plone.app.blob
    import p4a.subtyper

    fiveconfigure.debug_mode = True
    zcml.load_config('meta.zcml', p4a.subtyper)
    zcml.load_config('configure.zcml', p4a.subtyper)
    zcml.load_config('configure.zcml', p4a.common)
    zcml.load_config('configure.zcml', p4a.fileimage)
    zcml.load_config('configure.zcml', p4a.audio)
    zcml.load_config('configure.zcml', p4a.ploneaudio)
    zcml.load_config('configure.zcml', plone.app.blob)
    fiveconfigure.debug_mode = False
    ztc.installPackage('p4a.ploneaudio')
    ztc.installPackage('plone.app.blob')

load_package_products()
ptc.setupPloneSite(products=['p4a.ploneaudio'], 
                   extension_profiles=['plone.app.blob:file-replacement'])


def test_suite():
    suite = unittest.TestSuite()

    suite.addTest(ztc.FunctionalDocFileSuite('plone-audio.txt',
                                             package='p4a.ploneaudio',
                                             optionflags=doctest.ELLIPSIS,
                                             test_class=ptc.FunctionalTestCase))

    suite.addTest(ztc.FunctionalDocFileSuite('syndication-integration.txt',
                                             package='p4a.ploneaudio',
                                             optionflags=doctest.ELLIPSIS,
                                             test_class=ptc.FunctionalTestCase))

    suite.addTest(ztc.FunctionalDocFileSuite('browser.txt',
                                             package='p4a.ploneaudio',
                                             optionflags=doctest.ELLIPSIS,
                                             test_class=ptc.FunctionalTestCase))

    return suite