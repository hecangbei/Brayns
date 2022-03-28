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

from brayns.instance.scene.model_protocol import ModelProtocol
from brayns.instance.scene.scene import Scene
from instance.scene.mock_scene_client import MockSceneClient


class MockModel(ModelProtocol):

    def get_path(self) -> str:
        return 'path'

    def get_loader(self) -> str:
        return 'loader'

    def get_loader_properties(self) -> dict:
        return 'properties'


class TestScene(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._scene = Scene(self._client)

    def test_len(self) -> None:
        self._add_some_models()
        self.assertEqual(len(self._scene), len(self._client.models))

    def test_contains(self) -> None:
        self._add_some_models()
        for model in self._client.models:
            self.assertIn(model.id, self._scene)

    def test_iter(self) -> None:
        self._add_some_models()
        self.assertEqual(
            list(model.id for model in self._scene),
            list(model.id for model in self._client.models)
        )

    def test_bounds(self) -> None:
        self.assertEqual(self._scene.bounds, self._client.scene.bounds)

    def test_center(self) -> None:
        self.assertEqual(self._scene.center, self._scene.bounds.center)

    def test_size(self) -> None:
        self.assertEqual(self._scene.size, self._scene.bounds.size)

    def test_get_model(self) -> None:
        ref = self._client.add_model()
        model = self._scene.get_model(ref.id)
        self.assertEqual(ref.id, model.id)

    def test_add_model(self) -> None:
        instances = self._scene.add_model(MockModel())
        self.assertEqual(len(instances), 1)
        ref = self._client.models[0]
        model = instances[0]
        self.assertEqual(model.id, ref.id)
        self.assertEqual(model.bounds, ref.bounds)
        self.assertEqual(model.metadata, ref.metadata)
        self.assertEqual(model.visible, ref.visible)
        self.assertEqual(model.transform, ref.transform)

    def test_remove_model(self) -> None:
        self._add_some_models()
        count = len(self._scene)
        to_remove = self._client.models[0].id
        self._scene.remove_model(to_remove)
        self.assertEqual(len(self._scene), count - 1)
        self.assertNotIn(to_remove, self._scene)

    def test_clear(self) -> None:
        self._add_some_models()
        self._scene.clear()
        self.assertEqual(len(self._scene), 0)

    def _add_some_models(self) -> None:
        for _ in range(3):
            self._client.add_model()


if __name__ == '__main__':
    unittest.main()
