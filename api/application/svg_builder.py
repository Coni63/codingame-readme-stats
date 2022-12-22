import math

import cairo
from io import BytesIO, StringIO

from config import constants
import base64 
import svgutils
from lxml import etree

def decode_svg(svg_encoded):
    encoded = svg_encoded.replace("data:image/svg+xml;base64,", "")
    return base64.b64decode(encoded).decode("utf-8") 


def render(data):
    f = BytesIO()
    f2 = BytesIO()

    with cairo.SVGSurface(f, constants.SVG_width, constants.SVG_height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)
    
        context.set_source_rgba(0, 0, 0, 1)
        context.rectangle(0, 0, constants.SVG_width, constants.SVG_height)  # x, y, width, height
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

        context.set_source_rgba(1, 0, 0, 1)
        context.rectangle(50, 50, 29, 29)  # x, y, width, height
        context.fill()
    
        # getting all the svg versions available
        versions = surface.get_versions()

    a = etree.XML(f.getvalue())

    SVG_collaboration = etree.fromstring(decode_svg(constants.SVG_collaboration))
    SVG_algorithmes = etree.fromstring(decode_svg(constants.SVG_algorithmes))
    SVG_optimization = etree.fromstring(decode_svg(constants.SVG_optimization))
    SVG_speed = etree.fromstring(decode_svg(constants.SVG_speed))
    SVG_AI = etree.fromstring(decode_svg(constants.SVG_AI))

    d = svgutils.transform.SVG(decode_svg(constants.SVG_AI))
    d.moveto(50, 50)

    c = svgutils.transform.fromstring(decode_svg(constants.SVG_AI))
    # c.moveto(50, 50)


    fig = svgutils.transform.SVGFigure("500px", "200px")
    fig.append([a, d])

    return fig.to_str()
    # return svgutils.compose.Figure("500px", "200px", *all_trees).tostr()


# https://www.geeksforgeeks.org/pycairo-drawing-different-type-of-line-caps/?ref=rp
# https://pycairo.readthedocs.io/en/latest/reference/enums.html