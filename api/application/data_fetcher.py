import aiohttp
import asyncio
import re

from infrastructure import codingame_api

from domain import (
    IUserDto, 
    ILanguageDto, 
    ICertificationDto, 
    IAchievementDto, 
    IDataDto, 
    IRankingDto,
    IHistoricsDto
)


async def _get_user_data(codingamer: str, session: aiohttp.ClientSession) -> IUserDto:
    try:
        user_json  = await codingame_api.get_info_for(codingamer, session)
        if user_json is None:  # handle non existing codingamer
            raise ValueError("invalid Codingamer")

        user: IUserDto = IUserDto.from_dict(user_json)

        # empty history of ranks -- not used and use lot of memory
        user.codingamePointsRankingDto.rankHistorics = IHistoricsDto()

        return user
    except Exception as e:
        raise e


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
    if not re.match("^[0-9a-fA-F]+$", codingamer) and codingamer != "magic":
        raise ValueError("Invalid codingamer")

    # should be raised when the codingamer doesn't exist
    async with aiohttp.ClientSession() as session:
        try:
            user = await _get_user_data(codingamer, session)
            userid = user.codingamer.userId
        except ValueError as e:
            raise e

        # should not be raised -- at this stage we have for sure a valid codingamer
        # but maybe he does not have valid data for each sections
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [
                    asyncio.ensure_future(_get_languages_used_by(userid, session)),
                    asyncio.ensure_future(_get_certifications_for(userid, session)),
                    asyncio.ensure_future(_get_achievements_for(userid, session)),
                    asyncio.ensure_future(_get_ranking_for(userid, session)),
                ]

                ans = await asyncio.gather(*tasks)
                languages, certifications, achievements, rankings = ans

            return IDataDto(
                user=user,
                languages=languages,
                certifications=certifications,
                achievements=achievements,
                rankings=rankings,
            )
        except ValueError as e:
            raise e
