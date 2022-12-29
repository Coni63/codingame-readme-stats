from config import constants

from domain.i_data import IDataDto
from domain.i_profile import IProfileDto, IValue
from domain.i_language import ILanguageDto
from domain.i_achievement import IAchievementDto
from domain.i_certification import ICertificationDto
from domain.i_user_info import IUserDto

from infrastructure.codingame_api import get_points_from_rank


def evaluate(data: IDataDto) -> IProfileDto:  # pragma: no cover 
    (active_color, passive_color, score, label) = get_main_level(data)

    level_value = get_score_level(data.user)
    certif_value = get_score_certificate(data.certifications)
    top_language_value = get_score_best_language(data.languages)
    puzzle_solved_value = get_score_total_solved(data.languages)
    achievements_value = get_score_achievements(data.achievements)
    rank_value = get_score_rank(data.user)
    comp_value = get_score_competition(data.rankings, online=True)

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


def get_global_label(score: float) -> str:
    return "S"


def get_color_level(level: int) -> str:
    if level <= 8:
        return constants.COLOR_WOOD
    elif level <= 15:
        return constants.COLOR_BRONZE
    elif level <= 25:
        return constants.COLOR_SILVER
    elif level <= 35:
        return constants.COLOR_GOLD
    else:
        return constants.COLOR_LEGEND


def get_color_from_string(string: str) -> str:
    mapping = {
        "WOOD": constants.COLOR_WOOD,
        "BRONZE": constants.COLOR_BRONZE,
        "SILVER": constants.COLOR_SILVER,
        "GOLD": constants.COLOR_GOLD,
        "LEGEND": constants.COLOR_LEGEND,
    }
    return mapping.get(string, constants.COLOR_WOOD)


def get_color_language(puzzle_solved: int) -> str:
    if puzzle_solved <= 10:
        return constants.COLOR_WOOD
    elif puzzle_solved <= 25:
        return constants.COLOR_BRONZE
    elif puzzle_solved <= 50:
        return constants.COLOR_SILVER
    elif puzzle_solved <= 100:
        return constants.COLOR_GOLD
    else:
        return constants.COLOR_LEGEND


def get_color_total_solved(puzzle_solved: int) -> str:
    if puzzle_solved <= 25:
        return constants.COLOR_WOOD
    elif puzzle_solved <= 50:
        return constants.COLOR_BRONZE
    elif puzzle_solved <= 125:
        return constants.COLOR_SILVER
    elif puzzle_solved <= 250:
        return constants.COLOR_GOLD
    else:
        return constants.COLOR_LEGEND


def get_color_achievements(rate: float) -> str:
    if rate <= 0.25:
        return constants.COLOR_WOOD
    elif rate <= 0.50:
        return constants.COLOR_BRONZE
    elif rate <= 0.70:
        return constants.COLOR_SILVER
    elif rate <= 0.85:
        return constants.COLOR_GOLD
    else:
        return constants.COLOR_LEGEND


def get_color_rank(rate: float) -> str:
    if rate <= 0.0025:
        return constants.COLOR_LEGEND
    elif rate <= 0.0075:
        return constants.COLOR_GOLD
    elif rate <= 0.0225:
        return constants.COLOR_SILVER
    if rate <= 0.0675:
        return constants.COLOR_BRONZE
    else:
        return constants.COLOR_WOOD


def get_color_competition(rate: float) -> str:
    if rate <= 100:
        return constants.COLOR_WOOD
    elif rate <= 750:
        return constants.COLOR_BRONZE
    elif rate <= 1500:
        return constants.COLOR_SILVER
    elif rate <= 4000:
        return constants.COLOR_GOLD
    else:
        return constants.COLOR_LEGEND


##########################
# Fonctions to compute scores
##########################


def get_score_level(user: IUserDto) -> IValue:
    return IValue(
        value=user.codingamer.level,
        color=get_color_level(user.codingamer.level),
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
    top = max(languages, key=lambda x: x.puzzleCount)
    return IValue(
        value=top.languageName, 
        color=get_color_language(top.puzzleCount),
        title="Best Language",
        icon=constants.SVG_BEST_LANGUAGE,
        from_CG=False
    )


def get_score_total_solved(languages: list[ILanguageDto]) -> IValue:
    total = sum(x.puzzleCount for x in languages)
    return IValue(
        value=total, 
        color=get_color_total_solved(total),
        title="Puzzles Solved",
        icon=constants.SVG_PUZZLE_SOLVED,
        from_CG=False
    )


def get_score_achievements(achievements: list[IAchievementDto]) -> IValue:
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
        color=get_color_achievements(total_solved / total_available),
        title="Success",
        icon=constants.SVG_SUCCESS,
        from_CG=False
    )


def get_score_rank(user: IUserDto) -> IValue:
    rank = user.codingamer.rank
    last_rank = user.codingamePointsRankingDto.numberCodingamersGlobal

    return IValue(
        value=f"{rank}/{last_rank}", 
        color=get_color_rank(rank / last_rank),
        title="Global Rank",
        icon=constants.SVG_GLOBAL_RANK,
        from_CG=False
    )


def get_score_competition(rankings, online=False):
    if online:
        top = max(rankings.challenges, key=lambda x: x.points)

        points = get_points_from_rank(top.ranking, top.total)
        return IValue(
            value=f"{top.ranking}/{top.total}", 
            color=get_color_competition(points),
            title="Highest Compet.",
            icon=constants.SVG_HIGHEST_COMP,
            from_CG=False
        )
    else:
        f = [x for x in rankings.puzzles if x.puzzleType == "BOT_PROGRAMMING"]
        top = max(f, key=lambda x: x.points)
        return IValue(
            value=f"{top.ranking}/{top.totalPlayers}", 
            color=get_color_competition(top.points),
            title="Highest Compet.",
            icon=constants.SVG_HIGHEST_COMP,
            from_CG=False
        )


def get_main_level(data: IDataDto) -> tuple[str, str, str]:
    main_color = constants.COLOR_LEGEND
    back_color = constants.BACK_COLOR[main_color]
    score = 90
    return (main_color, back_color, score, get_global_label(score))
