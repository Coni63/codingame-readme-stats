import json
import asyncio
import math
import aiohttp

from config import constants
from config import fake_data_1 as fake_data


async def _fetch(url: str, data: dict, session: aiohttp.ClientSession) -> dict:    
    async with session.request('POST', url=url, data=json.dumps(data), headers=constants.CG_headers) as r: 
        # CG api return always 200 but with null when valid reqest but invalid user
        if r.status == 200:
            return await r.json()
        else:
            raise ValueError("invalid request --> status code : {r.status}")


async def get_info_for(codingamer: str, session: aiohttp.ClientSession) -> dict:
    if codingamer == "magic":
        await asyncio.sleep(0.01)
        return fake_data.FAKE_USER

    json = [codingamer]
    return await _fetch(constants.CG_USER_GLOBAL_STATS, json, session)


async def get_certifications_for(userid: int, session: aiohttp.ClientSession) -> dict:
    if userid == 0:
        await asyncio.sleep(0.01)
        return fake_data.FAKE_CERTIF

    json = [userid]
    return await _fetch(constants.CG_USER_CERTIFICATIONS, json, session)


async def get_languages_used_by(userid: int, session: aiohttp.ClientSession) -> dict:
    if userid == 0:
        await asyncio.sleep(0.01)
        return fake_data.FAKE_LANGUAGES

    json = [userid]
    return await _fetch(constants.CG_USER_LANGUAGE, json, session)


async def get_achievements_for(userid: int, session: aiohttp.ClientSession) -> dict:
    if userid == 0:
        await asyncio.sleep(0.01)
        return fake_data.FAKE_ACHIVEMENTS

    json = [userid]
    return await _fetch(constants.CG_USER_ACHIEVEMENTS, json, session)


async def get_ranking_for(userid: int, session: aiohttp.ClientSession) -> dict:
    if userid == 0:
        await asyncio.sleep(0.01)
        return fake_data.FAKE_RANKING

    json = [userid]
    return await _fetch(constants.CG_USER_RANKINGS, json, session)


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
