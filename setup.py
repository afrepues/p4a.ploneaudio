from setuptools import setup, find_packages
import os

versionfile = open(os.path.join('p4a', 'ploneaudio', 'VERSION.txt'))
version = versionfile.read().strip()
versionfile.close()

readme = open('README.txt')
long_description = readme.read()
readme.close()

setup(name='p4a.ploneaudio',
      version=version,
      description="Plone4Artists audio add-on for Plone ",
      long_description=long_description,
      classifiers=[
          'Framework :: Zope2',
          'Framework :: Zope3',
          'Framework :: Plone',
          'Programming Language :: Python',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Multimedia :: Sound/Audio',
          ],
      keywords='Plone4Artists audio mp3 ogg podcasting podcast id3 music',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      url='http://www.plone4artists.org/products/plone4artistsaudio',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['p4a'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'p4a.audio>=1.1dev',
          'p4a.common',
          'p4a.fileimage',
          'p4a.subtyper',
          'p4a.z2utils',
          'setuptools',
          'zope.annotation',
          'zope.app.event',
          'zope.component',
          'zope.event',
          'zope.interface',
          'zope.schema'
          ],
      extras_require=dict(tests=[
          'Products.fatsyndication',
          'Products.MimeTypesRegistry',
          'Products.PloneTestCase',
          'zope.app.annotation',
          'zope.publisher',
          'plone.app.blob'
      ]),
      )
