#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/kotocolor.png'])
    ]

setup(
    name="Electrum",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require={
        'full': requirements_hw + ['pycryptodomex'],
    },
    packages=[
        'electrum',
        'electrum_gui',
        'electrum_gui.qt',
        'electrum_plugins',
        'electrum_plugins.audio_modem',
        'electrum_plugins.cosigner_pool',
        'electrum_plugins.email_requests',
        'electrum_plugins.greenaddress_instant',
        'electrum_plugins.hw_wallet',
        'electrum_plugins.keepkey',
        'electrum_plugins.labels',
        'electrum_plugins.ledger',
        'electrum_plugins.trezor',
        'electrum_plugins.digitalbitbox',
        'electrum_plugins.trustedcoin',
        'electrum_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum': 'lib',
        'electrum_gui': 'gui',
        'electrum_plugins': 'plugins',
    },
    package_data={
        'electrum': [
            'servers_koto.json',
            'servers_testnet_koto.json',
            'servers_regtest_koto.json',
            'currencies.json',
            'checkpoints_koto.json',
            'checkpoints_testnet_koto.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum'],
    data_files=data_files,
    description="Lightweight Koto Wallet",
    author="WO",
    author_email="wo@kotocoin.info",
    license="MIT Licence",
    url="https://electrum.kotocoin.info",
    long_description="""Lightweight Koto Wallet"""
)
