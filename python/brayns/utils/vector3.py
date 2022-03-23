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

    def __iter__(self) -> Iterator[float]:
        yield from (self.x, self.y, self.z)

    def __neg__(self) -> 'Vector3':
        return Vector3(*(-x for x in self))

    def __abs__(self) -> float:
        return self.norm()

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(*(x - y for x, y in zip(self, other)))

    def __mul__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3(*(x * value for x in self))
        return Vector3(*(x * y for x, y in zip(self, value)))

    def __rmul__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        return self * value

    def __truediv__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3(*(x / value for x in self))
        return Vector3(*(x / y for x, y in zip(self, value)))

    def __rtruediv__(self, value: Union[int, float, 'Vector3']) -> 'Vector3':
        if isinstance(value, (int, float)):
            return Vector3(*(value / x for x in self))
        return Vector3(*(y / x for x, y in zip(self, value)))

    def square_norm(self) -> float:
        return sum(x * x for x in self)

    def norm(self) -> float:
        return math.sqrt(self.square_norm())

    def normalize(self) -> 'Vector3':
        return self / self.norm()
