from __future__ import annotations

from dataclasses import dataclass

import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
    from domain import IDataDto


@dataclass
class IValue:
    color: str
    title: str
    icon: str | None = None
    from_CG: bool | None = None
    value: str | None = None
    numerator: int | None = None
    denominator: int | None = None

    def __post_init__(self):
        if self.denominator:
            self.percent_rank = math.ceil(self.numerator / self.denominator * 1000) / 10


@dataclass
class IProfileDto:
    username: str
    active_color: str 
    passive_color: str
    main_rank: str
    score: int
    level: IValue
    certifications: list[IValue]
    language: IValue
    puzzle_solved: IValue
    achievements: IValue
    rank: IValue
    competition: IValue
    bot_battle: IValue
    lang_list: list[IValue]
    leaderboard: list[IValue]

    @staticmethod
    def from_user(user: IDataDto) -> IProfileDto:  # pragma: no cover 
        level_value = user.get_score_level()
        certif_value = user.get_score_certificate()
        top_language_value = user.get_score_best_language()
        puzzle_solved_value = user.get_score_total_solved()
        achievements_value = user.get_score_achievements()
        rank_value = user.get_score_rank()
        bot_value = user.get_score_competition(online=False)
        comp_value = user.get_score_competition(online=True)
        lang_list = user.get_score_list_language()
        leaderboard_list = user.get_score_list_leaderboard()

        (active_color, passive_color, score, label) = user.get_main_level()

        return IProfileDto(
            username=user.user.get_pseudo(),
            active_color=active_color,
            passive_color=passive_color,
            main_rank=label,
            level=level_value,
            certifications=certif_value,
            language=top_language_value,
            puzzle_solved=puzzle_solved_value,
            achievements=achievements_value,
            rank=rank_value,
            competition=comp_value,
            bot_battle=bot_value,
            score=score,
            lang_list=lang_list,
            leaderboard=leaderboard_list
        )
