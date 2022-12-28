import aiohttp
import asyncio

from infrastructure import codingame_api

from domain.i_user_info import IUserDto
from domain.i_language import ILanguageDto
from domain.i_certification import ICertificationDto
from domain.i_achievement import IAchievementDto
from domain.i_data import IDataDto
from domain.i_ranking import IRankingDto

async def _get_user_data(codingamer: str, session: aiohttp.ClientSession) -> IUserDto:
    user_json  = await codingame_api.get_info_for(codingamer, session)
    return IUserDto.from_dict(user_json)

async def _get_languages_used_by(userid: int, session: aiohttp.ClientSession) -> list[ILanguageDto]:
    languages_json = await codingame_api.get_languages_used_by(userid, session)
    return ILanguageDto.schema().load(languages_json, many=True)

async def _get_certifications_for(userid: int, session: aiohttp.ClientSession) -> list[ICertificationDto]:
    certifications_json = await codingame_api.get_certifications_for(userid, session)
    return ICertificationDto.schema().load(certifications_json, many=True)

async def _get_achievements_for(userid: int, session: aiohttp.ClientSession) -> list[IAchievementDto]:
    achievement_json = await codingame_api.get_achievements_for(userid, session)
    return IAchievementDto.schema().load(achievement_json, many=True)

async def _get_ranking_for(userid: int, session: aiohttp.ClientSession) -> IRankingDto:
    ranking_json = await codingame_api.get_ranking_for(userid, session)
    return IRankingDto.from_dict(ranking_json)

async def get_all_data(codingamer: str) -> IDataDto:
    async with aiohttp.ClientSession() as session:
        user = await _get_user_data(codingamer, session)
        userid = user.codingamer.userId

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(_get_languages_used_by(userid, session)),
            asyncio.ensure_future(_get_certifications_for(userid, session)),
            asyncio.ensure_future(_get_achievements_for(userid, session)),
            asyncio.ensure_future(_get_ranking_for(userid, session)),
        ]

        ans = await asyncio.gather(*tasks)
        languages, certifications, achievements, rankings = ans

    return IDataDto.from_dict({
        "user": user,
        "languages": languages,
        "certifications": certifications,
        "achievements": achievements,
        "rankings": rankings,
    })