from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from domain.evaluator import get_points_from_rank, get_color, bind_value_to_range


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

    def get_color_for(self, category):
        if category in ["bot", "contest", "optim", "codegolf"]:  # category where the player must be active
            thresholds = [166, 1285, 2911, 4037]
        else:                                                    # category with every players (or close to)
            thresholds = [3600, 4600, 4850, 4950]

        score = self.get_score_for(category)
        return get_color(score, thresholds, ascending=True)

    def get_score_for(self, category):
        config = {
            "global": (self.globalPointsRankGlobal, self.totalCodingamerGlobal.global_, 5000),
            "bot": (self.botProgrammingPointsRankGlobal, self.totalCodingamerGlobal.botProgramming, 5000),
            "contest": (self.contestPointsRankGlobal, self.totalCodingamerGlobal.contest, 5000),
            "optim": (self.optimPointsRankGlobal, self.totalCodingamerGlobal.optim, 5000),
            "clash": (self.clashPointsRankGlobal, self.totalCodingamerGlobal.clash, 5000),
            "codegolf": (self.codegolfPointsRankGlobal, self.totalCodingamerGlobal.codegolf, 5000),
        }

        score = get_points_from_rank(*config[category])
        return score

    def get_main_color_and_grade(self) -> tuple[str, str, float]:
        categories = ["global", "bot", "contest", "optim", "clash", "codegolf"]
        factors = [1, 1, 1, 1, 0.5, 0.2]

        grades = ["C", "B", "A", "S", "S+", "S++"]
        thresholds_grade = [5000, 11000, 14500, 18000, 20000]

        thresholds_color = [5000, 11000, 14500, 18000]

        score = sum(factor * self.get_score_for(category) for factor, category in zip(factors, categories))
        color = get_color(score, thresholds_color, ascending=True)
        grade = bind_value_to_range(score, thresholds_grade, grades)
        percent = 100 * score / 23500

        return color, grade, percent
