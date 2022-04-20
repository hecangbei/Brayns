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

from dataclasses import dataclass, field

from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.vector3 import Vector3


@dataclass
class Transform:

    translation: Vector3 = field(default_factory=lambda: Vector3.zero)
    rotation: Quaternion = field(default_factory=lambda: Quaternion.identity)
    scale: Vector3 = field(default_factory=lambda: Vector3.one)

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
