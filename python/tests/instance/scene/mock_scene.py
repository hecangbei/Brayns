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

from brayns.common.geometry.box import Box
from brayns.common.geometry.vector3 import Vector3
from tests.instance.scene.mock_scene_model import MockSceneModel


@dataclass
class MockScene:

    bounds: Box = Box(Vector3.full(-5), Vector3.full(5))
    models: list[MockSceneModel] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'bounds': {
                'min': list(self.bounds.min),
                'max': list(self.bounds.max)
            },
            'models': [
                model.to_dict()
                for model in self.models
            ]
        }
