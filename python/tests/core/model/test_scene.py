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

import unittest

from brayns.core.common.bounds import Bounds
from brayns.core.common.transform import Transform
from brayns.core.common.vector3 import Vector3
from brayns.core.model.model import Model
from brayns.core.model.scene import Scene
from tests.core.model.mock_model_instance import MockModelInstance


class TestScene(unittest.TestCase):

    def test_from_instance(self) -> None:
        instance = MockModelInstance()
        test = Scene.from_instance(instance)
        ref = Scene.deserialize(instance.scene)
        self.assertEqual(test, ref)

    def test_deserialize(self) -> None:
        message = {
            'bounds': {
                'min': [0, 0, 0],
                'max': [1, 1, 1]
            },
            'models': [
                {
                    'id': 0,
                    'bounds': {
                        'min': [0, 0, 0],
                        'max': [1, 1, 1]
                    },
                    'metadata': {'test': 1},
                    'visible': True,
                    'transformation': Transform.identity.serialize()
                }
            ]
        }
        test = Scene.deserialize(message)
        ref = Scene(
            Bounds(Vector3.zero, Vector3.one),
            [
                Model(
                    id=0,
                    bounds=Bounds(Vector3.zero, Vector3.one),
                    metadata={'test': 1},
                    visible=True,
                    transform=Transform.identity
                )
            ]
        )
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
