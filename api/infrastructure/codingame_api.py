import json
import requests
import asyncio
import math
import aiohttp

from config import constants
from config import fake_data

async def _fetch(url: str, data: dict, session: aiohttp.ClientSession) -> dict:    
    async with session.request('POST', url=url, data=json.dumps(data), headers=constants.CG_headers) as r: 
        return await r.json()

async def get_info_for(codingamer: str, session: aiohttp.ClientSession) -> dict:
    # json = [codingamer]
    # return await _fetch(constants.CG_USER_GLOBAL_STATS, json, session)

    await asyncio.sleep(0.1)
    return fake_data.FAKE_USER

async def get_certifications_for(userid: int, session: aiohttp.ClientSession) -> dict:
    # json = [userid]
    # return await _fetch(constants.CG_USER_CERTIFICATIONS, json, session)

    await asyncio.sleep(0.1)
    return fake_data.FAKE_CERTIF

async def get_languages_used_by(userid: int, session: aiohttp.ClientSession) -> dict:
    # json = [userid]
    # return await _fetch(constants.CG_USER_LANGUAGE, json, session)
    
    await asyncio.sleep(0.1)
    return fake_data.FAKE_LANGUAGES

async def get_achievements_for(userid: int, session: aiohttp.ClientSession) -> dict:
    # json = [userid]
    # return await _fetch(constants.CG_USER_ACHIEVEMENTS, json, session)
    
    await asyncio.sleep(0.1)
    return fake_data.FAKE_ACHIVEMENTS

async def get_ranking_for(userid: int, session: aiohttp.ClientSession) -> dict:
    # json = [userid]
    # return await _fetch(constants.CG_USER_RANKINGS, json, session)
    
    await asyncio.sleep(0.1)
    return fake_data.FAKE_RANKING


def get_points_from_rank(position: int, total: int, base: int = 5000) -> float:
    if position < 0: 
        raise ValueError("position must be a positive integer")

    if total < position: 
        raise ValueError("position must be lower than or equal to the total number of participants")

    if base <= 0: 
        raise ValueError("base must be a positive integer")

    b = int(base * min(total/500, 1))
    p = (total - position + 1) / total
    return round(math.pow(b, p))