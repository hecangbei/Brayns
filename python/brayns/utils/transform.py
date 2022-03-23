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

from brayns.utils.quaternion import Quaternion
from brayns.utils.vector3 import Vector3


@dataclass(frozen=True)
class Transform:

    translation: Vector3
    scale: Vector3
    rotation: Quaternion
    rotation_center: Vector3

    @staticmethod
    def from_dict(message: dict) -> 'Transform':
        return Transform(
            Vector3(*message['translation']),
            Vector3(*message['scale']),
            Quaternion(*message['rotation']),
            Vector3(*message['rotation_center']),
        )

    def to_dict(self) -> dict:
        return {
            'translation': list(self.translation),
            'scale': list(self.scale),
            'rotation': list(self.rotation),
            'rotation_center': list(self.rotation_center),
        }
