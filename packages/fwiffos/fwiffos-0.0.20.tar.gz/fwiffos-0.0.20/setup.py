# -*- coding: utf-8 -*-

from setuptools import setup
from os import path


HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.fwiffos.rst'), encoding='utf-8') as f:
    readme = f.read()

packages = [
    'fwiffos.core',
    'fwiffos.cli',
    'fwiffos.read',
    'fwiffos.write',
    'fwiffos.post',
    'fwiffos.scuttle',
]

requires = [
    'fire>=0.3.1',
    'ipython>=7.17.0',
    'python-ldap>=3.3.1',
]

setup(
    name='fwiffos',
    version='0.0.20',
    description='FwiffOS',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='SCUPPER™ Foundation',
    author_email='info@scupper.org',
    url='https://github.com/SCUPPERfoundation/fwiffo',
    license='MIT',
    packages=packages,
    package_data = {'': ['LICENSE', 'README.fwiffos.rst']},
    package_dir = {'fwiffos': 'fwiffos'},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={"console_scripts":"fwiffish=fwiffos.cli.__main__:main"},
)

