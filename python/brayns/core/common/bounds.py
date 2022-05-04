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
from typing import Iterable, Union

from brayns.core.common.vector3 import Vector3


@dataclass(frozen=True)
class Bounds:

    min: Vector3 = Vector3.zero
    max: Vector3 = Vector3.zero

    @staticmethod
    def deserialize(message: dict) -> 'Bounds':
        return Bounds(
            min=Vector3(*message['min']),
            max=Vector3(*message['max'])
        )

    @staticmethod
    def merge(bounds: Iterable['Bounds']) -> 'Bounds':
        return Bounds(
            min=min(i.min for i in bounds),
            max=max(i.max for i in bounds)
        )

    @staticmethod
    def from_size(size: Vector3, center: Vector3 = Vector3.zero) -> 'Bounds':
        half_size = size / 2
        return Bounds(center - half_size, center + half_size)

    @staticmethod
    def cube(size: float, center: Vector3 = Vector3.zero) -> 'Bounds':
        return Bounds.from_size(size * Vector3.one, center)

    @classmethod
    @property
    def empty(self) -> 'Bounds':
        return Bounds()

    @classmethod
    @property
    def one(self) -> 'Bounds':
        one_half = Vector3.full(0.5)
        return Bounds(-one_half, one_half)

    def __post_init__(self) -> None:
        if self.min > self.max:
            raise ValueError(f'Min {self.min} > max {self.max}')

    def __or__(self, other: 'Bounds') -> 'Bounds':
        return Bounds(min(self.min, other.min), max(self.max, other.max))

    def __contains__(self, value: Union['Bounds', Vector3]) -> bool:
        if isinstance(value, Bounds):
            return value.min in self and value.max in self
        return all(
            i >= min and i <= max
            for i, min, max in zip(value, self.min, self.max)
        )

    @property
    def center(self) -> Vector3:
        return (self.min + self.max) / 2

    @property
    def size(self) -> Vector3:
        return self.max - self.min

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    @property
    def depth(self) -> float:
        return self.size.z

    def serialize(self) -> dict:
        return {
            'min': list(self.min),
            'max': list(self.max)
        }

    def with_min(self, min: Vector3) -> 'Bounds':
        return replace(self, min=min)

    def with_max(self, max: Vector3) -> 'Bounds':
        return replace(self, max=max)

    def with_size(self, size: Vector3) -> 'Bounds':
        return Bounds.from_size(size, self.center)

    def with_center(self, center: Vector3) -> 'Bounds':
        return Bounds.from_size(self.size, center)

    def translate(self, translation: Vector3) -> 'Bounds':
        return Bounds(self.min + translation, self.max + translation)

    def rescale(self, scale: Vector3) -> 'Bounds':
        return Bounds.from_size(scale * self.size, self.center)
