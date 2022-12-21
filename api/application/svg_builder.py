import math

import cairo
from io import BytesIO

from config import constants

def render(data):
    f = BytesIO()

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
    
        # getting all the svg versions available
        versions = surface.get_versions()

    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    return f.getvalue()


# https://www.geeksforgeeks.org/pycairo-drawing-different-type-of-line-caps/?ref=rp
# https://pycairo.readthedocs.io/en/latest/reference/enums.html