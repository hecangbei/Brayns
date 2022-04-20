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

from brayns.core.geometry.box import Box
from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.transform import Transform
from brayns.core.geometry.vector3 import Vector3
from brayns.core.scene.model import Model
from brayns.core.scene.model_loader import ModelLoader
from brayns.core.scene.scene import Scene
from tests.core.scene.mock_scene_instance import MockSceneInstance


class TestScene(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSceneInstance()

    def test_from_instance(self) -> None:
        model = self._instance.add_model()
        scene = Scene.from_instance(self._instance)
        self.assertEqual(scene.bounds, Box.deserialize(self._instance.bounds))
        self.assertEqual(scene.models, [Model.deserialize(model)])
        self.assertEqual(self._instance.methods, ['get-scene'])
        self.assertEqual(self._instance.params, [None])

    def test_deserialize(self) -> None:
        self._instance.add_model()
        message = self._instance.get_scene()
        scene = Scene.deserialize(message)
        self.assertEqual(scene.bounds, Box.deserialize(message['bounds']))
        self.assertEqual(scene.models, [
            Model.deserialize(model)
            for model in message['models']
        ])

    def test_remove_models(self) -> None:
        ids = [1, 2, 3]
        Scene.remove_models(self._instance, ids)
        self.assertEqual(self._instance.methods, ['remove-model'])
        self.assertEqual(self._instance.params, [{'ids': ids}])

    def test_clear(self) -> None:
        for _ in range(3):
            self._instance.add_model()
        Scene.clear(self._instance)
        self.assertFalse(self._instance.models)


if __name__ == '__main__':
    unittest.main()
