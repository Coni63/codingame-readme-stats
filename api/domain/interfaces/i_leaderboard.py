from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class ILeaderboardCountDto:
    botProgramming: int
    clash: int
    codegolf: int
    contest: int
    optim: int
    global_: int = field(metadata=config(field_name="global"))


@dataclass_json
@dataclass
class ILeaderboardDto:
    codingamerId: int
    totalCodingamerCountry: ILeaderboardCountDto
    totalCodingamerGlobal: ILeaderboardCountDto
    achievementPointsRankCountry: int = 0
    achievementPointsRankGlobal: int = 0
    botProgrammingPointsRankCountry: int = 0
    botProgrammingPointsRankGlobal: int = 0
    clashPointsRankCountry: int = 0
    clashPointsRankGlobal: int = 0
    codegolfPointsRankCountry: int = 0
    codegolfPointsRankGlobal: int = 0
    contestPointsRankCountry: int = 0
    contestPointsRankGlobal: int = 0
    globalPointsRankCountry: int = 0
    globalPointsRankGlobal: int = 0
    optimPointsRankCountry: int = 0
    optimPointsRankGlobal: int = 0
    countryId: str = ""
