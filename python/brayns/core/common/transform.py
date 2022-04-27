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
class Transform:

    translation: Vector3 = Vector3.zero
    rotation: Quaternion = Quaternion.identity
    scale: Vector3 = Vector3.one

    @staticmethod
    def deserialize(message: dict) -> 'Transform':
        return Transform(
            translation=Vector3(*message['translation']),
            rotation=Quaternion(*message['rotation']),
            scale=Vector3(*message['scale'])
        )

    @classmethod
    @property
    def identity(cls) -> 'Transform':
        return Transform()

    def serialize(self) -> dict:
        return {
            'translation': list(self.translation),
            'rotation': list(self.rotation),
            'rotation_center': list(self.translation),
            'scale': list(self.scale)
        }

    def with_translation(self, translation: Vector3) -> 'Transform':
        return replace(self, translation=translation)

    def with_rotation(self, rotation: Quaternion) -> 'Transform':
        return replace(self, rotation=rotation)

    def with_scale(self, scale: Vector3) -> 'Transform':
        return replace(self, scale=scale)

    def translate(self, translation: Vector3) -> 'Transform':
        return self.with_translation(self.translation + translation)

    def rotate(self, rotation: Quaternion, center: Vector3 = Vector3.zero) -> 'Transform':
        return replace(
            self,
            translation=self.translation + center - rotation.rotate(center),
            rotation=rotation * self.rotation
        )

    def rescale(self, scale: Vector3) -> 'Transform':
        return self.with_scale(scale * self.scale)
