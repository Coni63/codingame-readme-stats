from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.interfaces.i_user_info import IUserDto
from domain.interfaces.i_language import ILanguageDto
from domain.interfaces.i_certification import ICertificationDto
from domain.interfaces.i_achievement import IAchievementDto
from domain.interfaces.i_ranking import IRankingDto
from domain.interfaces.i_leaderboard import ILeaderboardDto


@dataclass_json
@dataclass
class IDataDto:
    user: IUserDto
    languages: list[ILanguageDto]
    certifications: list[ICertificationDto]
    achievements: list[IAchievementDto]
    rankings: IRankingDto
    leaderboard: ILeaderboardDto
