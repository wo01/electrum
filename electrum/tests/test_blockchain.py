import shutil
import tempfile
import os

from electrum import constants, blockchain
from electrum.simple_config import SimpleConfig
from electrum.blockchain import Blockchain, deserialize_header, hash_header
from electrum.util import bh2u, bfh, make_dir

from . import ElectrumTestCase


class TestVerifyHeader(ElectrumTestCase):

    # Data for Koto block header #1334541.
    valid_header = "05000000a8c37bcbf4aa6697e617391eb8fa9d740797db313fc1516f45ee6f93ead10999b82ce3068a1012c894b780057a750847f133bbb705a51ed7d77ac077553d6fa66e47fc5eb9a71f1d00002f8ead6b998975bb4415209950812cd41f881f9fef0b51bec0a3b0b1e822d5850524"
    target = Blockchain.bits_to_target(0x1d1fa7b9)
    prev_hash = "9909d1ea936fee456f51c13f31db9707749dfab81e3917e69766aaf4cb7bc3a8"

    def setUp(self):
        super().setUp()
        self.header = deserialize_header(bfh(self.valid_header), 1334541)

    def test_valid_header(self):
        Blockchain.verify_header(self.header, self.prev_hash, self.target)

    def test_expected_hash_mismatch(self):
        with self.assertRaises(Exception):
            Blockchain.verify_header(self.header, self.prev_hash, self.target,
                                     expected_header_hash="foo")

    def test_prev_hash_mismatch(self):
        with self.assertRaises(Exception):
            Blockchain.verify_header(self.header, "foo", self.target)

    def test_target_mismatch(self):
        with self.assertRaises(Exception):
            other_target = Blockchain.bits_to_target(0x1d300000)
            Blockchain.verify_header(self.header, self.prev_hash, other_target)

    def test_insufficient_pow(self):
        with self.assertRaises(Exception):
            self.header["nonce"] = 100
            Blockchain.verify_header(self.header, self.prev_hash, self.target)
