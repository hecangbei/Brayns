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

from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.transform import Transform
from brayns.core.geometry.vector3 import Vector3
from brayns.core.scene.model_loader import ModelLoader
from brayns.core.scene.scene_manager import SceneManager
from tests.core.scene.mock_scene_client import MockSceneClient


class TestSceneManager(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._manager = SceneManager(self._client)

    def test_get_scene(self) -> None:
        for _ in range(3):
            self._client.add_model()
        ref = self._client.scene
        test = self._manager.get_scene()
        self.assertEqual(test, ref)

    def test_get_model(self) -> None:
        ref = self._client.add_model()
        test = self._manager.get_model(ref.id)
        self.assertEqual(test, ref)

    def test_update_model(self) -> None:
        ref = self._client.add_model()
        test = self._manager.get_model(ref.id)
        test.visible = False
        test.transform = Transform(
            Vector3.one,
            Quaternion.from_euler(Vector3(0, 0, 30), degrees=True),
            2 * Vector3.one
        )
        self._manager.update_model(test)
        self.assertEqual(test, ref)

    def test_add_model(self) -> None:
        info = ModelLoader('path', 'loader', {'test': 1})
        test = self._manager.add_model(info)
        ref = self._client.models
        self.assertEqual(len(ref), 1)
        self.assertEqual(test, ref)

    def test_remove_models(self) -> None:
        ids = []
        for _ in range(3):
            model = self._client.add_model()
            ids.append(model.id)
        self._manager.remove_models(ids[:2])
        models = self._client.models
        self.assertEqual(len(models), 1)

    def test_clear_models(self) -> None:
        for _ in range(3):
            self._client.add_model()
        self._manager.clear_models()
        self.assertFalse(self._client.models)


if __name__ == '__main__':
    unittest.main()
