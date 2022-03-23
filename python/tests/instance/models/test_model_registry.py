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

from brayns.instance.models.model_instance import ModelInstance
from brayns.instance.models.model_protocol import ModelProtocol
from brayns.instance.models.model_registry import ModelRegistry
from client.mock_client import MockClient


class MockModel(ModelProtocol):

    @property
    def path(self) -> str:
        return 'path'

    @property
    def loader(self) -> str:
        return 'loader'

    @property
    def loader_properties(self) -> dict:
        return 'properties'


class TestModelRegistry(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockClient()
        self._models = ModelRegistry(self._client)

    def test_len(self) -> None:
        ids = [1, 2, 3]
        self._mock_scene(ids)
        self.assertEqual(len(self._models), len(ids))

    def test_contains(self) -> None:
        ids = [1, 2, 3]
        self._mock_scene(ids)
        self.assertIn(2, self._models)
        self.assertTrue(self._client.has_received('get-scene', None))
        self._mock_scene(ids)
        self.assertIn(ModelInstance(self._client, 1), self._models)
        self.assertTrue(self._client.has_received('get-scene', None))

    def test_iter(self) -> None:
        ids = [1, 2, 3]
        self._mock_scene(ids)
        self.assertEqual(list(model.id for model in self._models), ids)
        self.assertTrue(self._client.has_received('get-scene', None))

    def test_getitem(self) -> None:
        id = 1
        self._mock_scene([id])
        self.assertEqual(self._models[id].id, id)
        self.assertTrue(self._client.has_received('get-model', {'id': id}))

    def test_add(self) -> None:
        model = MockModel()
        id = 0
        self._client.results.append([{'id': id}])
        instances = self._models.add(model)
        self.assertTrue(
            self._client.has_received('add-model', model.to_dict())
        )
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0].id, id)

    def _mock_scene(self, ids: list[int]) -> None:
        self._client.results.append({
            'models': [
                {
                    'id': id
                }
                for id in ids
            ]
        })


if __name__ == '__main__':
    unittest.main()
