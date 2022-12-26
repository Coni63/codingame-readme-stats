from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


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
    points: Optional[float] = 0.0                 # not in codegolf
    ranksByLanguage: Optional[dict] = None        # only for codegolf instead of points
    totalPlayersByLanguage: Optional[dict] = None # only for codegolf instead of points
    pointsByLanguage: Optional[dict] = None       # only for codegolf instead of points


@dataclass_json
@dataclass
class IRankingDto:
    challenges: list[IChallengeDto]
    puzzles: list[IPuzzleDto]
    