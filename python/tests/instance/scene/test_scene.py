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

from typing import Any
import unittest

from brayns.client.client_protocol import ClientProtocol
from brayns.instance.scene.model_instance import ModelInstance
from brayns.instance.scene.model_protocol import ModelProtocol
from brayns.instance.scene.scene import Scene
from brayns.utils.box import Box
from brayns.utils.quaternion import Quaternion
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3


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


class MockClient(ClientProtocol):

    def __init__(self) -> None:
        self.scene = {
            'bounds': {
                'min': [1, 2, 3],
                'max': [4, 5, 6]
            },
            'models': []
        }
        self._id = 0

    def create_fake_model(self) -> dict:
        self._id += 1
        return {
            'id': self._id - 1,
            'bounds': self.scene['bounds'],
            'metadata': {'test': '123'},
            'visible': True,
            'transformation': Transform(
                Vector3(0, 0, 0),
                Quaternion(0, 0, 0, 1),
                Vector3(1, 1, 1)
            ).to_dict()
        }

    def add_fake_model(self) -> dict:
        model = self.create_fake_model()
        self.scene['models'].append(model)
        return model

    def request(self, method: str, params: Any = None) -> Any:
        if method == 'get-scene':
            return self.scene
        if method == 'get-model':
            return self._get_model(params['id'])
        if method == 'add-model':
            return [self.add_fake_model()]
        if method == 'update-model':
            return self._update_model(params)
        if method == 'remove-model':
            return self._remove_model(params)
        raise RuntimeError('Test error')

    def _get_model(self, id: int) -> dict:
        return [
            model for model in self.scene['models']
            if model['id'] == id
        ][0]

    def _update_model(self, params: dict) -> None:
        model = self._get_model(params['id'])
        model.update(params)

    def _remove_model(self, params: dict) -> None:
        self.scene['models'] = [
            model for model in self.scene['models']
            if model['id'] not in params['ids']
        ]


class TestScene(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockClient()
        self._scene = Scene(self._client)

    def test_len(self) -> None:
        count = 3
        for _ in range(count):
            self._client.add_fake_model()
        self.assertEqual(len(self._scene), count)

    def test_contains(self) -> None:
        count = 3
        for _ in range(count):
            self._client.add_fake_model()
        self.assertIn(2, self._scene)
        self.assertNotIn(4, self._scene)
        self.assertIn(ModelInstance(self._client, 1), self._scene)

    def test_iter(self) -> None:
        count = 3
        for _ in range(count):
            self._client.add_fake_model()
        self.assertEqual(list(model.id for model in self._scene), [0, 1, 2])

    def test_getitem(self) -> None:
        count = 3
        for _ in range(count):
            self._client.add_fake_model()
        for i in range(count):
            self.assertEqual(self._scene[i].id, i)

    def test_bounds(self) -> None:
        self.assertEqual(
            self._scene.bounds,
            Box.from_dict(self._client.scene['bounds'])
        )

    def test_add(self) -> None:
        instances = self._scene.add(MockModel())
        self.assertEqual(len(instances), 1)
        template = self._client.scene['models'][0]
        model = instances[0]
        self.assertEqual(model.id, template['id'])
        self.assertEqual(model.bounds, Box.from_dict(template['bounds']))
        self.assertEqual(model.metadata, template['metadata'])
        self.assertEqual(model.visible, template['visible'])
        self.assertEqual(model.transform.to_dict(), template['transformation'])

    def test_remove(self) -> None:
        count = 3
        for _ in range(count):
            self._client.add_fake_model()
        self._scene.remove(0)
        self.assertEqual(len(self._scene), 2)
        self.assertIn(2, self._scene)
        self._scene.remove(ModelInstance(self._client, 2))
        self.assertEqual(len(self._scene), 1)

    def test_clear(self) -> None:
        for _ in range(3):
            self._client.add_fake_model()
        self._scene.clear()
        self.assertEqual(len(self._scene), 0)


if __name__ == '__main__':
    unittest.main()
