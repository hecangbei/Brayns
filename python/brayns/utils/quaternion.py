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
from typing import Iterable, Iterator, Union

from brayns.utils.vector3 import Vector3


@dataclass(frozen=True)
class Quaternion:

    x: float
    y: float
    z: float
    w: float

    @staticmethod
    def from_euler(rpy: Vector3, degrees: bool = False) -> 'Quaternion':
        if degrees:
            rpy = Vector3.unpack(math.radians(i) for i in rpy)
        rpy /= 2
        cr, cp, cy = Vector3.unpack(math.cos(i) for i in rpy)
        sr, sp, sy = Vector3.unpack(math.sin(i) for i in rpy)
        return Quaternion(
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )

    @staticmethod
    def from_axis_angle(axis: Vector3, angle: float, degrees=False) -> 'Quaternion':
        if degrees:
            angle = math.radians(angle)
        half_angle = angle / 2
        axis = axis.normalized * math.sin(half_angle)
        return Quaternion(*axis, math.cos(half_angle))

    @staticmethod
    def from_vector(value: Vector3) -> 'Quaternion':
        return Quaternion(*value, 0.0)

    @staticmethod
    def identity() -> 'Quaternion':
        return Quaternion(0.0, 0.0, 0.0, 1.0)

    @staticmethod
    def unpack(values: Iterable[float]) -> 'Quaternion':
        return Quaternion(*values)

    def __iter__(self) -> Iterator[float]:
        yield from (self.x, self.y, self.z, self.w)

    def __abs__(self) -> float:
        return self.norm

    def __neg__(self) -> 'Quaternion':
        return Quaternion.unpack(-i for i in self)

    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion.unpack(i + j for i, j in zip(self, other))

    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion.unpack(i - j for i, j in zip(self, other))

    def __mul__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return Quaternion.unpack(i * value for i in self)
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
            return Quaternion.unpack(i / value for i in self)
        return self * value.inverse

    def __rtruediv__(self, value: Union[int, float, 'Quaternion']) -> 'Quaternion':
        if isinstance(value, (int, float)):
            return Quaternion.unpack(value / i for i in self)
        return value * self.inverse

    @property
    def vector(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

    @property
    def square_norm(self) -> float:
        return sum(i * i for i in self)

    @property
    def norm(self) -> float:
        return math.sqrt(self.square_norm)

    @property
    def normalized(self) -> 'Quaternion':
        return self / self.norm

    @property
    def conjugate(self) -> 'Quaternion':
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    @property
    def inverse(self) -> 'Quaternion':
        return self.conjugate / self.square_norm

    def rotate(self, value: Vector3, center=Vector3.full(0)) -> Vector3:
        rotation = self.normalized
        quaternion = Quaternion.from_vector(value - center)
        quaternion = rotation * quaternion * rotation.conjugate
        return center + quaternion.vector
