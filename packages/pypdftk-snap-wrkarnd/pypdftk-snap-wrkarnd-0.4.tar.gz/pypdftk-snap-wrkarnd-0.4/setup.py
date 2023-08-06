#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pypdftk-snap-wrkarnd',
    description='''Python wrapper for PDFTK with snap installation workaround''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.4',
    author='Julien Bouquillon',
    author_email='julien@revolunet.com',
    url='http://github.com/revolunet/pypdftk',
    py_modules=['pypdftk'],
    scripts=['pypdftk.py'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
