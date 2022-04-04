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

from brayns.common.geometry.quaternion import Quaternion
from brayns.common.geometry.vector3 import Vector3


@dataclass(frozen=True)
class Transform:

    translation: Vector3 = Vector3.zero()
    rotation: Quaternion = Quaternion.identity()
    scale: Vector3 = Vector3.one()

    @staticmethod
    def from_dict(message: dict) -> 'Transform':
        return Transform(
            Vector3(*message['translation']),
            Quaternion(*message['rotation']),
            Vector3(*message['scale'])
        )

    def to_dict(self) -> dict:
        return {
            'translation': list(self.translation),
            'rotation': list(self.rotation),
            'scale': list(self.scale),
            'rotation_center': list(self.translation)
        }

    def update(self, **kwargs) -> 'Transform':
        return replace(self, **kwargs)

    def translate(self, translation: Vector3) -> 'Transform':
        return self.update(translation=self.translation + translation)

    def rotate(self, rotation: Quaternion, center=Vector3.zero()) -> 'Transform':
        return self.update(
            translation=rotation.rotate(self.translation, center),
            rotation=rotation * self.rotation
        )

    def rescale(self, scale: Vector3) -> 'Transform':
        return self.update(scale=self.scale * scale)
