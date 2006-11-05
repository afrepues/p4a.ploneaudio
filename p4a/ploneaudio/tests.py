import unittest
import doctest
from zope.testing import doctestunit
from p4a.ploneaudio import testing
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

def test_suite():
    suite = unittest.TestSuite((
        doctestunit.DocTestSuite('p4a.ploneaudio.atct'),
        ))
    
    from p4a import ploneaudio

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

    return suite
