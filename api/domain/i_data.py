from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.i_user_info import IUserDto
from domain.i_language import ILanguageDto
from domain.i_certification import ICertificationDto
from domain.i_achievement import IAchievementDto


@dataclass_json
@dataclass
class IDataDto:
    user: IUserDto
    languages : list[ILanguageDto]
    certifications : list[ICertificationDto]
    achievements : list[IAchievementDto]
