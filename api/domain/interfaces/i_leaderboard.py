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
    achievementPointsRankCountry: int
    achievementPointsRankGlobal: int
    botProgrammingPointsRankCountry: int
    botProgrammingPointsRankGlobal: int
    clashPointsRankCountry: int
    clashPointsRankGlobal: int
    codegolfPointsRankCountry: int
    codegolfPointsRankGlobal: int
    contestPointsRankCountry: int
    contestPointsRankGlobal: int
    globalPointsRankCountry: int
    globalPointsRankGlobal: int
    optimPointsRankCountry: int
    optimPointsRankGlobal: int
    totalCodingamerCountry: ILeaderboardCountDto
    totalCodingamerGlobal: ILeaderboardCountDto
    countryId: str = ""
