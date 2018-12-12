from decimal import Decimal

from electrum.util import format_satoshis, format_fee_satoshis, parse_URI

from . import SequentialTestCase


class TestUtil(SequentialTestCase):

    def test_format_satoshis(self):
        self.assertEqual("0.00001234", format_satoshis(1234))

    def test_format_satoshis_negative(self):
        self.assertEqual("-0.00001234", format_satoshis(-1234))

    def test_format_fee_float(self):
        self.assertEqual("1.7", format_fee_satoshis(1700/1000))

    def test_format_fee_decimal(self):
        self.assertEqual("1.7", format_fee_satoshis(Decimal("1.7")))

    def test_format_fee_precision(self):
        self.assertEqual("1.666",
                         format_fee_satoshis(1666/1000, precision=6))
        self.assertEqual("1.7",
                         format_fee_satoshis(1666/1000, precision=1))

    def test_format_satoshis_whitespaces(self):
        self.assertEqual("     0.0001234 ",
                         format_satoshis(12340, whitespaces=True))
        self.assertEqual("     0.00001234",
                         format_satoshis(1234, whitespaces=True))

    def test_format_satoshis_whitespaces_negative(self):
        self.assertEqual("    -0.0001234 ",
                         format_satoshis(-12340, whitespaces=True))
        self.assertEqual("    -0.00001234",
                         format_satoshis(-1234, whitespaces=True))

    def test_format_satoshis_diff_positive(self):
        self.assertEqual("+0.00001234",
                         format_satoshis(1234, is_diff=True))

    def test_format_satoshis_diff_negative(self):
        self.assertEqual("-0.00001234", format_satoshis(-1234, is_diff=True))

    def _do_test_parse_URI(self, uri, expected):
        result = parse_URI(uri)
        self.assertEqual(expected, result)

    def test_parse_URI_address(self):
        self._do_test_parse_URI('koto:k14q1H8QwqVTbuYHaUi4mzQ3CcUfUvLs3Bx',
                                {'address': 'k14q1H8QwqVTbuYHaUi4mzQ3CcUfUvLs3Bx'})

    def test_parse_URI_only_address(self):
        self._do_test_parse_URI('k1DwmGbGEi5SpKgbUa1vQRasGqvwBcbT6W6',
                                {'address': 'k1DwmGbGEi5SpKgbUa1vQRasGqvwBcbT6W6'})


    def test_parse_URI_address_label(self):
        self._do_test_parse_URI('koto:k11tYVUauz5zBWrNqqVFJqwJs4yZUahYEAm?label=electrum%20test',
                                {'address': 'k11tYVUauz5zBWrNqqVFJqwJs4yZUahYEAm', 'label': 'electrum test'})

    def test_parse_URI_address_message(self):
        self._do_test_parse_URI('koto:k19NZMAsRzmVG2KbZxhxuW1wmy3Rruc4mKY?message=electrum%20test',
                                {'address': 'k19NZMAsRzmVG2KbZxhxuW1wmy3Rruc4mKY', 'message': 'electrum test', 'memo': 'electrum test'})

    def test_parse_URI_address_amount(self):
        self._do_test_parse_URI('koto:jzzeWEjmdZDWRdRyJBzC7FFB6DFrDzueGvL?amount=0.0003',
                                {'address': 'jzzeWEjmdZDWRdRyJBzC7FFB6DFrDzueGvL', 'amount': 30000})

    def test_parse_URI_address_request_url(self):
        self._do_test_parse_URI('koto:k1BYGdsVP8WmHq12sDuw3e4ZuUCriLAaiVU?r=http://domain.tld/page?h%3D2a8628fc2fbe',
                                {'address': 'k1BYGdsVP8WmHq12sDuw3e4ZuUCriLAaiVU', 'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

    def test_parse_URI_ignore_args(self):
        self._do_test_parse_URI('koto:k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko?test=test',
                                {'address': 'k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko', 'test': 'test'})

    def test_parse_URI_multiple_args(self):
        self._do_test_parse_URI('koto:k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko?amount=0.00004&label=electrum-test&message=electrum%20test&test=none&r=http://domain.tld/page',
                                {'address': 'k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko', 'amount': 4000, 'label': 'electrum-test', 'message': u'electrum test', 'memo': u'electrum test', 'r': 'http://domain.tld/page', 'test': 'none'})

    def test_parse_URI_no_address_request_url(self):
        self._do_test_parse_URI('koto:?r=http://domain.tld/page?h%3D2a8628fc2fbe',
                                {'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

    def test_parse_URI_invalid_address(self):
        self.assertRaises(BaseException, parse_URI, 'koto:invalidaddress')

    def test_parse_URI_invalid(self):
        self.assertRaises(BaseException, parse_URI, 'notkoto:k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko')

    def test_parse_URI_parameter_polution(self):
        self.assertRaises(Exception, parse_URI, 'koto:k1CjN5qBaT8BKyXKDKNEuBKgFZKgyciNUko?amount=0.0003&label=test&amount=30.0')
