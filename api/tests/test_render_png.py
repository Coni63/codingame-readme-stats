import asyncio
import unittest

from pathlib import Path

from application import evaluator, svg_builder, user_data


class TestRendererMethods(unittest.TestCase):

    def test_render_readme_image(self):
        user_datas = asyncio.run(user_data.get_all_data("magic"))
        profile_data = evaluator.evaluate(user_datas, online=False)

        root = Path('.').resolve().parent / "assets"

        svg = svg_builder.render(profile_data, second_category=None)
        img_location = root / "badge_simple_category.svg"
        with open(img_location, "wb") as f:
            f.write(svg)

        svg = svg_builder.render(profile_data, second_category="certifications")
        img_location = root / "badge_certifications.svg"
        with open(img_location, "wb") as f:
            f.write(svg)

        svg = svg_builder.render(profile_data, second_category="languages")
        img_location = root / "badge_languages.svg"
        with open(img_location, "wb") as f:
            f.write(svg)

        svg = svg_builder.render(profile_data, second_category="languages", second_category_number=3)
        img_location = root / "badge_languages_top.svg"
        with open(img_location, "wb") as f:
            f.write(svg)


if __name__ == '__main__':
    unittest.main()
