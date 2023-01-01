import asyncio
import unittest
from application import evaluator, svg_builder, user_data

from application.svg_builder import get_scale, hex_to_rgb


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

    def test_render_readme_image(self):
        import os
        user_datas = asyncio.run(user_data.get_all_data("magic"))
        profile_data = evaluator.evaluate(user_datas, online=False)
        svg = svg_builder.render(profile_data)
        img_location = os.path.join(os.path.abspath(__file__), "..", "..", "..", "assets", "badge.svg")
        with open(img_location, "wb") as f:
            f.write(svg)
