#!/bin/env python
from distutils.core import setup
setup(name='plunger',
      version='0.0.1',
      description='A 3D format converter',
      author='Kai Blin',
      author_email='kai.blin@gmail.com',
      url='http://wiki.worldforge.org/wiki/Plunger',
      scripts=['plunger/plunger'],
      packages=['plunger', 'plunger.plugins', 'plunger.plugins.collada_plugin',
	'plunger.plugins.ogrexml_plugin'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                   'Topic :: Multimedia :: Graphics :: Graphics Conversion',
                   'Topic :: Utilities'],
      )


