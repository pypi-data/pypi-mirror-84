"""
Shapes drawers.

"""

from math import pi

from .helpers import normalize, point, point_angle, size


def circle(surface, node):
    """Draw a circle ``node`` on ``surface``."""
    r = size(surface, node.get('r'))
    if not r:
        return
    cx = size(surface, node.get('cx'), 'x')
    cy = size(surface, node.get('cy'), 'y')

    surface.context.new_sub_path()
    surface.context.arc(cx, cy, r, 0, 2 * pi)


def ellipse(surface, node):
    """Draw an ellipse ``node`` on ``surface``."""
    rx = size(surface, node.get('rx'), 'x')
    ry = size(surface, node.get('ry'), 'y')
    if not rx or not ry:
        return
    cx = size(surface, node.get('cx'), 'x')
    cy = size(surface, node.get('cy'), 'y')

    ratio = ry / rx
    surface.context.new_sub_path()
    surface.context.save()
    surface.context.scale(1, ratio)
    surface.context.arc(cx, cy / ratio, rx, 0, 2 * pi)
    surface.context.restore()


def line(surface, node):
    """Draw a line ``node``."""
    x1, y1, x2, y2 = tuple(
        size(surface, node.get(position), position[0])
        for position in ('x1', 'y1', 'x2', 'y2'))
    surface.context.move_to(x1, y1)
    surface.context.line_to(x2, y2)
    angle = point_angle(x1, y1, x2, y2)
    node.vertices = [(x1, y1), (pi - angle, angle), (x2, y2)]


def polygon(surface, node):
    """Draw a polygon ``node`` on ``surface``."""
    polyline(surface, node)
    surface.context.close_path()


def polyline(surface, node):
    """Draw a polyline ``node``."""
    points = normalize(node.get('points', ''))
    if points:
        x, y, points = point(surface, points)
        surface.context.move_to(x, y)
        node.vertices = [(x, y)]
        while points:
            x_old, y_old = x, y
            x, y, points = point(surface, points)
            angle = point_angle(x_old, y_old, x, y)
            node.vertices.append((pi - angle, angle))
            surface.context.line_to(x, y)
            node.vertices.append((x, y))


def rect(surface, node):
    """Draw a rect ``node`` on ``surface``."""
    x, y = size(surface, node.get('x'), 'x'), size(surface, node.get('y'), 'y')
    width = size(surface, node.get('width'), 'x')
    height = size(surface, node.get('height'), 'y')
    rx = node.get('rx')
    ry = node.get('ry')
    if rx and ry is None:
        ry = rx
    elif ry and rx is None:
        rx = ry
    rx = size(surface, rx, 'x')
    ry = size(surface, ry, 'y')

    if rx == 0 or ry == 0:
        surface.context.rectangle(x, y, width, height)
    else:
        if rx > width / 2:
            rx = width / 2
        if ry > height / 2:
            ry = height / 2

        # Inspired by Cairo Cookbook
        # http://cairographics.org/cookbook/roundedrectangles/
        ARC_TO_BEZIER = 4 * (2 ** .5 - 1) / 3
        c1 = ARC_TO_BEZIER * rx
        c2 = ARC_TO_BEZIER * ry

        surface.context.new_path()
        surface.context.move_to(x + rx, y)
        surface.context.rel_line_to(width - 2 * rx, 0)
        surface.context.rel_curve_to(c1, 0, rx, c2, rx, ry)
        surface.context.rel_line_to(0, height - 2 * ry)
        surface.context.rel_curve_to(0, c2, c1 - rx, ry, -rx, ry)
        surface.context.rel_line_to(-width + 2 * rx, 0)
        surface.context.rel_curve_to(-c1, 0, -rx, -c2, -rx, -ry)
        surface.context.rel_line_to(0, -height + 2 * ry)
        surface.context.rel_curve_to(0, -c2, rx - c1, -ry, rx, -ry)
        surface.context.close_path()
