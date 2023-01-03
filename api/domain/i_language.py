from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class ICertificateDto:
    lastTryDate: int
    programmingLanguageId: str
    languageName: str
    score: float
    comparativeScore: float
    communityStats: list[int]
    lowerScoreWarning: bool
    codingamerId: int
    certificationHistoryId: int
    handle: str
    visible: bool
    date: int
    diplomaPreviewId: int = 0
    type: str = ""
    legacy: bool = False
    candidateId: int = 0


@dataclass_json
@dataclass
class ILanguageDto:
    programmingLanguageId: str
    languageName: str
    logoId: int
    puzzleCount: int
    certification: Optional[ICertificateDto] = None
