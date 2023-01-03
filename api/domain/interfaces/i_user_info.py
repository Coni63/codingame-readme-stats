from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class IHistoricsDto:
    clashPoints: list[int] = field(default_factory=lambda: [])
    codegolfPoints: list[int] = field(default_factory=lambda: [])
    contestPoints: list[int] = field(default_factory=lambda: [])
    dates: list[int] = field(default_factory=lambda: [])
    multiTrainingPoints: list[int] = field(default_factory=lambda: [])
    optimPoints: list[int] = field(default_factory=lambda: [])
    points: list[int] = field(default_factory=lambda: [])
    ranks: list[int] = field(default_factory=lambda: [])
    totals: list[int] = field(default_factory=lambda: [])


@dataclass_json
@dataclass
class IRankingDto:
    numberCodingamers: int
    numberCodingamersGlobal: int
    rankHistorics: IHistoricsDto
    codingamePointsAchievements: int = 0
    codingamePointsClash = int = 0
    codingamePointsCodegolf: int = 0
    codingamePointsContests: int = 0
    codingamePointsMultiTraining: int = 0
    codingamePointsOptim: int = 0
    codingamePointsRank: int = 0
    codingamePointsTotal: int = 0
    codingamePointsXp: int = 0


@dataclass_json
@dataclass
class ICodingameDto:
    userId: int 
    rank: int
    level: int
    formValues: dict = field(default_factory=lambda: {})
    enable: bool = True
    cover: int = 0
    publicHandle: str = ""
    tagline: str = ""
    countryId: str = ""
    city: str = ""
    category: str = ""
    avatar: int = 0
    xp: int = 0
    company: str = ""
    schoolId: int = 0
    pseudo: str = ""


@dataclass_json
@dataclass
class ILevelDto:
    cumulativeXp: int = 0
    level: int = 0
    xpThreshold: int = 0
    rewardLanguages: dict = field(default_factory=lambda: {})


@dataclass_json
@dataclass
class IUserDto:
    codingamePointsRankingDto: IRankingDto
    codingamer: ICodingameDto
    xpThresholds: list[ILevelDto] = field(default_factory=lambda: [])
    codingamerPoints: int = 0
    achievementCount: int = 0
