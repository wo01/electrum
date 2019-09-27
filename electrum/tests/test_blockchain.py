import shutil
import tempfile
import os

from electrum import constants, blockchain
from electrum.simple_config import SimpleConfig
from electrum.blockchain import Blockchain, deserialize_header, hash_header
from electrum.util import bh2u, bfh, make_dir

from . import ElectrumTestCase


class TestVerifyHeader(ElectrumTestCase):

    # Data for Koto block header #890000.
    valid_header = "05000000a9fc843c50b522e2f721992b5e56e8d71e41c8582c37b1dc13b6be75a15387a56d55d71b20bd3c8bf6ad8028d9266d21841e6751a4a9681956131390cb7429ad2e1c635d25b9161d2aab7b086b16877ef06e5e2473d85c8f7fd7073c5e720ae02afd89ee35b166fa81b8b103"
    target = Blockchain.bits_to_target(0x1d16b925)
    prev_hash = "a58753a175beb613dcb1372c58c8411ed7e8565e2b9921f7e222b5503c84fca9"

    def setUp(self):
        super().setUp()
        self.header = deserialize_header(bfh(self.valid_header), 890000)

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
