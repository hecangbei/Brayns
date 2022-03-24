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
from brayns.utils.box import Box
from brayns.utils.quaternion import Quaternion
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3
from client.mock_client import MockClient


class TestModelInstance(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockClient()
        self._model = ModelInstance(self._client, 0)
        self._transform = Transform(
            translation=Vector3(1, 2, 3),
            rotation=Quaternion(1, 2, 3, 4),
            scale=Vector3(4, 5, 6)
        )

    def test_id(self) -> None:
        self.assertEqual(self._model.id, 0)

    def test_bounds(self) -> None:
        bounds = Box(
            min=Vector3(1, 2, 3),
            max=Vector3(4, 5, 6)
        )
        self._add_result({
            'bounds': {
                'min': bounds.min,
                'max': bounds.max
            }
        })
        self.assertEqual(self._model.bounds, bounds)
        self._check_get()

    def test_metadata(self) -> None:
        metadata = {
            'test1': '1',
            'test2': '2'
        }
        self._add_result({
            'metadata': metadata
        })
        self.assertEqual(self._model.metadata, metadata)
        self._check_get()

    def test_visible(self) -> None:
        self._add_result({'visible': False})
        self.assertFalse(self._model.visible)
        self._check_get()
        self._add_result({})
        self._model.visible = True
        self._check_set({'visible': True})

    def test_transform(self) -> None:
        result = {'transformation': self._transform.to_dict()}
        self._add_result(result)
        self.assertEqual(self._model.transform, self._transform)
        self._check_get()

    def test_translate(self) -> None:
        translation = Vector3(3, 2, 1)
        transform = self._transform.to_dict()
        self._add_result({'transformation': transform})
        self._add_result({})
        self._model.translate(translation)
        expected = self._transform.translate(translation)
        self.assertEqual(self._get_received_transform(), expected.to_dict())

    def test_rotate(self) -> None:
        rotation = Quaternion(4, 5, 6, 7)
        center = Vector3(1, 2, 3)
        transform = self._transform.to_dict()
        self._add_result({'transformation': transform})
        self._add_result({})
        self._model.rotate(rotation, center)
        expected = self._transform.rotate(rotation, center)
        self.assertEqual(self._get_received_transform(), expected.to_dict())

    def _add_result(self, values: dict) -> None:
        message = {'id': self._model.id}
        message.update(values)
        self._client.results.append(message)

    def _check_get(self) -> None:
        self.assertTrue(
            self._client.has_received('get-model', {'id': self._model.id})
        )

    def _check_set(self, values: dict) -> None:
        message = {'id': self._model.id}
        message.update(values)
        self.assertTrue(
            self._client.has_received('update-model', message)
        )

    def _get_received_transform(self) -> dict:
        return self._client.get_last_result()['transformation']


if __name__ == '__main__':
    unittest.main()
