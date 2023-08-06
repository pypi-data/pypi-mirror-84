#!/usr/bin/env python3
# coding: utf-8

from math import *
from zencad import *


class ScrewStyle:

    def __init__(
            self,
            angle: float = pi / 2,
            depth: float = 1.2,
            deepening: float = 0.01
    ):
        self._angle = angle
        self.depth = depth
        self._deepening = deepening

    def create_shape(
            self,
            radius: float,
            height: float
    ):
        pattern_length = self.depth + self._deepening
        pattern_half_height = pattern_length * sin(self._angle / 2)
        pattern = polysegment(
            points([
                (0, 0, pattern_half_height),
                (pattern_length, 0, 0),
                (0, 0, -pattern_half_height)
            ]),
            closed=True
        )
        screw_step = pattern_half_height * 2 + self._deepening
        pattern = pattern.right(radius - self._deepening)
        z_offset = screw_step
        extended_height = height + z_offset * 2
        path = helix(radius, extended_height, screw_step)
        result = pipe_shell(spine=path, profiles=[pattern], frenet=True)
        result += cylinder(radius, extended_height)
        result = result.down(z_offset)
        result ^= cylinder(radius + pattern_length + self._deepening, height)
        return result


if __name__ == "__main__":
    style = ScrewStyle(
        angle=pi / 2,
        depth=1.2,
        deepening=0.01
    )

    mask = halfspace().rotateX(pi / 2)

    screw_radius = 3.6
    screw_height = 12
    wall = 2.4

    screw = style.create_shape(
        radius=screw_radius,
        height=screw_height
    )

    disp(screw ^ mask, color(1, 0, 1))

    friction = 0.2
    base = cylinder(
        r=screw_radius + style.depth + friction + wall,
        h=screw_height
    )
    base -= style.create_shape(
        radius=screw_radius + friction,
        height=screw_height
    )

    disp(base ^ mask, color(0, 1, 1))

    show()
