import shutil
import tempfile
import os

from electrum import constants, blockchain
from electrum.simple_config import SimpleConfig
from electrum.blockchain import Blockchain, deserialize_header, hash_header
from electrum.util import bh2u, bfh, make_dir

from . import ElectrumTestCase


class TestVerifyHeader(ElectrumTestCase):

    # Data for Koto block header #1056620.
    valid_header = "0500000046b175f0bdab4d7c2c4cf501c9bb192d037d7b7dcefcf34a8684c19dca62b82c3c550621d820a798277b8ec063811d8b4d26f74868d9da61f4ff7c0da548f7f50678fc5d729a0e1d000030e72a9614689e6408a6c11985046866a02d4ee68e4def996b27d84c98675697df2f"
    target = Blockchain.bits_to_target(0x1d0e9a72)
    prev_hash = "2cb862ca9dc184864af3fcce7d7b7d032d19bbc901f54c2c7c4dabbdf075b146"

    def setUp(self):
        super().setUp()
        self.header = deserialize_header(bfh(self.valid_header), 1056620)

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
            other_target = Blockchain.bits_to_target(0x1d0eeeee)
            Blockchain.verify_header(self.header, self.prev_hash, other_target)

    def test_insufficient_pow(self):
        with self.assertRaises(Exception):
            self.header["nonce"] = 100
            Blockchain.verify_header(self.header, self.prev_hash, self.target)
