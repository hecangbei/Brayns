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

from dataclasses import dataclass, replace
from typing import Iterator

from brayns.core.common.quaternion import Quaternion
from brayns.core.common.vector3 import Vector3


@dataclass(frozen=True)
class Plane:

    normal: Vector3
    distance: float = 0.0

    @staticmethod
    def from_coefficients(a: float, b: float, c: float, d: float) -> 'Plane':
        return Plane(Vector3(a, b, c), d)

    @classmethod
    @property
    def horizonal(cls) -> 'Plane':
        return Plane(Vector3.up)

    @classmethod
    @property
    def front(cls) -> 'Plane':
        return Plane(Vector3.forward)

    @classmethod
    @property
    def side(cls) -> 'Plane':
        return Plane(Vector3.right)

    def __iter__(self) -> Iterator[float]:
        yield from self.normal
        yield self.distance

    def serialize(self) -> dict:
        return {
            'coefficients': list(self)
        }

    def with_normal(self, normal: Vector3) -> 'Plane':
        return replace(self, normal=normal)

    def with_distance(self, distance: float) -> 'Plane':
        return replace(self, distance=distance)

    def translate(self, distance: float) -> 'Plane':
        return Plane(self.normal, self.distance + distance)

    def rotate(self, rotation: Quaternion) -> 'Plane':
        return replace(self, normal=rotation.rotate(self.normal))
