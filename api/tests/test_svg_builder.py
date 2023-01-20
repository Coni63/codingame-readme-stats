import unittest

from application.svg_builder import get_scale, hex_to_rgb, human_format


class TestRendererMethods(unittest.TestCase):

    def test_get_scale(self):
        self.assertAlmostEqual(get_scale("20px", 20), 1.0)
        self.assertAlmostEqual(get_scale("40px", 20), .5)
        self.assertAlmostEqual(get_scale("2px", 20), 10.0)
        self.assertAlmostEqual(get_scale("20", 20), 1.0)
        self.assertAlmostEqual(get_scale("40", 20), .5)
        self.assertAlmostEqual(get_scale("2", 20), 10.0)
        self.assertAlmostEqual(get_scale(20, 20), 1.0)
        self.assertAlmostEqual(get_scale(40, 20), .5)
        self.assertAlmostEqual(get_scale(2, 20), 10.0)

    def test_invalid_get_scale(self):
        with self.assertRaises(ValueError):
            get_scale("20%")

    def test_hex_to_rgb(self):
        self.assertSequenceEqual(hex_to_rgb("#FF0000"), (1.0, 0.0, 0.0))
        self.assertSequenceEqual(hex_to_rgb("#00FF00"), (0.0, 1.0, 0.0))
        self.assertSequenceEqual(hex_to_rgb("#0000FF"), (0.0, 0.0, 1.0))
        self.assertSequenceEqual(hex_to_rgb("#FF00FF"), (1.0, 0.0, 1.0))
        self.assertSequenceEqual(hex_to_rgb("#ff00ff"), (1.0, 0.0, 1.0))

    def test_invalid_hex_to_rgb(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("#F0F")  # invalid -- shorten format

        with self.assertRaises(ValueError):
            hex_to_rgb("FF00FF")  # invalid format -- missing #

        with self.assertRaises(ValueError):
            hex_to_rgb("#ZZ00AA")  # invalid letter

    def test_human_format(self):
        self.assertEqual(human_format(1), "1")
        self.assertEqual(human_format(9), "9")
        self.assertEqual(human_format(10), "10")
        self.assertEqual(human_format(99), "99")
        self.assertEqual(human_format(100), "100")
        self.assertEqual(human_format(999), "999")
        self.assertEqual(human_format(1000), "1k")
        self.assertEqual(human_format(1234), "1.23k")
        self.assertEqual(human_format(9999), "10k")
        self.assertEqual(human_format(10000), "10k")
        self.assertEqual(human_format(12345), "12.3k")
        self.assertEqual(human_format(99999), "100k")
        self.assertEqual(human_format(100000), "100k")
        self.assertEqual(human_format(999999), "1m")
        self.assertEqual(human_format(1000000), "1m")
        self.assertEqual(human_format(9999999), "10m")
