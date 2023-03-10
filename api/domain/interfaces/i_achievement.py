from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class IAchievementDto:
    id: str
    puzzleId: int
    title: str
    description: str
    points: int
    progress: int
    progressMax: int
    completionTime: int
    imageBinaryId: int
    categoryId: str
    groupId: str
    level: str
    weight: float
    unit: str = ""
    unlockText: str = ""

    def can_count(self):
        return self.categoryId not in ["coder", "social"]

    def get_weight(self):
        if self.completionTime > 0:
            return True, self.weight
        return False, self.weight
