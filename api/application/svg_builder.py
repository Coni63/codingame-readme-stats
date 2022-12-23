import math

import cairo
from io import BytesIO, StringIO

from config import constants
import base64 
import svgutils
from lxml import etree

def roundrect(context, x, y, width, height, r):
    context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    context.close_path()

def decode_svg(svg_encoded):
    encoded = svg_encoded.replace("data:image/svg+xml;base64,", "")
    return base64.b64decode(encoded).decode("utf-8") 

def place_icon(svg_encoded, nth_position=1, line_color="#000000"):
    svg_element: svgutils.transform.SVGFigure = svgutils.transform.fromstring(decode_svg(svg_encoded)).getroot()
    svg_element.moveto(*get_position(nth_position), get_scale())
    svg_element.root.getchildren()[0].getchildren()[0].set("fill", line_color)
    return svg_element

def place_icon2(svg_encoded, nth_position=1, line_color="#000000"):
    svg_element: svgutils.transform.SVGFigure = svgutils.transform.fromstring(decode_svg(svg_encoded)).getroot()
    svg_element.moveto(*get_position2(nth_position), get_scale()*0.5)
    svg_element.root.getchildren()[0].set("fill", line_color)
    return svg_element

def get_square(context, nth_position, bg_color):
    s = get_scale() * 29
    color = hex_to_rgb(bg_color)
    context.set_source_rgb(*color)
    # context.rectangle(*get_position(nth_position), s, s)  # x, y, width, height
    roundrect(context, *get_position(nth_position), s, s, 5)
    context.fill()

def get_square2(context, nth_position, bg_color):
    s = get_scale() * 29
    color = hex_to_rgb(bg_color)
    context.set_source_rgb(*color)
    # context.rectangle(*get_position(nth_position), s, s)  # x, y, width, height
    roundrect(context, *get_position2(nth_position), s, s, 5)
    context.fill()

def get_certif_label(context, nth_position, text, bg_color):
    position = get_position(nth_position)
    color = hex_to_rgb(bg_color)
    context.set_source_rgb(*color)
    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(13)
    context.move_to(190, position[1]+15)
    context.show_text(text)
    context.stroke()

def get_stats_label(context, nth_position, text, bg_color):
    position = get_position(nth_position)
    color = hex_to_rgb(bg_color)
    context.set_source_rgb(*color)
    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(13)
    context.move_to(390, position[1]+15)
    context.show_text(text)
    context.stroke()

def draw_line(context, x1, y1, x2, y2, color):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(5)
    context.move_to(x1, y1)
    context.line_to(x2, y2) 
    context.stroke()

def draw_borders(context, color):
    context.set_source_rgb(*hex_to_rgb(color))
    context.set_line_width(5)
    # context.rectangle(0, 0, constants.SVG_width, constants.SVG_height)  # x, y, width, height
    roundrect(context, 0, 0, constants.SVG_width, constants.SVG_height, 20)
    context.stroke()

def get_title(context, text, font_color):
    color = hex_to_rgb(font_color)
    context.set_source_rgb(*color)
    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(35)
    context.move_to(20, 35)
    context.show_text(text)
    xbearing, ybearing, width, height, xadvance, yadvance = context.text_extents(text)

    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(25)
    context.move_to(20 + width + 2, 35)
    context.show_text("'s profile")

    context.stroke()

def get_position(n = 1):
    return (160, n * 25 + 20)

def get_position2(n = 1):
    return (365, n * 25 + 20)

def get_scale():
    return 0.66

def hex_to_rgb(value):
    value = value.lstrip('#')
    r = value[:2]
    g = value[2:4]
    b = value[4:]
    return (int(r, 16)/255.0, int(g, 16)/255.0, int(b, 16)/255.0)

def get_rank(score):
    return "A+"

def create_pie(context, score, font_color, background_color):
    start_angle = 3*math.pi/2
    end_angle = 3*math.pi/2 + 2*math.pi*score/100
    center = (80, 105)
    radius = 50

    context.set_source_rgb(*hex_to_rgb(background_color))
    context.set_line_width(10)
    context.set_line_cap(cairo.LINE_CAP_BUTT)
    context.arc(*center, radius,  end_angle, start_angle)  # cx, cy, radius, angle_start, angle_end
    context.stroke()

    context.set_source_rgb(*hex_to_rgb(font_color))
    context.set_line_width(12)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.arc(*center, radius, start_angle, end_angle)  # cx, cy, radius, angle_start, angle_end
    context.stroke()

    context.set_source_rgb(*hex_to_rgb(font_color))
        
    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(35)
    context.move_to(center[0]-18, center[1]+10)
    context.show_text(get_rank(score))
    context.stroke()

def render(data):
    f = BytesIO()

    with cairo.SVGSurface(f, constants.SVG_width, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        draw_borders(context, constants.COLOR_LEGEND)

        # pie with score & note
        create_pie(context, 65, font_color=constants.COLOR_LEGEND, background_color=constants.COLOR_SILVER)

        get_title(context, "username", font_color=constants.COLOR_LEGEND)

        # SQUARE BACKGROUND FOR CERTIFS
        get_square(context, 1.5, constants.COLOR_LEGEND)
        get_square(context, 2.5, constants.COLOR_GOLD)
        get_square(context, 3.5, constants.COLOR_SILVER)
        get_square(context, 4.5, constants.COLOR_BRONZE)
        get_square(context, 5.5, constants.COLOR_LEGEND)

        # 
        get_square2(context, 1, constants.COLOR_LEGEND)
        get_square2(context, 2, constants.COLOR_GOLD)
        get_square2(context, 3, constants.COLOR_SILVER)
        get_square2(context, 4, constants.COLOR_BRONZE)
        get_square2(context, 5, constants.COLOR_LEGEND)
        get_square2(context, 6, constants.COLOR_LEGEND)

        # LABEL CERTIFS
        s = "{title}:{ranking}"
        # get_certif_label(context, 1, "CERTIFICATIONS", constants.COLOR_LEGEND)
        get_certif_label(context, 1.5, s.format(title="Collaboration", ranking="LEGEND"), constants.COLOR_LEGEND)
        get_certif_label(context, 2.5, s.format(title="Algorithmes", ranking="GOLD"), constants.COLOR_GOLD)
        get_certif_label(context, 3.5, s.format(title="Optimization", ranking="SILVER"), constants.COLOR_SILVER)
        get_certif_label(context, 4.5, s.format(title="Coding Speed", ranking="BRONZE"), constants.COLOR_BRONZE)
        get_certif_label(context, 5.5, s.format(title="AI", ranking="LEGEND"), constants.COLOR_LEGEND)

        # DRAW SEPARATORS
        draw_line(context, 150, 50, 150, 190, constants.COLOR_LEGEND)
        draw_line(context, 360, 50, 360, 190, constants.COLOR_LEGEND)

        # LABEL STATS
        get_stats_label(context, 1, s.format(title="Global Rank", ranking="1234/654321"), constants.COLOR_LEGEND)
        get_stats_label(context, 2, s.format(title="Puzzle Solved", ranking="530"), constants.COLOR_GOLD)
        get_stats_label(context, 3, s.format(title="Level", ranking="38"), constants.COLOR_SILVER)
        get_stats_label(context, 4, s.format(title="Success", ranking="350/500"), constants.COLOR_BRONZE)
        get_stats_label(context, 5, s.format(title="Best Language", ranking="Python"), constants.COLOR_LEGEND)
        get_stats_label(context, 6, s.format(title="Highest Compet.", ranking="1200/15000"), constants.COLOR_LEGEND)


        # getting all the svg versions available
        versions = surface.get_versions()

    # the card is the component having nearly everything except external icons from CG
    card = etree.XML(f.getvalue())

    # load icons from constants (extracted from CG)
    SVG_collaboration = place_icon(constants.SVG_collaboration, nth_position=1.5)
    SVG_algorithmes = place_icon(constants.SVG_algorithmes, nth_position=2.5)
    SVG_optimization = place_icon(constants.SVG_optimization, nth_position=3.5)
    SVG_speed = place_icon(constants.SVG_speed, nth_position=4.5)
    SVG_AI = place_icon(constants.SVG_AI, nth_position=5.5)

    # load icons for stats
    SVG_GLOBAL_RANK = place_icon2(constants.SVG_GLOBAL_RANK, nth_position=1)
    SVG_PUZZLE_SOLVED = place_icon2(constants.SVG_PUZZLE_SOLVED, nth_position=2)
    SVG_LEVEL = place_icon2(constants.SVG_LEVEL, nth_position=3)
    SVG_SUCCESS = place_icon2(constants.SVG_SUCCESS, nth_position=4)
    SVG_BEST_LANGUAGE = place_icon2(constants.SVG_BEST_LANGUAGE, nth_position=5)
    SVG_HIGHEST_COMP = place_icon2(constants.SVG_HIGHEST_COMP, nth_position=6)

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