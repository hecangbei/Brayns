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

from brayns.instance.scene.model_instance import ModelInstance
from brayns.instance.scene.model_protocol import ModelProtocol
from brayns.instance.scene.model_registry import ModelRegistry
from brayns.utils.box import Box
from tests.instance.scene.mock_scene_client import MockSceneClient


class MockModel(ModelProtocol):

    def get_path(self) -> str:
        return 'path'

    def get_loader(self) -> str:
        return 'loader'

    def get_loader_properties(self) -> dict:
        return 'properties'


class TestModelRegistry(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._models = ModelRegistry(self._client)

    def test_len(self) -> None:
        self._add_some_models()
        self.assertEqual(len(self._models), len(self._client.get_models()))

    def test_contains(self) -> None:
        self._add_some_models()
        for id in self._client.get_model_ids():
            self.assertIn(id, self._models)
            self.assertIn(ModelInstance(self._client, id), self._models)

    def test_iter(self) -> None:
        self._add_some_models()
        self.assertEqual(
            list(model.id for model in self._models),
            self._client.get_model_ids()
        )

    def test_getitem(self) -> None:
        self._add_some_models()
        for id in self._client.get_model_ids():
            self.assertEqual(self._models[id].id, id)

    def test_add(self) -> None:
        instances = self._models.add(MockModel())
        self.assertEqual(len(instances), 1)
        template = self._client.get_models()[0]
        model = instances[0]
        self.assertEqual(model.id, template['id'])
        self.assertEqual(model.bounds, Box.from_dict(template['bounds']))
        self.assertEqual(model.metadata, template['metadata'])
        self.assertEqual(model.visible, template['visible'])
        self.assertEqual(model.transform.to_dict(), template['transformation'])

    def test_remove(self) -> None:
        self._add_some_models()
        ids = self._client.get_model_ids()
        count = len(ids)
        removed = ids[0:2]
        self._models.remove(removed)
        self.assertEqual(len(self._models), count - len(removed))
        for id in removed:
            self.assertNotIn(id, self._models)
        for id in self._client.get_model_ids():
            self.assertIn(id, self._models)

    def test_clear(self) -> None:
        self._add_some_models()
        self._models.clear()
        self.assertEqual(len(self._models), 0)

    def _add_some_models(self) -> None:
        for _ in range(3):
            self._client.add_mock_model()


if __name__ == '__main__':
    unittest.main()
