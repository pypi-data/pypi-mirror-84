#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations
from math import *
from zencad import *
from typing import Callable


class InvoluteStyle:

    def __init__(
            self,
            module: float = 3.6,
            pressure_angle: float = deg2rad(20),
            addendum_by_module: float = 1,
            dedendum_by_module: float = 1.157,
            root_fillet_by_module: float = 0.5
    ):
        self.module = module
        self.pressure_angle = pressure_angle
        self.addendum = addendum_by_module * module
        self.dedendum = dedendum_by_module * module
        self.root_fillet = root_fillet_by_module * module


class GearContext:

    @staticmethod
    def _find(
            style: InvoluteStyle,
            initial_tooth_count: int,
            tooth_count_step: int,
            predicate: Callable[[GearContext], bool]
    ) -> GearContext:
        tooth_count = initial_tooth_count
        while True:
            context = GearContext(style, tooth_count)
            if predicate(context):
                return context
            tooth_count += tooth_count_step

    @staticmethod
    def find_min(
            style: InvoluteStyle,
            predicate: Callable[[GearContext], bool]
    ) -> GearContext:
        return GearContext._find(
            style=style,
            initial_tooth_count=2,
            tooth_count_step=1,
            predicate=predicate
        )

    @staticmethod
    def find_max(
            style: InvoluteStyle,
            initial_tooth_count: int,
            predicate: Callable[[GearContext], bool]
    ) -> GearContext:
        return GearContext._find(
            style=style,
            initial_tooth_count=initial_tooth_count,
            tooth_count_step=-1,
            predicate=predicate
        )

    def __init__(
            self,
            style: InvoluteStyle,
            tooth_count: int
    ):

        self._style = style
        self.tooth_count = tooth_count
        self.tooth_angle = pi * 2 / tooth_count

        self.pitch_radius = tooth_count * style.module / 2
        self._base_radius = self.pitch_radius * cos(style.pressure_angle)
        self.outside_radius = self.pitch_radius + style.addendum
        self.root_radius = self.pitch_radius - style.dedendum

        self._base_angle = self._calc_raw_involute_angle(self.pitch_radius) + self.tooth_angle / 4
        self._pitch_angle = self._calc_involute_angle(self.pitch_radius)
        self._outside_angle = self._calc_involute_angle(self.outside_radius)

        self._involuteStartRadius = max(self._base_radius, self.root_radius)
        self._involuteStartAngle = self._calc_involute_angle(self._involuteStartRadius)

        self._config_root_fillet()

    def _config_root_fillet(self):
        root_segment_angle_cos = sin(self.tooth_angle / 2 - self._base_angle)
        max_by_tooth_angle = (self.root_radius * root_segment_angle_cos) / (1 - root_segment_angle_cos)
        max_by_base_radius = (self._base_radius ** 2 - self.root_radius ** 2) / (2 * self.root_radius)
        self._root_fillet = min(
            [
                self._style.root_fillet,
                max_by_tooth_angle,
                max_by_base_radius,
            ]
        )
        if self._root_fillet < 0:
            self._root_fillet = 0
        r = self.root_radius
        f = self._root_fillet
        self._root_fillet_length = sqrt((r + f) ** 2 - f ** 2) - r
        self._root_fillet_angle = acos(f / (r + f))
        self._root_fillet_offset_angle = asin(f / (r + f))

    def _calc_raw_involute_angle(
            self,
            radius: float
    ):
        t = sqrt((radius / self._base_radius) ** 2 - 1)
        return t - atan(t)

    def _calc_involute_angle(
            self,
            radius: float
    ):
        result = self._calc_raw_involute_angle(radius)
        result = self._base_angle - result
        return result

    def create_profile(
            self,
            involute_points_count: int = 30
    ):

        wires = []

        def add_root_circle():
            end_angle = -self._involuteStartAngle - self._root_fillet_offset_angle
            start_angle = -self.tooth_angle - end_angle
            if end_angle <= start_angle:
                return
            wires.append(
                circle(
                    r=self.root_radius,
                    angle=(start_angle, end_angle),
                    wire=True
                )
            )

        add_root_circle()

        def create_side_wire():
            side_wires = []

            def add_root_fillet_circle():
                if self._root_fillet <= 0:
                    return
                side_wires.append(
                    circle(
                        r=self._root_fillet,
                        angle=(- self._root_fillet_angle, 0),
                        wire=True
                    )
                        .rotateZ(pi)
                        .right(self.root_radius + self._root_fillet)
                        .rotateZ(-self._base_angle - self._root_fillet_offset_angle)
                )

            add_root_fillet_circle()

            def add_root_to_base_segment():
                srart_radius = self.root_radius + self._root_fillet_length
                end_radius = self._base_radius
                if end_radius <= srart_radius:
                    return
                side_wires.append(
                    segment(
                        (srart_radius, 0),
                        (end_radius, 0)
                    )
                        .rotateZ(-self._base_angle)
                )

            add_root_to_base_segment()

            def add_involute():

                def get_point(radius):
                    result = point(radius, 0)
                    angle = self._calc_involute_angle(radius)
                    result = result.rotateZ(angle)
                    result = result.mirrorXZ()
                    return result

                radius_start = self._involuteStartRadius
                radius_step = (self.outside_radius - radius_start) / (involute_points_count - 1)
                points = [get_point(radius_start + radius_step * i) for i in range(involute_points_count)]
                side_wires.append(interpolate(points))

            add_involute()

            result = sew(side_wires)
            return result

        side_wire = create_side_wire()

        wires.append(side_wire)

        def add_outside_circle():
            if self._outside_angle <= 0:
                return
            wires.append(
                circle(
                    r=self.outside_radius,
                    angle=(-self._outside_angle, self._outside_angle),
                    wire=True
                )
            )

        add_outside_circle()

        wires.append(side_wire.mirrorXZ())

        result = sew(wires)
        result = sew([result.rotateZ(self.tooth_angle * i) for i in range(self.tooth_count)])
        return result

    def create_markup(self):
        tooth_separator_segment = segment(
            (self.root_radius, 0),
            (self.outside_radius, 0)
        )
        result = [tooth_separator_segment.rotateZ(self.tooth_angle * (i + 0.5)) for i in range(self.tooth_count)]
        result += [
            circle(self.root_radius, wire=True),
            circle(self._base_radius, wire=True),
            circle(self.pitch_radius, wire=True),
            circle(self.outside_radius, wire=True)
        ]
        return union(result)


if __name__ == "__main__":
    from time import time

    wall = 2.4
    friction = 0.2

    involute_style = InvoluteStyle(
        module=2.4,
        pressure_angle=deg2rad(20),
        addendum_by_module=1,
        dedendum_by_module=1.157,
        root_fillet_by_module=0.25
    )

    gear1Context = GearContext.find_min(
        style=involute_style,
        predicate=lambda context: context.outside_radius > 15
    )
    gear2Context = GearContext.find_max(
        style=involute_style,
        initial_tooth_count=100,
        predicate=lambda context: context.outside_radius < 60
    )

    gear1 = disp(
        difference(
            [
                gear1Context.create_profile().fill(),
                circle(gear1Context.root_radius - wall)
            ]
        )
            .extrude(wall)
            .rotateZ(gear1Context.tooth_angle / 2),
        color(1, 1, 0)
    )

    gear2 = disp(
        difference(
            [
                gear2Context.create_profile().fill(),
                circle(gear2Context.root_radius - wall)
            ]
        )
            .extrude(wall),
        color(0, 1, 1)
    )

    startTime = time()


    def animate(_):
        teeth_rotation = (time() - startTime) * 0.5

        gear1_transformation = \
            left(gear1Context.pitch_radius + friction / 2) \
            * rotateZ(-teeth_rotation * gear1Context.tooth_angle)
        gear1.relocate(gear1_transformation)

        gear2_transformation = \
            right(gear2Context.pitch_radius + friction / 2) \
            * rotateZ(teeth_rotation * gear2Context.tooth_angle)
        gear2.relocate(gear2_transformation)


    show(animate=animate)
