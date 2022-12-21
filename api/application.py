import constants
import codingame_api

import aiohttp
import asyncio
import json 

from interfaces.i_user_info import IUserDto
from interfaces.i_language import ILanguageDto
from interfaces.i_certification import ICertificationDto
from interfaces.i_achievement import IAchievementDto

async def _get_user_data(codingamer, session):
    user_json  = await codingame_api.get_info_for(codingamer, session)
    return IUserDto.from_dict(user_json)

async def _get_languages_used_by(userid, session):
    languages_json = await codingame_api.get_languages_used_by(userid, session)
    return ILanguageDto.schema().load(languages_json, many=True)

async def _get_certifications_for(userid, session):
    certifications_json = await codingame_api.get_certifications_for(userid, session)
    return ICertificationDto.schema().load(certifications_json, many=True)

async def _get_achievements_for(userid, session):
    achievement_json = await codingame_api.get_achievements_for(userid, session)
    return IAchievementDto.schema().load(achievement_json, many=True)

async def _fetch(url, data, session):    
    async with session.request('POST', url=url, data=data, headers=constants.CG_headers) as r: 
        return await r.json()

async def get_all_data(codingamer:str) -> dict:
    async with aiohttp.ClientSession() as session:
        user = await _get_user_data(codingamer, session)
        userid = user.codingamer.userId

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(_get_languages_used_by(userid, session)),
            asyncio.ensure_future(_get_certifications_for(userid, session)),
            asyncio.ensure_future(_get_achievements_for(userid, session))
        ]

        ans = await asyncio.gather(*tasks)
        languages, certifications, achievements = ans

    return {
        "user": user.codingamer.userId,
        "a": len(achievements),
        "b": len(languages),
        "c": len(certifications),
    }