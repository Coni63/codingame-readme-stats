import asyncio

from application import data_fetcher, svg_builder
from domain import evaluator
from infrastructure import cache_manager


def get_svg_for_user(codingamer, online: bool, second_category: str, third_category: str, language_number: int):

    user_datas = cache_manager.load_data(codingamer)

    if user_datas is None:
        try:
            user_datas = asyncio.run(data_fetcher.get_all_data(codingamer))
            cache_manager.save_data(codingamer, user_datas)
        except ValueError as e:
            return {"message": str(e)}, 404

    try:
        profile_data = evaluator.evaluate(user_datas, online=online)
        svg = svg_builder.render(profile_data, second_category, third_category, language_number)
    except Exception:
        return None

    return svg
