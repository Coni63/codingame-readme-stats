from config import constants




def get_global_rank(score):
    return "S"


def get_color_level(level):
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

def get_color_from_string(string):
    if string == "WOOD":
        return constants.COLOR_WOOD
    elif string == "BRONZE":
        return constants.COLOR_BRONZE
    elif string == "SILVER":
        return constants.COLOR_SILVER
    elif string == "GOLD":
        return constants.COLOR_GOLD
    elif string == "LEGEND":
        return constants.COLOR_LEGEND
    else:
        return constants.COLOR_WOOD

def get_color_language(puzzle_solved):
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

def get_color_total_solved(puzzle_solved):
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

def get_color_certificate(certifications, order):
    ans = [("WOOD", constants.COLOR_WOOD) for _ in range(len(order))]
    for certification in certifications:
        idx = order.index(certification.category)
        level = certification.level
        ans[idx] = (level, get_color_from_string(level))
    return ans

def get_best_language(languages):
    top = max(languages, key=lambda x:x.puzzleCount)
    return top.languageName, get_color_language(top.puzzleCount)


def get_total_solved(languages):
    total = sum(x.puzzleCount for x in languages)
    return total, get_color_total_solved(total)

def get_color_achievements(rate):
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

def get_score_achievements(achievements):
    skip = ["coder", "social"]
    total_solved = 0
    total_available = 0
    count_solved  = 0
    count_available = 0
    for achievement in achievements:
        if achievement.categoryId in skip:
            continue

        if achievement.completionTime > 0:
            total_solved += achievement.weight
            count_solved += 1

        total_available += achievement.weight
        count_available += 1
    return (count_solved, count_available), get_color_achievements(total_solved / total_available)

def get_color_rank(rate):
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

def get_score_rank(user):
    rank = user.codingamer.rank
    last_rank = user.codingamePointsRankingDto.numberCodingamersGlobal

    return (rank, last_rank), get_color_rank(rank / last_rank)