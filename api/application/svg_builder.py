from __future__ import annotations

import math
import re
import cairo
import base64 
import svgutils

from io import BytesIO
from lxml import etree

from config import constants
from domain import IProfileDto, IValue

##########################
# helpers
##########################


def human_format(num: int) -> str:
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'm'][magnitude])


def get_scale(element_height: int | str, target_height: int = 20) -> float:
    if not isinstance(element_height, str) and not isinstance(element_height, int):
        raise ValueError("invalid element_height")

    if isinstance(element_height, str):
        element_height = int(element_height.replace("px", ""))
    return target_height / element_height


def hex_to_rgb(value: str):
    if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
        raise ValueError("Invalid error, format must be #FF0000")

    value = value.lstrip('#')
    r = value[:2]
    g = value[2:4]
    b = value[4:]
    return (int(r, 16) / 255.0, int(g, 16) / 255.0, int(b, 16) / 255.0)


def get_height(n: int = 1):  # pragma: no cover
    return (n - 1) * constants.TEXT_PADDING + constants.Y_TOP


##########################
# Creation of geometries
##########################


def roundrect(context: cairo.Context, 
              x: int, y: int, width: int, height: int, r: int):   # pragma: no cover 
    context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    context.close_path()


def get_square(context: cairo.Context, x: int, y: int, bg_color: str):  # pragma: no cover 
    s = 24  # images are 20px x 20px and square is 24px x 24px
    context.set_source_rgb(*hex_to_rgb(bg_color))
    roundrect(context, x-2, y-2, s, s, 4)
    context.fill()


def set_text(context: cairo.Context, 
             x: int, y: int, text: str, 
             font_color: str, font_size: int):  # pragma: no cover

    context.set_source_rgb(*hex_to_rgb(font_color))
    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(font_size)
    context.move_to(x, y)
    context.show_text(text)
    context.stroke()

    xbearing, ybearing, width, height, xadvance, yadvance = context.text_extents(text)
    return width


def draw_line(context: cairo.Context,
              x1: int, y1: int, x2: int, y2: int,
              color: str, line_width: int=5):  # pragma: no cover
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_width)
    context.move_to(x1, y1)
    context.line_to(x2, y2) 
    context.stroke()


def draw_borders(context: cairo.Context, width, height, color: str, line_thk: int=5, night=True):  # pragma: no cover
    roundrect(context, 0, 0, width, height, constants.SVG_border_radius)
    if night:
        context.set_source_rgb(*hex_to_rgb(constants.COLOR_BG_CG))
        context.fill_preserve()

    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_thk)
    roundrect(context, 0, 0, width, height, constants.SVG_border_radius)
    context.stroke()


##########################
# Work on svg files
##########################


def decode_svg(svg_encoded: str) -> str:  # pragma: no cover
    encoded = svg_encoded.replace("data:image/svg+xml;base64,", "")
    return base64.b64decode(encoded).decode("utf-8") 


def place_icon(svg_encoded: str, x: int, y: int,
               line_color: str = "none", from_CG: bool=True) -> svgutils.transform.SVGFigure:  # pragma: no cover
    figure = svgutils.transform.fromstring(decode_svg(svg_encoded))
    svg_element = figure.getroot()
    svg_element.moveto(x, y, get_scale(figure.height))
    if from_CG:
        svg_element.root.getchildren()[0].getchildren()[0].set("fill", line_color)
    else:
        svg_element.root.getchildren()[0].set("fill", line_color)
    return svg_element


##########################
# Fonctions to generate the svg figure
##########################

def add_CG_logo(img_width: int, night: bool=False):
    if night:
        return place_icon(constants.SVG_CG_NIGHT, img_width-160, 10, "none", False),  # icon CG
    else:
        return place_icon(constants.SVG_CG, img_width-160, 10, "none", False),  # icon CG


def get_title(context: cairo.Context, text: str, x: int, y: int, font_color: str):  # pragma: no cover
    w1 = set_text(context, x, y, text, font_color=font_color, font_size=constants.TITLE_FONT_SIZE)
    set_text(context, x + w1 + 2, y, "'s profile", font_color=font_color, font_size=constants.LARGE_FONT_SIZE)


def create_pie(context: cairo.Context, x: int, y: int, radius: int, score: int,
               active_color: str, passive_color: str, label: str):  # pragma: no cover
    start_angle = 3*math.pi/2
    end_angle = 3*math.pi/2 + 2*math.pi*score/100

    context.set_source_rgb(*hex_to_rgb(passive_color))
    context.set_line_width(10)
    context.set_line_cap(cairo.LINE_CAP_BUTT)
    context.arc(x, y, radius, end_angle, start_angle)  # cx, cy, radius, angle_start, angle_end
    context.stroke()

    context.set_source_rgb(*hex_to_rgb(active_color))
    context.set_line_width(12)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.arc(x, y, radius, start_angle, end_angle)  # cx, cy, radius, angle_start, angle_end
    context.stroke()

    context.set_source_rgb(*hex_to_rgb(active_color))
    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(constants.TITLE_FONT_SIZE)

    # center the text within the circle
    (x_, y_, width, height, dx, dy) = context.text_extents(label)
    context.move_to(x - width/2, y + height/2)    
    context.show_text(label)
    context.stroke()


def add_row(context: cairo.Context, x_start: int, y: int, data: IValue, percent: bool=False, line_color="#000000"):  # pragma: no cover 
    get_square(context, x_start + constants.PADDING, y, data.color)

    # the image is 20px height and the text is font_size. So the shift is font_size + (20 - font_size) / 2
    offset_text = 0.5 * constants.NORMAL_FONT_SIZE + 10  
    text_start = x_start + constants.ICON_SIZE + 2 * constants.PADDING

    w1 = set_text(context, text_start, y + offset_text, f"{data.title}:",
                  font_color=data.color, font_size=constants.NORMAL_FONT_SIZE)
    if data.numerator:
        w2 = set_text(context, text_start + w1 + 2, y + offset_text, f"{human_format(data.numerator)}", 
                      font_color=data.color, font_size=constants.NORMAL_FONT_SIZE)
        w3 = set_text(context, text_start + w1 + w2 + 2, y + offset_text + 2, f"/{human_format(data.denominator)}", 
                      font_color=data.color, font_size=constants.SMALL_FONT_SIZE)
        if percent and data.numerator > 0:
            w3 = set_text(context, text_start + w1 + w2 + w3 + 4, y + offset_text, f"(Top {data.percent_rank}%)", 
                      font_color=data.color, font_size=constants.NORMAL_FONT_SIZE)
    elif data.numerator == 0:
        set_text(context, text_start + w1 + 2, y + offset_text, "N/A",
                 font_color=data.color, font_size=constants.NORMAL_FONT_SIZE)
    else:
        set_text(context, text_start + w1 + 2, y + offset_text, f"{data.value}",
                 font_color=data.color, font_size=constants.NORMAL_FONT_SIZE)
    return place_icon(data.icon, x_start + constants.PADDING, y, from_CG=data.from_CG, line_color=line_color)


def render_puzzle_stats(context: cairo.Context, start_x: int, data: IProfileDto):  # pragma: no cover 
    # add text with relevant icons -- part from global stats
    SVG_PUZZLE_SOLVED = add_row(context, start_x, get_height(1), data.puzzle_solved)
    SVG_LEVEL         = add_row(context, start_x, get_height(2), data.level)
    SVG_SUCCESS       = add_row(context, start_x, get_height(3), data.achievements)
    SVG_BEST_LANGUAGE = add_row(context, start_x, get_height(4), data.language)
    SVG_HIGHEST_COMP  = add_row(context, start_x, get_height(5), data.competition)
    SVG_HIGHEST_BOT   = add_row(context, start_x, get_height(6), data.bot_battle)

    return [SVG_PUZZLE_SOLVED, SVG_LEVEL, SVG_SUCCESS, SVG_BEST_LANGUAGE, SVG_HIGHEST_COMP, SVG_HIGHEST_BOT]


def render_certifications(context: cairo.Context, start_x: int, data: list[IValue]):  # pragma: no cover 
    # add text with relevant icons -- part from certifications
    SVG_collaboration = add_row(context, start_x, get_height(1.5), data[0])
    SVG_algorithmes   = add_row(context, start_x, get_height(2.5), data[1])
    SVG_optimization  = add_row(context, start_x, get_height(3.5), data[2])
    SVG_speed         = add_row(context, start_x, get_height(4.5), data[3])
    SVG_AI            = add_row(context, start_x, get_height(5.5), data[4])

    return [SVG_collaboration, SVG_algorithmes, SVG_optimization, SVG_speed, SVG_AI]


def render_leaderboard(context: cairo.Context, start_x: int, data: list[IValue], percent: bool = False):  # pragma: no cover 
    # add text with relevant icons -- part from certifications
    SVG_global     = add_row(context, start_x, get_height(1), data[0], percent=percent)
    SVG_contest    = add_row(context, start_x, get_height(2), data[1], percent=percent)
    SVG_ai_battle  = add_row(context, start_x, get_height(3), data[2], percent=percent, line_color="none")
    SVG_optim      = add_row(context, start_x, get_height(4), data[3], percent=percent)
    SVG_clash      = add_row(context, start_x, get_height(5), data[4], percent=percent)
    SVG_codegolf   = add_row(context, start_x, get_height(6), data[5], percent=percent, line_color="none")

    return [SVG_contest, SVG_ai_battle, SVG_optim, SVG_clash, SVG_codegolf, SVG_global]


def render_language(context: cairo.Context, start_x: int, data: list[IValue], limit: int = 6):  # pragma: no cover 
    new_objects = []
    # add text with relevant icons -- part from top languages
    subset = data[:limit]  # if there is less than the requested number, no issue
    num_elems = len(subset)
    offset = 4 - 0.5 * num_elems
    for i, language in enumerate(subset):
        svg = add_row(context, start_x, get_height(i + offset), language)
        new_objects.append(svg)

    return new_objects


def render_category(context: cairo.Context, start_x: int, category: str, data: IProfileDto, language_number=6, percent: bool=False):
    if category is None:
        return []

    draw_line(context, 
              start_x, 
              get_height(1.5),
              start_x, 
              get_height(6.5), 
              data.active_color)

    if category == "certifications":
        return render_certifications(context, start_x, data.certifications)
    elif category == "languages":
        return render_language(context, start_x, data.lang_list, language_number)
    elif category == "leaderboard":
        return render_leaderboard(context, start_x, data.leaderboard, percent)
    elif category == "puzzles":
        return render_puzzle_stats(context, start_x, data)

    return []


def render(data: IProfileDto, 
           first_category: str = "leaderboard",
           second_category: str = None, 
           third_category: str = None, 
           language_number: int = 6,
           percent: bool = False,
           night: bool = False) -> str:  # pragma: no cover

    f = BytesIO()

    if second_category is None:
        width_img = constants.SVG_width_simple
    elif third_category is None:
        width_img = constants.SVG_width_double
    else:
        width_img = constants.SVG_width_triple
    
    x_section2 = constants.X_SECTION1 + constants.SPACE_BAR
    x_section3 = x_section2 + constants.SPACE_BAR
    
    show_percent = percent and "leaderboard" in [first_category,
                                                 second_category,
                                                 third_category]
    
    if show_percent:
        width_img += constants.PERCENT_SIZE
        if "leaderboard" in [first_category, second_category]:
            x_section3 += constants.PERCENT_SIZE
            if "leaderboard" == first_category:
                x_section2 += constants.PERCENT_SIZE

    with cairo.SVGSurface(f, width_img, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        draw_borders(context, width_img, constants.SVG_height, data.active_color, night=night)

        get_title(context, data.username, x=20, y=35, font_color=data.active_color)

        # pie with score & note
        create_pie(context, constants.X_PIE, get_height(4), constants.RADIUS_PIE, data.score, active_color=data.active_color,
                   passive_color=data.passive_color, label=data.main_rank)

        list_other_svg = [*add_CG_logo(width_img, night=night)]
        list_other_svg += render_category(context, constants.X_SECTION1, first_category, data, language_number, percent)
        list_other_svg += render_category(context, x_section2, second_category, data, language_number, percent)
        list_other_svg += render_category(context, x_section3, third_category, data, language_number, percent)

        # Setting SVG unit
        surface.set_document_unit(3)  # https://www.geeksforgeeks.org/pycairo-how-to-set-svg-unit/

    all_elements = [
        etree.XML(f.getvalue()),  # main card that we merge with external icons
        *list_other_svg
    ]

    # merge all svg in one
    fig = svgutils.transform.SVGFigure()
    fig.set_size((f"{width_img}px", f"{constants.SVG_height}px"))
    fig.root.set("id", "cg-readme-stats-user-details")
    fig.root.set("role", "presentation")
    fig.root.set("viewBox", f"0 0 {width_img} {constants.SVG_height}")  
    fig.append(all_elements)
    return fig.to_str()
