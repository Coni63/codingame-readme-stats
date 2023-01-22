from __future__ import annotations
from dataclasses import dataclass


@dataclass
class IValue:
    color: str
    title: str
    icon: str | None = None
    from_CG: bool | None = None
    value: str | None = None
    numerator: int | None = None
    denominator: int | None = None


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
    lang_list: list[IValue]
    leaderboard: list[IValue]
