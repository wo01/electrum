# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from .util import inv_dict
from . import bitcoin


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/wo01/electrum-koto"
GIT_REPO_ISSUES_URL = "https://github.com/wo01/electrum-koto/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 0

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


class BitcoinMainnet(AbstractNet):

    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 0
    ADDRTYPE_P2SH = 5
    SEGWIT_HRP = "bc"
    GENESIS = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers_koto.json', {})
    CHECKPOINTS = read_json('checkpoints_koto.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 999999999

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
#        'p2wpkh-p2sh': 0x049d7878,  # yprv
#        'p2wsh-p2sh':  0x0295b005,  # Yprv
#        'p2wpkh':      0x04b2430c,  # zprv
#        'p2wsh':       0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
#        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
#        'p2wsh-p2sh':  0x0295b43f,  # Ypub
#        'p2wpkh':      0x04b24746,  # zpub
#        'p2wsh':       0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 0
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [
        'nodes.lightning.directory.',
        'lseed.bitcoinstats.com.',
    ]


class BitcoinTestnet(AbstractNet):

    TESTNET = True
    WIF_PREFIX = 0xef
    ADDRTYPE_P2PKH = 111
    ADDRTYPE_P2SH = 196
    SEGWIT_HRP = "tb"
    GENESIS = "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet_koto.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet_koto.json', [])

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
#        'p2wpkh-p2sh': 0x044a4e28,  # uprv
#        'p2wsh-p2sh':  0x024285b5,  # Uprv
#        'p2wpkh':      0x045f18bc,  # vprv
#        'p2wsh':       0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
#        'p2wpkh-p2sh': 0x044a5262,  # upub
#        'p2wsh-p2sh':  0x024289ef,  # Upub
#        'p2wpkh':      0x045f1cf6,  # vpub
#        'p2wsh':       0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        #'test.nodes.lightning.directory.',  # times out.
        #'lseed.bitcoinstats.com.',  # ignores REALM byte and returns mainnet peers...
    ]


class KotoMainnet(BitcoinMainnet):
    ADDRTYPE_P2PKH = [0x18, 0x36]
    ADDRTYPE_P2SH = [0x18, 0x3b]
    SEGWIT_HRP = "koto"
    OVERWINTER_HEIGHT = 335600
    SAPLING_HEIGHT = 556500
    GENESIS = "6d424c350729ae633275d51dc3496e16cd1b1d195c164da00f39c499a2e9959e"
    BIP44_COIN_TYPE = 510

class KotoTestnet(BitcoinTestnet):
    ADDRTYPE_P2PKH = [0x18, 0xa4]
    ADDRTYPE_P2SH = [0x18, 0x39]
    SEGWIT_HRP = "toko"
    OVERWINTER_HEIGHT = 93500
    SAPLING_HEIGHT = 275500
    GENESIS = "bf84afbde20c2d213b68b231ddb585ab616ef7567226820f00d9b397d774d2f0"

class KotoRegtest(KotoTestnet):
    SEGWIT_HRP = "reg"
    GENESIS = "dd905d5cda469020ddc364fdb530a4fb4559b9a117f78fdfbcc89d29d4909289"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    OVERWINTER_HEIGHT = -1
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class BitcoinSimnet(BitcoinTestnet):

    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


# don't import net directly, import the module instead (so that net is singleton)
net = KotoMainnet

def set_simnet():
    global net
    net = BitcoinSimnet

def set_mainnet():
    global net
    net = KotoMainnet


def set_testnet():
    global net
    net = KotoTestnet


def set_regtest():
    global net
    net = KotoRegtest
