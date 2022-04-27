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

from dataclasses import dataclass
from typing import Iterator

from brayns.core.common.vector import Vector


@dataclass(frozen=True)
class Color(Vector):

    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0
    alpha: float = 1.0

    @staticmethod
    def normalize_hex(value: str) -> float:
        return int(value, base=16) / 255

    @staticmethod
    def from_hex(value: str) -> 'Color':
        return Color(
            Color.normalize_hex(value[0:2]),
            Color.normalize_hex(value[2:4]),
            Color.normalize_hex(value[4:6])
        )

    @staticmethod
    def from_int8(red: int, green: int, blue: int, alpha: int = 255) -> 'Color':
        return Color(red, green, blue, alpha) / 255

    @classmethod
    @property
    def bbp_background(cls) -> 'Color':
        return Color(0.004, 0.016, 0.102, 0.0)

    def __iter__(self) -> Iterator[float]:
        yield self.red
        yield self.green
        yield self.blue
        yield self.alpha
