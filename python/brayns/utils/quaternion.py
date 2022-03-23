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

import math
from dataclasses import dataclass
from typing import Iterator, Union

from brayns.utils.vector3 import Vector3


@dataclass(frozen=True)
class Quaternion:

    x: float
    y: float
    z: float
    w: float

    @staticmethod
    def from_euler(
        roll: float,
        pitch: float,
        yaw: float,
        degrees: bool = False
    ) -> 'Quaternion':
        if degrees:
            roll, pitch, yaw = (
                math.radians(angle)
                for angle in (roll, pitch, yaw)
            )
        r, p, y = (angle / 2 for angle in (roll, pitch, yaw))
        cr, cp, cy = (math.cos(angle) for angle in (r, p, y))
        sr, sp, sy = (math.sin(angle) for angle in (r, p, y))
        return Quaternion(
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )

    @staticmethod
    def from_axis_angle(
        axis: Vector3,
        angle: float,
        degrees=False
    ) -> 'Quaternion':
        if degrees:
            angle = math.radians(angle)
        half_angle = angle / 2
        axis = axis.normalize() * math.sin(half_angle)
        return Quaternion(*axis, math.cos(half_angle))

    def __iter__(self) -> Iterator[float]:
        yield from (self.x, self.y, self.z, self.w)

    def __abs__(self) -> float:
        return self.norm()

    def __neg__(self) -> 'Quaternion':
        return Quaternion(*(-x for x in self))

    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(*(x - y for x, y in zip(self, other)))

    def __mul__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return Quaternion(*(x * value for x in self))
        x0, y0, z0, w0 = self
        x1, y1, z1, w1 = value
        return Quaternion(
            w0 * x1 + x0 * w1 + y0 * z1 - z0 * y1,
            w0 * y1 - x0 * z1 + y0 * w1 + z0 * x1,
            w0 * z1 + x0 * y1 - y0 * x1 + z0 * w1,
            w0 * w1 - x0 * x1 - y0 * y1 - z0 * z1
        )

    def __rmul__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return self * value
        return value * self

    def __truediv__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return Quaternion(*(x / value for x in self))
        return self * value.inverse()

    def __rtruediv__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return Quaternion(*(value / x for x in self))
        return value * self.inverse()

    def square_norm(self) -> float:
        return sum(x * x for x in self)

    def norm(self) -> float:
        return math.sqrt(self.square_norm())

    def normalize(self) -> 'Quaternion':
        return self / self.norm()

    def conjugate(self) -> 'Quaternion':
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def inverse(self) -> 'Quaternion':
        return self.conjugate() / self.square_norm()

    def apply(self, value: Vector3) -> Vector3:
        q = self.normalize()
        v = q * Quaternion(*value, 0.0) * q.conjugate()
        return Vector3(v.x, v.y, v.z)

    def apply_around(self, value: Vector3, center: Vector3) -> Vector3:
        return center + self.apply(value - center)
