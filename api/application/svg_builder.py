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

def get_square(context, nth_position, bg_color):
    s = get_scale() * 29
    color = hex_to_rgb(bg_color)
    context.set_source_rgb(*color)
    # context.rectangle(*get_position(nth_position), s, s)  # x, y, width, height
    roundrect(context, *get_position(nth_position), s, s, 5)
    context.fill()

def get_position(n = 1):
    return (160, n * 25 - 20)

def get_scale():
    return 0.66

def hex_to_rgb(value):
    value = value.lstrip('#')
    r = value[:2]
    g = value[2:4]
    b = value[4:]
    return (int(r, 16)/255.0, int(g, 16)/255.0, int(b, 16)/255.0)

def render(data):
    f = BytesIO()

    with cairo.SVGSurface(f, constants.SVG_width, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)
    
        context.set_source_rgba(0, 0, 0, 1)
        context.rectangle(0, 0, constants.SVG_width-10, constants.SVG_height-10)  # x, y, width, height
        context.stroke()

        context.set_source_rgba(1, 0, 0, 1)
        context.set_line_width(10)
        context.set_line_cap(cairo.LINE_CAP_BUTT)
        context.arc(50, 50, 30,  6.7*math.pi/2, 3*math.pi/2)  # cx, cy, radius, angle_start, angle_end
        context.stroke()

        context.set_source_rgba(0, 0, 0, 1)
        context.set_line_width(12)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        # context.set_line_cap(cairo.LINE_CAP_SQUARE)
        context.arc(50, 50, 30, 3*math.pi/2, 6.7*math.pi/2)  # cx, cy, radius, angle_start, angle_end
        context.stroke()

        # SQUARE BACKGROUND FOR IMG
        get_square(context, 1, "#FF0000")
        get_square(context, 2, "#00FF00")
        get_square(context, 3, "#FF00FF")
        get_square(context, 4, "#FFFF00")
        get_square(context, 5, "#00FFFF")

        # getting all the svg versions available
        versions = surface.get_versions()

    a = etree.XML(f.getvalue())

    SVG_collaboration = place_icon(constants.SVG_collaboration, nth_position=1)
    SVG_algorithmes = place_icon(constants.SVG_algorithmes, nth_position=2)
    SVG_optimization = place_icon(constants.SVG_optimization, nth_position=3)
    SVG_speed = place_icon(constants.SVG_speed, nth_position=4)
    SVG_AI = place_icon(constants.SVG_AI, nth_position=5)


    fig = svgutils.transform.SVGFigure()
    fig.set_size(("{constants.SVG_width}px", "{constants.SVG_height}px"))
    fig.append([a, SVG_collaboration, SVG_algorithmes, SVG_optimization, SVG_speed, SVG_AI])
    return fig.to_str()
    # return svgutils.compose.Figure("500px", "200px", *all_trees).tostr()


# https://www.geeksforgeeks.org/pycairo-drawing-different-type-of-line-caps/?ref=rp
# https://pycairo.readthedocs.io/en/latest/reference/enums.html

# <svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" fill="none"><script xmlns=""/><link xmlns="" type="text/css" rel="stylesheet" id="dark-mode-custom-link"/><link xmlns="" type="text/css" rel="stylesheet" id="dark-mode-general-link"/><style xmlns="" lang="en" type="text/css" id="dark-mode-custom-style"/><style xmlns="" lang="en" type="text/css" id="dark-mode-native-style"/><style xmlns="" lang="en" type="text/css" id="dark-mode-native-sheet"/><script xmlns="" id="youtube-hd-fjdmkanbdloodhegphphhklnjfngoffa">var ythdlog = () =&gt; {};;var ythderror = () =&gt; {};</script>
