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

from brayns.core.common.quaternion import Quaternion
from brayns.core.common.vector3 import Vector3


@dataclass(frozen=True)
class Capsule:

    start_point: Vector3
    start_radius: float
    end_point: Vector3
    end_radius: float

    @property
    def center(self) -> Vector3:
        return (self.end_point + self.start_point) / 2

    def serialize(self) -> dict:
        return {
            'p0': list(self.start_point),
            'r0': self.start_radius,
            'p1': list(self.end_point),
            'p1': self.end_radius
        }

    def with_start_point(self, start_point: Vector3) -> 'Capsule':
        return replace(self, start_point=start_point)

    def with_start_radius(self, start_radius: float) -> 'Capsule':
        return replace(self, start_radius=start_radius)

    def with_end_point(self, end_point: Vector3) -> 'Capsule':
        return replace(self, end_point=end_point)

    def with_end_radius(self, end_radius: float) -> 'Capsule':
        return replace(self, end_radius=end_radius)

    def with_radius(self, radius: float) -> 'Capsule':
        return replace(
            self,
            start_radius=radius,
            end_radius=radius
        )

    def translate(self, translation: Vector3) -> 'Capsule':
        return replace(
            self,
            start_point=self.start_point + translation,
            end_point=self.end_point + translation,
        )

    def rotate(self, rotation: Quaternion, center: Vector3 = Vector3.zero) -> 'Capsule':
        return replace(
            self,
            start_point=rotation.rotate(self.start_point, center),
            end_point=rotation.rotate(self.end_point, center)
        )

    def multiply_radius(self, value: float) -> 'Capsule':
        return replace(
            self,
            start_radius=value * self.start_radius,
            end_radius=value * self.end_radius
        )
