#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.code import setup
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, '../README.md')) as f:
    README = f.read()

setup(
    name='guibot',
    version='0.41.1',
    description='GUI automation tool',
    long_description=README,
    long_description_content_type='text/markdown',

    install_requires=[
        "Pillow",
    ],
    tests_require=[
        'PyQt5',
    ],

    url='http://guibot.org',
    maintainer='Intra2net',
    maintainer_email='opensource@intra2net.com',
    download_url='',

    packages=['guibot'],
    package_dir={'guibot': '../guibot'},

    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Desktop Environment',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
