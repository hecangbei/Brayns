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

from brayns.common.geometry.quaternion import Quaternion
from brayns.common.geometry.transform import Transform
from brayns.common.geometry.vector3 import Vector3
from brayns.instance.scene.model_instance import ModelInstance
from tests.instance.scene.mock_scene_client import MockSceneClient


class TestModelInstance(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._mock = self._client.add_model()
        self._model = ModelInstance(self._client, self._mock.id)

    def test_id(self) -> None:
        self.assertEqual(self._model.id, self._mock.id)

    def test_bounds(self) -> None:
        self.assertEqual(self._model.bounds, self._mock.bounds)

    def test_metadata(self) -> None:
        self.assertEqual(self._model.metadata, self._mock.metadata)

    def test_visible(self) -> None:
        self._mock.visible = True
        self.assertTrue(self._model.visible)
        self._model.visible = False
        self.assertFalse(self._mock.visible)

    def test_transform(self) -> None:
        self.assertEqual(self._model.transform, self._mock.transform)
        transform = Transform(
            translation=Vector3(1, 2, 3),
            rotation=Quaternion(1, 2, 3, 4),
            scale=Vector3(4, 5, 6)
        )
        self._model.transform = transform
        self.assertEqual(self._mock.transform, transform)

    def test_translation(self) -> None:
        self.assertEqual(
            self._model.translation,
            self._mock.transform.translation
        )
        test = Vector3.one()
        self._model.translation = test
        self.assertEqual(self._mock.transform.translation, test)

    def test_rotation(self) -> None:
        self.assertEqual(
            self._model.rotation,
            self._mock.transform.rotation
        )
        test = Quaternion.from_euler(
            Vector3(0, 0, 90),
            degrees=True
        )
        self._model.rotation = test
        self.assertEqual(self._mock.transform.rotation, test)

    def test_scale(self) -> None:
        self.assertEqual(
            self._model.scale,
            self._mock.transform.scale
        )
        test = 2 * Vector3.one()
        self._model.scale = test
        self.assertEqual(self._mock.transform.scale, test)


if __name__ == '__main__':
    unittest.main()
