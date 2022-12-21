from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class IHistoricsDto:
    clashPoints: list[int]
    codegolfPoints: list[int]
    contestPoints: list[int]
    dates: list[int]
    multiTrainingPoints: list[int]
    optimPoints: list[int]
    points: list[int]
    ranks: list[int]
    totals: list[int]


@dataclass_json
@dataclass
class IRankingDto:
    codingamePointsAchievements: int
    codingamePointsClash = int
    codingamePointsCodegolf: int
    codingamePointsContests: int
    codingamePointsMultiTraining: int
    codingamePointsOptim: int
    codingamePointsRank: int
    codingamePointsTotal: int
    codingamePointsXp: int
    numberCodingamers: int
    numberCodingamersGlobal: int
    rankHistorics: IHistoricsDto


@dataclass_json
@dataclass
class ICodingameDto:
    avatar: int
    category: str
    city: str
    company: str
    countryId: str
    cover: int
    enable: bool
    formValues: dict
    level: int 
    pseudo: str
    publicHandle: str
    rank: int 
    schoolId: int 
    tagline: str
    userId: int 
    xp: int 


@dataclass_json
@dataclass
class ILevelDto:
    cumulativeXp: int 
    level: int 
    xpThreshold: int 
    rewardLanguages: Optional[dict] = None


@dataclass_json
@dataclass
class IUserDto:
    achievementCount: int
    codingamePointsRankingDto: IRankingDto
    codingamer: ICodingameDto
    codingamerPoints: int
    xpThresholds: list[ILevelDto]


