import constants
import codingame_api

from interfaces.i_user_info import IUserDto
from interfaces.i_language import ILanguageDto
from interfaces.i_certification import ICertificationDto
from interfaces.i_achievement import IAchievementDto

def _get_user_data(codingamer):
    user_json  = codingame_api.get_info_for(codingamer)
    return IUserDto.from_dict(user_json)

def _get_languages_used_by(userid):
    languages_json = codingame_api.get_languages_used_by(userid)
    return ILanguageDto.schema().load(languages_json, many=True)

def _get_certifications_for(userid):
    certifications_json = codingame_api.get_certifications_for(userid)
    return ICertificationDto.schema().load(certifications_json, many=True)

def _get_achievements_for(userid):
    achievement_json = codingame_api.get_achievements_for(userid)
    return IAchievementDto.schema().load(achievement_json, many=True)

def get_all_data(codingamer:str) -> dict:
    user = _get_user_data(codingamer)

    userid = user.codingamer.userId

    languages = _get_languages_used_by(userid)
    certifications = _get_certifications_for(userid)
    achievements = _get_achievements_for(userid)

    return {
        "user": user.codingamer.userId,
        "a": len(achievements),
        "b": len(languages),
        "c": len(certifications),
    }