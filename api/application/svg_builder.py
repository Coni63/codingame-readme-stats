import math

import cairo
from io import BytesIO

from config import constants
import base64 
import svgutils
from lxml import etree

from domain.i_profile import IProfileDto

##########################
# helpers
##########################

def get_scale(element, target_height=20):
    return target_height / int(element.height.replace("px", ""))

def hex_to_rgb(value):
    value = value.lstrip('#')
    r = value[:2]
    g = value[2:4]
    b = value[4:]
    return (int(r, 16)/255.0, int(g, 16)/255.0, int(b, 16)/255.0)

def get_height(n: int=1, padding: int=26, top_offset: int=45):
    return (n-1) * padding + top_offset

##########################
# Creation of geometries
##########################

def roundrect(context: cairo.Context, 
              x: int, y: int, width: int, height: int, r: int):
    context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    context.close_path()

def get_square(context: cairo.Context, x: int, y: int, bg_color: str):
    s = 24  # images are 20px x 20px and square is 24px x 24px
    context.set_source_rgb(*hex_to_rgb(bg_color))
    roundrect(context, x-2, y-2, s, s, 4)
    context.fill()

def set_text(context: cairo.Context, x: int, y: int, text: str, bg_color: str, font_size: int=12):
    offset_text = 0.5 * font_size + 10  # l'image fait 20px et le text fait font_size. Il faut donc shifter de font_size + (20 - font_size) / 2
    context.set_source_rgb(*hex_to_rgb(bg_color))
    context.select_font_face(constants.FONT_NAME, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(font_size)
    context.move_to(x, y + offset_text)
    context.show_text(text)
    context.stroke()

def draw_line(context: cairo.Context, x1: int, y1: int, x2: int, y2: int, color: str, line_width: int=5):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_width)
    context.move_to(x1, y1)
    context.line_to(x2, y2) 
    context.stroke()

def draw_borders(context: cairo.Context, color: str, line_width: int=5):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(line_width)
    roundrect(context, 0, 0, constants.SVG_width, constants.SVG_height, constants.SVG_border_radius)
    context.stroke()

##########################
# Work on svg files
##########################

def decode_svg(svg_encoded: str) -> str:
    encoded = svg_encoded.replace("data:image/svg+xml;base64,", "")
    return base64.b64decode(encoded).decode("utf-8") 

def place_icon(svg_encoded: str, x: int, y: int, line_color: str="#000000", from_CG: bool=True) -> svgutils.transform.SVGFigure:
    figure = svgutils.transform.fromstring(decode_svg(svg_encoded))
    svg_element = figure.getroot()
    svg_element.moveto(x, y, get_scale(figure))
    if from_CG:
        svg_element.root.getchildren()[0].getchildren()[0].set("fill", line_color)
    else:
        svg_element.root.getchildren()[0].set("fill", line_color)
    return svg_element

##########################
# Fonctions to generate the svg figure
##########################

def get_title(context: cairo.Context, text: str, x: int, y: int, font_color: str, font_size_big: int=35, font_size_small: int=25):
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

def create_pie(context: cairo.Context, x: int, y: int, radius: int, score: int, active_color: str, passive_color: str, label: str, font_size_big: int=35):
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

def render(data: IProfileDto):
    f = BytesIO()

    s = "{title}:{ranking}"
    c1 = 160  # x position of the first section
    c2 = 410  # x position of the second section

    with cairo.SVGSurface(f, constants.SVG_width, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        draw_borders(context, data.active_color)

        get_title(context, data.username, 20, 35, font_color=data.active_color)
        
        # pie with score & note
        y_pie = 35 + (constants.SVG_height - 35) // 2
        create_pie(context, 80, y_pie, 50, data.score, active_color=data.active_color, passive_color=data.passive_color, label=data.main_rank)

        # DRAW SEPARATORS
        draw_line(context, c1, 55, c1, constants.SVG_height-20, data.active_color)

        # SQUARE BACKGROUND FOR STATS SVG
        get_square(context, c1+30, get_height(1), data.rank.color)
        get_square(context, c1+30, get_height(2), data.puzzle_solved.color)
        get_square(context, c1+30, get_height(3), data.level.color)
        get_square(context, c1+30, get_height(4), data.achievements.color)
        get_square(context, c1+30, get_height(5), data.language.color)
        get_square(context, c1+30, get_height(6), data.competition.color)

        # LABEL STATS
        set_text(context, c1+60, get_height(1), s.format(title="Global Rank",     ranking=data.rank.value), data.rank.color)
        set_text(context, c1+60, get_height(2), s.format(title="Puzzle Solved",   ranking=data.puzzle_solved.value) , data.puzzle_solved.color)
        set_text(context, c1+60, get_height(3), s.format(title="Level",           ranking=data.level.value), data.level.color)
        set_text(context, c1+60, get_height(4), s.format(title="Success",         ranking=data.achievements.value), data.achievements.color)
        set_text(context, c1+60, get_height(5), s.format(title="Best Language",   ranking=data.language.value), data.language.color)
        set_text(context, c1+60, get_height(6), s.format(title="Highest Compet.", ranking=data.competition.value), data.competition.color)

        # DRAW SEPARATORS
        draw_line(context, c2, 55, c2, constants.SVG_height-20, constants.COLOR_LEGEND)

        # SQUARE BACKGROUND FOR CERTIFS SVG
        get_square(context, c2+30, get_height(1.5), data.certifications[0].color)
        get_square(context, c2+30, get_height(2.5), data.certifications[1].color)
        get_square(context, c2+30, get_height(3.5), data.certifications[2].color)
        get_square(context, c2+30, get_height(4.5), data.certifications[3].color)
        get_square(context, c2+30, get_height(5.5), data.certifications[4].color)

        # LABEL CERTIFS
        set_text(context, c2+60, get_height(1.5), s.format(title="Collaboration", ranking=data.certifications[0].value), data.certifications[0].color)
        set_text(context, c2+60, get_height(2.5), s.format(title="Algorithmes",   ranking=data.certifications[1].value), data.certifications[1].color)
        set_text(context, c2+60, get_height(3.5), s.format(title="Optimization",  ranking=data.certifications[2].value), data.certifications[2].color)
        set_text(context, c2+60, get_height(4.5), s.format(title="Coding Speed",  ranking=data.certifications[3].value), data.certifications[3].color)
        set_text(context, c2+60, get_height(5.5), s.format(title="AI",            ranking=data.certifications[4].value), data.certifications[4].color)

    # the card is the component having nearly everything except external icons from CG
    card = etree.XML(f.getvalue())

    # load icons for stats
    SVG_GLOBAL_RANK   = place_icon(constants.SVG_GLOBAL_RANK,     c1+30, get_height(1), from_CG=False)
    SVG_PUZZLE_SOLVED = place_icon(constants.SVG_PUZZLE_SOLVED,   c1+30, get_height(2), from_CG=False)
    SVG_LEVEL         = place_icon(constants.SVG_LEVEL,           c1+30, get_height(3), from_CG=False)
    SVG_SUCCESS       = place_icon(constants.SVG_SUCCESS,         c1+30, get_height(4), from_CG=False)
    SVG_BEST_LANGUAGE = place_icon(constants.SVG_BEST_LANGUAGE,   c1+30, get_height(5), from_CG=False)
    SVG_HIGHEST_COMP  = place_icon(constants.SVG_HIGHEST_COMP,    c1+30, get_height(6), from_CG=False)

    # load icons from constants (extracted from CG)
    SVG_collaboration = place_icon(constants.SVG_collaboration, c2+30, get_height(1.5), from_CG=True)
    SVG_algorithmes   = place_icon(constants.SVG_algorithmes,   c2+30, get_height(2.5), from_CG=True)
    SVG_optimization  = place_icon(constants.SVG_optimization,  c2+30, get_height(3.5), from_CG=True)
    SVG_speed         = place_icon(constants.SVG_speed,         c2+30, get_height(4.5), from_CG=True)
    SVG_AI            = place_icon(constants.SVG_AI,            c2+30, get_height(5.5), from_CG=True)


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