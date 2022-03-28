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

from brayns.utils.box import Box
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3


@dataclass
class MockSceneModel:

    id: int
    bounds: Box = Box(-Vector3.one(), Vector3.one())
    metadata: dict[str, str] = field(default_factory=dict)
    visible: bool = True
    transform: Transform = Transform()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'bounds': {
                'min': list(self.bounds.min),
                'max': list(self.bounds.max)
            },
            'metadata': self.metadata,
            'visible': self.visible,
            'transformation': self.transform.to_dict()
        }
