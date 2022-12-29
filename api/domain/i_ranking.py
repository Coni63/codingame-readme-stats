from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class IChallengeDto:
    title: str
    date: int
    lateTimeMax: int
    publicId: str
    privateChallenge: bool
    predefinedTestId: int
    ranking: int
    total: int
    points: int
    maxPoints: int


@dataclass_json
@dataclass
class IPuzzleDto:
    puzzlePublicId: str
    prettyId: str
    predefinedTestId: int 
    labelTitleId: int 
    lastActivity: int 
    labelTitle:  str
    ranking: int
    totalPlayers: int
    puzzleType: str
    points: float = 0.0  # not in codegolf
    ranksByLanguage: dict = field(default_factory=lambda: {})  # only for codegolf instead of points
    totalPlayersByLanguage: dict = field(default_factory=lambda: {})  # only for codegolf instead of points
    pointsByLanguage: dict = field(default_factory=lambda: {})  # only for codegolf instead of points


@dataclass_json
@dataclass
class IRankingDto:
    challenges: list[IChallengeDto] = field(default_factory=lambda: [])
    puzzles: list[IPuzzleDto] = field(default_factory=lambda: [])
