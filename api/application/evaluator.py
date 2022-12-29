from config import constants

from domain.i_data import IDataDto
from domain.i_profile import IProfileDto, IValue
from domain.i_language import ILanguageDto
from domain.i_achievement import IAchievementDto
from domain.i_certification import ICertificationDto
from domain.i_user_info import IUserDto

from infrastructure.codingame_api import get_points_from_rank


def evaluate(data: IDataDto, online: bool = True) -> IProfileDto:  # pragma: no cover 
    level_value = get_score_level(data.user)
    certif_value = get_score_certificate(data.certifications)
    top_language_value = get_score_best_language(data.languages)
    puzzle_solved_value = get_score_total_solved(data.languages)
    achievements_value = get_score_achievements(data.achievements)
    rank_value = get_score_rank(data.user)
    comp_value = get_score_competition(data.rankings, online=online)

    (active_color, passive_color, score, label) = get_main_level(
        level_value,
        certif_value,
        top_language_value,
        puzzle_solved_value,
        achievements_value,
        rank_value,
        comp_value
    )

    return IProfileDto(
        username=data.user.codingamer.pseudo,
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
        score=score
    )

##########################
# Fonctions to handle colors
##########################


def _bind_value_to_range(value: int | float, thresholds: list[int | float], outputs: list[any]):
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

    return _bind_value_to_range(value, thresholds, colors)


def get_color_from_string(string: str) -> str:
    mapping = {
        "WOOD": constants.COLOR_WOOD,
        "BRONZE": constants.COLOR_BRONZE,
        "SILVER": constants.COLOR_SILVER,
        "GOLD": constants.COLOR_GOLD,
        "LEGEND": constants.COLOR_LEGEND,
    }
    return mapping.get(string, constants.COLOR_WOOD)


##########################
# Fonctions to compute scores
##########################


def get_score_level(user: IUserDto) -> IValue:
    # quantiles of levels in CG using the top 100k players
    # threshold used are 25% of the remaining players at every steps
    # wood is bottom 75%
    # bronze is bottom 75% for the 25% remaining players
    # and so forth
    # Silver is top 6.25%
    # Gold is top 1.56%
    # Legend is 0.4% top players
    # quantile = [(1 - (0.25)**i) for i in range(1, 5)]
    thresholds = [9, 16, 24, 31]

    return IValue(
        value=user.codingamer.level,
        color=get_color(user.codingamer.level, thresholds, ascending=True),
        title="Level",
        icon=constants.SVG_LEVEL,
        from_CG=False
    )


def get_score_certificate(certifications: list[ICertificationDto]) -> list[IValue]:
    order = ['COLLABORATION', 'ALGORITHMS', 'OPTIMIZATION', 'CODING_SPEED', 'AI']
    titles = {
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

    ans = [IValue(
        value="WOOD", 
        color=constants.COLOR_WOOD, 
        title=titles[cat],
        icon=icons[cat],
        from_CG=True
    ) for cat in order]

    for certification in certifications:
        idx = order.index(certification.category)
        level = certification.level
        ans[idx] = IValue(
            value=level, 
            color=get_color_from_string(level),
            title=titles[certification.category],
            icon=icons[certification.category],
            from_CG=True
        )
    return ans


def get_score_best_language(languages: list[ILanguageDto]) -> IValue:
    thresholds = [10, 25, 50, 100]

    top = max(languages, key=lambda x: x.puzzleCount)
    return IValue(
        value=top.languageName, 
        color=get_color(top.puzzleCount, thresholds, ascending=True),
        title="Best Language",
        icon=constants.SVG_BEST_LANGUAGE,
        from_CG=False
    )


def get_score_total_solved(languages: list[ILanguageDto]) -> IValue:
    thresholds = [25, 50, 125, 250]
    total = sum(x.puzzleCount for x in languages)
    return IValue(
        value=total, 
        color=get_color(total, thresholds, ascending=True),
        title="Puzzles Solved",
        icon=constants.SVG_PUZZLE_SOLVED,
        from_CG=False
    )


def get_score_achievements(achievements: list[IAchievementDto]) -> IValue:
    # Based on points given to every success (harder succes provides more points)
    # the sum of achieved success / total success is used
    # threshold used are 67% of the remaining players at every steps
    # To be a legend, you need to have 80% of success score
    # every success does not count
    # [1-((0.67)**i) for i in range(1, 5)]
    thresholds = [0.33, 0.55, 0.70, 0.79]

    skip = ["coder", "social"]
    total_solved = 0
    total_available = 0
    count_solved = 0
    count_available = 0
    for achievement in achievements:
        if achievement.categoryId in skip:
            continue

        if achievement.completionTime > 0:
            total_solved += achievement.weight
            count_solved += 1

        total_available += achievement.weight
        count_available += 1

    return IValue(
        value=f"{count_solved}/{count_available}",
        color=get_color(total_solved / total_available, thresholds, ascending=True),
        title="Success",
        icon=constants.SVG_SUCCESS,
        from_CG=False
    )


def get_score_rank(user: IUserDto) -> IValue:
    # threshold used are 25% of the remaining players at every steps limited to 100k
    # wood is bottom 75%
    # bronze is bottom 75% for the 25% remaining players
    # and so forth
    # Silver is top 6.25%
    # Gold is top 1.56%
    # Legend is 0.4% top players
    # [100000*((0.25)**i) for i in range(1, 5)]
    thresholds = [390, 1562, 6250, 25000]

    rank = user.codingamer.rank
    last_rank = user.codingamePointsRankingDto.numberCodingamersGlobal

    return IValue(
        value=f"{rank}/{last_rank}", 
        color=get_color(rank, thresholds, ascending=False),
        title="Global Rank",
        icon=constants.SVG_GLOBAL_RANK,
        from_CG=False
    )


def get_score_competition(rankings, online=False):
    # threshold used are 60% of the remaining players at every steps limited to 100k
    # wood is bottom 60%
    # bronze is bottom 60% for the 40% remaining players
    # and so forth
    # Silver is top 16%
    # Gold is top 6.5%
    # Legend is 1.5% top players
    # everything is based on 5000 base score from CG's formula
    # [math.pow(5000, (2000-((0.4**i)*2000)+1)/2000) for i in range(1, 5)]
    thresholds = [166, 1285, 2911, 4037]

    if online:
        top = max(rankings.challenges, key=lambda x: get_points_from_rank(x.ranking, x.total))

        points = get_points_from_rank(top.ranking, top.total)
        return IValue(
            value=f"{top.ranking}/{top.total}", 
            color=get_color(points, thresholds, ascending=True),
            title="Highest Compet.",
            icon=constants.SVG_HIGHEST_COMP,
            from_CG=False
        )
    else:
        f = [x for x in rankings.puzzles if x.puzzleType == "BOT_PROGRAMMING"]
        top = max(f, key=lambda x: x.points)
        return IValue(
            value=f"{top.ranking}/{top.totalPlayers}", 
            color=get_color(top.points, thresholds, ascending=True),
            title="Highest Compet.",
            icon=constants.SVG_HIGHEST_COMP,
            from_CG=False
        )


def get_global_score(level_value: IValue,
                     certif_value: list[IValue],
                     top_language_value: IValue,
                     puzzle_solved_value: IValue,
                     achievements_value: IValue,
                     rank_value: IValue,
                     comp_value: IValue
                     ) -> float:
    color_point = {
        constants.COLOR_WOOD: 0, 
        constants.COLOR_BRONZE: 1, 
        constants.COLOR_SILVER: 2, 
        constants.COLOR_GOLD: 3, 
        constants.COLOR_LEGEND: 4
    }
    weigths: tuple[IValue, int] = [
        (level_value, 50),
        (certif_value, 10),
        (top_language_value, 2),
        (puzzle_solved_value, 5),
        (achievements_value, 20),
        (rank_value, 100),
        (comp_value, 50),
    ]

    points = 0
    max_points = 0
    for value, weight in weigths:
        if isinstance(value, list):
            for element in value:
                points += weight * color_point[element.color]
            max_points += color_point[constants.COLOR_LEGEND] * weight * 5  # there is 5 certifications
        else:
            points += weight * color_point[value.color]
            max_points += color_point[constants.COLOR_LEGEND] * weight

    return 100 * points / max_points


def get_main_level(*args) -> tuple[str, str, str]:
    outputs = ["C", "B", "A", "S", "S+", "S++"]
    thresholds = [25, 50, 75, 85, 95]

    score = get_global_score(*args)

    main_color = get_color(score, thresholds[:4], ascending=True)
    back_color = constants.BACK_COLOR[main_color]
    label = _bind_value_to_range(score, thresholds, outputs)
    return (main_color, back_color, score, label)
