import unittest
from zope.testing import doctestunit

def test_suite():
    suite = unittest.TestSuite((
        doctestunit.DocTestSuite('p4a.ploneaudio.atct'),
        ))
    
    from p4a import ploneaudio
    if ploneaudio.has_ataudio_support():
        from p4a.ploneaudio.ataudio import tests
        suite.addTest(tests.test_suite())

    return suite
