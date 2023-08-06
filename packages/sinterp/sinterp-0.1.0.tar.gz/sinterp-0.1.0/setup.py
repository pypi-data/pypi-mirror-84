# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='sinterp',
    version='0.1.0',
    packages=['sinterp', ],
    url='https://github.com/ndrwpvlv/sinterp',
    license='MIT',
    author='Andrei S. Pavlov',
    author_email='ndrw.pvlv@gmail.com',
    description='Simple fast linear interpolation for Python',
    download_url='https://github.com/ndrwpvlv/sinterp/archive/0.1.0.tar.gz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['interpolation', 'linear interpolation', ],

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['attrs==20.2.0', 'importlib-metadata==2.0.0', 'iniconfig==1.1.1', 'packaging==20.4',
                      'pluggy==0.13.1', 'py==1.9.0', 'pyparsing==2.4.7', 'pytest==6.1.2', 'six==1.15.0',
                      'toml==0.10.2', 'zipp==3.4.0', ],
)
