# -*- coding: utf-8 -*-

from setuptools import setup

from SimLight._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

# exec(open('./SimLight/_version.py').read())

setup(
    name='SimLight',
    description='A tool helps your optical simulation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    version=__version__,
    author='Miyoshichi',
    author_email='zhou.x.ae@m.titech.ac.jp',
    packages=['SimLight'],
    install_requires=[
        'numpy',
        'matplotlib',
        'julia',
        'scipy',
        'scikit-image',
        'pillow',
        'pyfftw'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    url='https://github.com/Miyoshichi/SimLight'
)
