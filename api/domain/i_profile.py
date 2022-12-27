from dataclasses import dataclass


@dataclass
class IValue:
    value: str
    color: str


@dataclass
class IProfileDto:
    username: str
    active_color: str 
    passive_color: str
    main_rank: str
    score: int
    level: IValue
    certifications: list[IValue]
    language : IValue
    puzzle_solved : IValue
    achievements : IValue
    rank : IValue
    competition : IValue

