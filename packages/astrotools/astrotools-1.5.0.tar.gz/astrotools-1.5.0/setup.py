#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='astrotools',
    version='1.5.0',
    description='Python Astro Tools',
    long_description="""The astrotools documentation is provided http://astro.pages.rwth-aachen.de/astrotools/""",
    long_description_content_type='text/markdown',
    author='Teresa Bister, Martin Urban, David Walz, Marcus Wirtz',
    author_email='bister@physik.rwth-aachen.de, murban@physik.rwth-aachen.de, '
                 'walz@physik.rwth-aachen.de, mwirtz@physik.rwth-aachen.de',
    license='MIT',
    keywords='astro auger',
    url='http://astro.pages.rwth-aachen.de/astrotools/',
    project_urls={
        'Documentation': 'http://astro.pages.rwth-aachen.de/astrotools/',
        'Source': 'https://git.rwth-aachen.de/astro/astrotools',
        'Tutorial': 'http://astro.pages.rwth-aachen.de/astrotools/tutorial.html'
        },
    packages=['astrotools'],
    package_data={'astrotools': ['data/*.txt', 'data/*.dat', 'data/lnA/*', 'data/xmax/*', 'data/comp/*', 'simulation/*']},
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
    install_requires=['numpy', 'healpy', 'matplotlib', 'scipy']
)
