import asyncio

from application import data_fetcher, svg_builder
from domain import IProfileDto
from infrastructure import cache_manager


def get_svg_for_user(codingamer, online: bool, first_category: str, second_category: str, third_category: str, language_number: int):

    user_datas = cache_manager.load_data(codingamer)

    if user_datas is None:
        try:
            user_datas = asyncio.run(data_fetcher.get_all_data(codingamer))
            cache_manager.save_data(codingamer, user_datas)
        except ValueError as e:
            return {"message": str(e)}, 404

    # try:
    profile_data = IProfileDto.from_user(user_datas)
    svg = svg_builder.render(profile_data, first_category, second_category, third_category, language_number)
    # except Exception:
        # return None

    return svg
