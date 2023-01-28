from __future__ import annotations
import math
from config import constants


def get_points_from_rank(position: int, total: int, base: int = 5000) -> float:
    if position < 0: 
        raise ValueError("position must be a positive integer")

    if position == 0:  # case when the user never join a specific category
        return 0

    if total < position: 
        raise ValueError("position must be lower than or equal to the total number of participants")

    if base <= 0: 
        raise ValueError("base must be a positive integer")

    if total == 0:  # Detective Pikaptcha has 0 total and 0 in rankings
        return 0

    b = int(base * min(total/500, 1))
    p = (total - position + 1) / total
    return round(math.pow(b, p))


def bind_value_to_range(value: int | float, thresholds: list[int | float], outputs: list[any]):
    if len(thresholds)+1 != len(outputs):
        raise ValueError("length of thresholds must be equal to length of output - 1")

    for threshold, output in zip(thresholds, outputs):
        if value <= threshold:
            return output
    return outputs[-1]


def get_color(value: int | float, thresholds: list[int | float], ascending: bool = True):
    colors = [
        constants.COLOR_WOOD, 
        constants.COLOR_BRONZE, 
        constants.COLOR_SILVER, 
        constants.COLOR_GOLD, 
        constants.COLOR_LEGEND
    ]

    if not ascending:
        colors = colors[::-1]

    return bind_value_to_range(value, thresholds, colors)
