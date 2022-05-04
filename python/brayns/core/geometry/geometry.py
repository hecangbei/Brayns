# Copyright (c) 2015-2022 EPFL/Blue Brain Project
# All rights reserved. Do not distribute without permission.
#
# Responsible Author: adrien.fleury@epfl.ch
#
# This file is part of Brayns <https://github.com/BlueBrain/Brayns>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from typing import Iterable

from brayns.core.common.bounds import Bounds
from brayns.core.common.capsule import Capsule
from brayns.core.common.color import Color
from brayns.core.common.plane import Plane
from brayns.core.common.sphere import Sphere
from brayns.core.model.model import Model
from brayns.instance.instance import Instance


class Geometry:

    @staticmethod
    def add_boxes(instance: Instance, boxes: list[tuple[Bounds, Color]]) -> Model:
        geometries = (
            (box.serialize(), color)
            for box, color in boxes
        )
        return Geometry._add(instance, 'add-boxes', geometries)

    @staticmethod
    def add_capsules(instance: Instance, capsules: list[tuple[Capsule, Color]]) -> Model:
        geometries = (
            (capsule.serialize(), color)
            for capsule, color in capsules
        )
        return Geometry._add(instance, 'add-capsules', geometries)

    @staticmethod
    def add_planes(instance: Instance, planes: list[tuple[Plane, Color]]) -> Model:
        geometries = (
            (plane.serialize(), color)
            for plane, color in planes
        )
        return Geometry._add(instance, 'add-planes', geometries)

    @staticmethod
    def add_spheres(instance: Instance, spheres: list[tuple[Sphere, Color]]) -> Model:
        geometries = (
            (sphere.serialize(), color)
            for sphere, color in spheres
        )
        return Geometry._add(instance, 'add-spheres', geometries)

    @staticmethod
    def _add(instance: Instance, method: str, geometries: Iterable[tuple[dict, Color]]) -> Model:
        params = [
            {
                'geometry': geometry,
                'color': list(color)
            }
            for geometry, color in geometries
        ]
        result = instance.request(method, params)
        return Model.deserialize(result)
