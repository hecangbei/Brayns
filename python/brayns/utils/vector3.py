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


@dataclass(frozen=True)
class Vector3:

    x: float
    y: float
    z: float

    @staticmethod
    def full(value: float) -> 'Vector3':
        return Vector3(value, value, value)

    @staticmethod
    def unpack(values: Iterator[float]) -> 'Vector3':
        return Vector3(*values)

    def __iter__(self) -> Iterator[float]:
        yield from (self.x, self.y, self.z)

    def __neg__(self) -> 'Vector3':
        return Vector3.unpack(-i for i in self)

    def __abs__(self) -> float:
        return self.norm

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3.unpack(i + j for i, j in zip(self, other))

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3.unpack(i - j for i, j in zip(self, other))

    def __mul__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3.unpack(i * value for i in self)
        return Vector3.unpack(i * j for i, j in zip(self, value))

    def __rmul__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        return self * value

    def __truediv__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3.unpack(i / value for i in self)
        return Vector3.unpack(i / j for i, j in zip(self, value))

    def __rtruediv__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3.unpack(value / i for i in self)
        return Vector3.unpack(j / i for i, j in zip(self, value))

    @property
    def square_norm(self) -> float:
        return sum(i * i for i in self)

    @property
    def norm(self) -> float:
        return math.sqrt(self.square_norm)

    @property
    def normalized(self) -> 'Vector3':
        return self / self.norm
