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