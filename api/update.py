import asyncio

from application import data_fetcher
from infrastructure import cache_manager

"""
Script scheduled every day
Will fetch data for every codingamer that uses the API
"""

for codingamer in cache_manager.list_cache():
    user_datas = asyncio.run(data_fetcher.get_all_data(codingamer))
    cache_manager.save_data(codingamer, user_datas)
