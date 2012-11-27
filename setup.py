#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Main installation file for GeoBases.
'''

from setuptools import setup
from os import getenv
import os.path as op
from sys import stderr

INSTALL_REQUIRES = [
    # Public - core
    'pyyaml',
    'python_geohash',
    'python_Levenshtein',
    # Public - CLI
    'argparse',
    'termcolor',
    'colorama'
]

EXTRAS_REQUIRE = {
    # Private
    'OpenTrep': ['OpenTrepWrapper>=0.6']
}

DEPENDENCY_LINKS        = []
DEPENDENCY_LINKS_EXTRAS = {
    'OpenTrep' : ['http://oridist.orinet/python/']
}

# Managing OpenTrep dependency
WITH_OPENTREP = getenv('WITH_OPENTREP', None)

if WITH_OPENTREP == '1':
    # Forcing OpenTrepWrapper support
    INSTALL_REQUIRES.extend(EXTRAS_REQUIRE['OpenTrep'])
    DEPENDENCY_LINKS.extend(DEPENDENCY_LINKS_EXTRAS['OpenTrep'])

    print >> stderr, '/!\ Adding "%s" to mandatory dependencies' % \
            str(EXTRAS_REQUIRE['OpenTrep'])
else:
    print >> stderr, '/!\ Installing without "%s"' % \
            str(EXTRAS_REQUIRE['OpenTrep'])


try:
    # monkey patch: Crack SandboxViolation verification from
    # http://www.cubicweb.org/1422923
    #import setuptools.command.easy_install # only if easy_install avaible
    from setuptools.sandbox import DirectorySandbox as DS

    def _ok(self, path):
        """Return True if ``path`` can be written during installation."""
        return True

    DS._ok = _ok

except ImportError:
    raise


setup(
    name = 'GeoBases',
    version = '4.1.2',
    author = 'Alex Prengere',
    author_email = 'alex.prengere@amadeus.com',
    url = 'http://mediawiki.orinet.nce.amadeus.net/index.php/GeoBases',
    description = 'Some geographical functions.',
    ## This line induces bugs because it lacks the file relative path
    #long_description = open('README').read(),
    #
    # Manage standalone scripts
    entry_points = {
        'console_scripts' : [
            'GeoBase = GeoBaseMain:main'
        ]
    },
    #packages=find_packages(),
    packages = [
        'GeoBases'
    ],
    py_modules = [
        'GeoBaseMain'
    ],
    dependency_links = DEPENDENCY_LINKS,
    install_requires = INSTALL_REQUIRES,
    extras_require   = EXTRAS_REQUIRE,
    package_dir = {
        'GeoBases': 'GeoBases'
    },
    package_data = {
        'GeoBases': [
            "DataSources/Sources.yaml",
            "DataSources/CheckDataUpdates.sh",
            "MapAssets/*",
            "TablesAssets/*",
            "DataSources/*/*.csv",
            "DataSources/*/*.txt",
            "DataSources/*/*/*.csv",
            "DataSources/*/*/*.txt",
        ]
    },
    #scripts = [
    #    'GeoBases/DataSources/CheckDataUpdates.sh'
    #],
    data_files = [
        # Tests should not be exported
        #('test', [
        #    'test/test_GeoBases.py'
        #]),
        # Will create dir if needed
        (op.join(getenv('HOME'), '.zsh/completion/'), [
            'completion/_GeoBase'
        ])
    ]
)

