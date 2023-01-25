from dataclasses import dataclass
from dataclasses_json import dataclass_json

from config import constants


@dataclass_json
@dataclass
class ICertificationDto:
    category: str
    level: str
    description: str

    def get_color(self) -> str:
        mapping = {
            "WOOD": constants.COLOR_WOOD,
            "BRONZE": constants.COLOR_BRONZE,
            "SILVER": constants.COLOR_SILVER,
            "GOLD": constants.COLOR_GOLD,
            "LEGEND": constants.COLOR_LEGEND,
        }
        return mapping.get(self.level, constants.COLOR_WOOD)

    def get_level(self) -> str:
        return self.level.capitalize()

    def get_title(self) -> str:
        titles: dict = {
            'COLLABORATION': 'Collaboration',
            'ALGORITHMS': 'Algorithms',
            'OPTIMIZATION': 'Optimization',
            'CODING_SPEED': 'Coding Speed',
            'AI': 'AI'
        }
        return titles[self.category]

    def get_icon(self) -> str:
        icons = {
            'COLLABORATION': constants.SVG_collaboration,
            'ALGORITHMS': constants.SVG_algorithmes,
            'OPTIMIZATION': constants.SVG_optimization,
            'CODING_SPEED': constants.SVG_speed,
            'AI': constants.SVG_AI,
        }

        return icons[self.category]

    def get_index(self) -> int:
        order = ['COLLABORATION', 'ALGORITHMS', 'OPTIMIZATION', 'CODING_SPEED', 'AI']
        return order.index(self.category)

    @staticmethod
    def get_titles_icon_in_order():
        titles: dict = {
            'COLLABORATION': 'Collaboration',
            'ALGORITHMS': 'Algorithms',
            'OPTIMIZATION': 'Optimization',
            'CODING_SPEED': 'Coding Speed',
            'AI': 'AI'
        }

        icons = {
            'COLLABORATION': constants.SVG_collaboration,
            'ALGORITHMS': constants.SVG_algorithmes,
            'OPTIMIZATION': constants.SVG_optimization,
            'CODING_SPEED': constants.SVG_speed,
            'AI': constants.SVG_AI,
        }

        for category in ['COLLABORATION', 'ALGORITHMS', 'OPTIMIZATION', 'CODING_SPEED', 'AI']:
            yield titles[category], icons[category]