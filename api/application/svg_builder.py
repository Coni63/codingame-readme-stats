import math

import cairo
from io import BytesIO, StringIO

from config import constants
import base64 
import svgutils
from lxml import etree

from application import leveler

def roundrect(context, x, y, width, height, r):
    context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    context.close_path()

def decode_svg(svg_encoded):
    encoded = svg_encoded.replace("data:image/svg+xml;base64,", "")
    return base64.b64decode(encoded).decode("utf-8") 

def place_icon_from_CG(svg_encoded, x, y, line_color="#000000"):
    figure = svgutils.transform.fromstring(decode_svg(svg_encoded))
    svg_element: svgutils.transform.SVGFigure = figure.getroot()
    svg_element.moveto(x, y, get_scale(figure))
    svg_element.root.getchildren()[0].getchildren()[0].set("fill", line_color)
    return svg_element

def place_other_icon(svg_encoded, x, y, line_color="#000000"):
    figure = svgutils.transform.fromstring(decode_svg(svg_encoded))
    svg_element: svgutils.transform.SVGFigure = figure.getroot()
    svg_element.moveto(x, y, get_scale(figure))
    svg_element.root.getchildren()[0].set("fill", line_color)
    return svg_element

def get_square(context, x, y, bg_color):
    s = 24  # images are 20px x 20px and square is 24px x 24px
    context.set_source_rgb(*hex_to_rgb(bg_color))
    roundrect(context, x-2, y-2, s, s, 4)
    context.fill()

def set_text(context, x, y, text, bg_color, font_size=12):
    offset_text = 0.5 * font_size + 10  # l'image fait 20px et le text fait font_size. Il faut donc shifter de font_size + (20 - font_size) / 2
    context.set_source_rgb(*hex_to_rgb(bg_color))
    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(font_size)
    context.move_to(x, y + offset_text)
    context.show_text(text)
    context.stroke()

def draw_line(context, x1, y1, x2, y2, color, line_width=5):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_width)
    context.move_to(x1, y1)
    context.line_to(x2, y2) 
    context.stroke()

def draw_borders(context, color, line_width=5):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_width)
    roundrect(context, 0, 0, constants.SVG_width, constants.SVG_height, constants.SVG_border_radius)
    context.stroke()

def get_title(context, text, x, y, font_color, font_size_big=35, font_size_small=25):
    color = hex_to_rgb(font_color)
    context.set_source_rgb(*color)
    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(font_size_big)
    context.move_to(x, y)
    context.show_text(text)
    xbearing, ybearing, width, height, xadvance, yadvance = context.text_extents(text)

    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size_small)
    context.move_to(x + width + 2, y)
    context.show_text("'s profile")

    context.stroke()

def get_scale(element, target_height=20):
    return target_height / int(element.height.replace("px", ""))

def hex_to_rgb(value):
    value = value.lstrip('#')
    r = value[:2]
    g = value[2:4]
    b = value[4:]
    return (int(r, 16)/255.0, int(g, 16)/255.0, int(b, 16)/255.0)

def create_pie(context, x, y, radius, score, active_color, passive_color, label, font_size_big=35):
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
    context.set_font_size(font_size_big)

    # center the text within the circle
    (x_, y_, width, height, dx, dy) = context.text_extents(label)
    context.move_to(x - width/2, y + height/2)    
    context.show_text(label)
    context.stroke()

def get_height(n = 1, padding=26, top_offset=45):
    return (n-1) * padding + top_offset

def render(data):
    username = data.user.codingamer.pseudo

    level = data.user.codingamer.level
    color_level = leveler.get_color_level(level)

    certif = leveler.get_color_certificate(data.certifications, order=['COLLABORATION', 'ALGORITHMS', 'OPTIMIZATION', 'CODING_SPEED', 'AI'])

    language, color_language = leveler.get_best_language(data.languages)
    total_solved, color_total_solved = leveler.get_total_solved(data.languages)

    (count_solved, count_available), color_achivements = leveler.get_score_achievements(data.achievements)

    (user_rank, last_rank), color_user_rank = leveler.get_score_rank(data.user)

    (best_comp_rank, total_comp_player), color_competition = leveler.get_score_competition(data.rankings, online=True)

    (active_color, passive_color, label) = leveler.get_main_level(data)

    f = BytesIO()

    s = "{title}:{ranking}"
    c1 = 160  # x position of the first section
    c2 = 410  # x position of the second section

    with cairo.SVGSurface(f, constants.SVG_width, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        draw_borders(context, active_color)

        get_title(context, username, 20, 35, font_color=active_color)
        
        # pie with score & note
        y_pie = 35 + (constants.SVG_height - 35) // 2
        create_pie(context, 80, y_pie, 50, 65, active_color=active_color, passive_color=passive_color, label=label)

        # DRAW SEPARATORS
        draw_line(context, c1, 55, c1, constants.SVG_height-20, active_color)

        # SQUARE BACKGROUND FOR STATS SVG
        get_square(context, c1+30, get_height(1), color_user_rank)
        get_square(context, c1+30, get_height(2), color_total_solved)
        get_square(context, c1+30, get_height(3), color_level)
        get_square(context, c1+30, get_height(4), color_achivements)
        get_square(context, c1+30, get_height(5), color_language)
        get_square(context, c1+30, get_height(6), color_competition)

        # LABEL STATS
        set_text(context, c1+60, get_height(1), s.format(title="Global Rank",     ranking=f"{user_rank}/{last_rank}"), color_user_rank)
        set_text(context, c1+60, get_height(2), s.format(title="Puzzle Solved",   ranking=total_solved) , color_total_solved)
        set_text(context, c1+60, get_height(3), s.format(title="Level",           ranking=level)        , color_level)
        set_text(context, c1+60, get_height(4), s.format(title="Success",         ranking=f"{count_solved}/{count_available}"), color_achivements)
        set_text(context, c1+60, get_height(5), s.format(title="Best Language",   ranking=language)     , color_language)
        set_text(context, c1+60, get_height(6), s.format(title="Highest Compet.", ranking=f"{best_comp_rank}/{total_comp_player}") , color_competition)

        # DRAW SEPARATORS
        draw_line(context, c2, 55, c2, constants.SVG_height-20, constants.COLOR_LEGEND)

        # SQUARE BACKGROUND FOR CERTIFS SVG
        get_square(context, c2+30, get_height(1.5), certif[0][1])
        get_square(context, c2+30, get_height(2.5), certif[1][1])
        get_square(context, c2+30, get_height(3.5), certif[2][1])
        get_square(context, c2+30, get_height(4.5), certif[3][1])
        get_square(context, c2+30, get_height(5.5), certif[4][1])

        # LABEL CERTIFS
        set_text(context, c2+60, get_height(1.5), s.format(title="Collaboration", ranking=certif[0][0]), certif[0][1])
        set_text(context, c2+60, get_height(2.5), s.format(title="Algorithmes",   ranking=certif[1][0]), certif[1][1])
        set_text(context, c2+60, get_height(3.5), s.format(title="Optimization",  ranking=certif[2][0]), certif[2][1])
        set_text(context, c2+60, get_height(4.5), s.format(title="Coding Speed",  ranking=certif[3][0]), certif[3][1])
        set_text(context, c2+60, get_height(5.5), s.format(title="AI",            ranking=certif[4][0]), certif[4][1])

        # getting all the svg versions available
        versions = surface.get_versions()

    # the card is the component having nearly everything except external icons from CG
    card = etree.XML(f.getvalue())

    # load icons for stats
    SVG_GLOBAL_RANK   = place_other_icon(constants.SVG_GLOBAL_RANK,   c1+30, get_height(1))
    SVG_PUZZLE_SOLVED = place_other_icon(constants.SVG_PUZZLE_SOLVED, c1+30, get_height(2))
    SVG_LEVEL         = place_other_icon(constants.SVG_LEVEL,         c1+30, get_height(3))
    SVG_SUCCESS       = place_other_icon(constants.SVG_SUCCESS,       c1+30, get_height(4))
    SVG_BEST_LANGUAGE = place_other_icon(constants.SVG_BEST_LANGUAGE, c1+30, get_height(5))
    SVG_HIGHEST_COMP  = place_other_icon(constants.SVG_HIGHEST_COMP,  c1+30, get_height(6))

    # load icons from constants (extracted from CG)
    SVG_collaboration = place_icon_from_CG(constants.SVG_collaboration, c2+30, get_height(1.5))
    SVG_algorithmes   = place_icon_from_CG(constants.SVG_algorithmes,   c2+30, get_height(2.5))
    SVG_optimization  = place_icon_from_CG(constants.SVG_optimization,  c2+30, get_height(3.5))
    SVG_speed         = place_icon_from_CG(constants.SVG_speed,         c2+30, get_height(4.5))
    SVG_AI            = place_icon_from_CG(constants.SVG_AI,            c2+30, get_height(5.5))


    all_elements = [
        card, 
        SVG_collaboration, 
        SVG_algorithmes, 
        SVG_optimization, 
        SVG_speed, 
        SVG_AI, 
        SVG_GLOBAL_RANK,
        SVG_PUZZLE_SOLVED,
        SVG_LEVEL,
        SVG_SUCCESS,
        SVG_BEST_LANGUAGE,
        SVG_HIGHEST_COMP
    ]

    # merge all svg in one
    fig = svgutils.transform.SVGFigure()
    fig.set_size(("{constants.SVG_width}px", "{constants.SVG_height}px"))
    fig.append(all_elements)
    return fig.to_str()


# https://www.geeksforgeeks.org/pycairo-drawing-different-type-of-line-caps/?ref=rp
# https://pycairo.readthedocs.io/en/latest/reference/enums.html

# "Open Sans",Lato,sans-serif