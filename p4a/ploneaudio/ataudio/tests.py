from unittest import TestSuite
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Products.PloneTestCase import layer
from Products.PloneTestCase import PloneTestCase

DEPENDENCIES = ['Archetypes', 'ATAudio']
PRODUCT_DEPENDENCIES = ['MimetypesRegistry', 'PortalTransforms',
                        'basesyndication', 'fatsyndication']

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    PloneTestCase.installProduct(dependency)

PRODUCTS = list(DEPENDENCIES)

PloneTestCase.setupPloneSite(products=PRODUCTS)

from Products.Five import zcml
import p4a.common
import p4a.audio
import p4a.ploneaudio

class MigrationTestCase(PloneTestCase.PloneTestCase):
    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        zcml.load_config('configure.zcml', p4a.common)
        zcml.load_config('configure.zcml', p4a.audio)
        zcml.load_config('configure.zcml', p4a.ploneaudio)

def test_suite():
    suite = TestSuite()
    suite.layer = layer.ZCMLLayer
    suite.addTest(ZopeDocFileSuite(
        'migration.txt',
        package='p4a.ploneaudio.ataudio',
        test_class=MigrationTestCase,
        )
    )

    return suite
