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
from brayns.common.geometry.box import Box
from brayns.common.geometry.quaternion import Quaternion
from brayns.common.geometry.transform import Transform
from brayns.common.geometry.vector3 import Vector3
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
        self.assertEqual(self._model.visible, self._mock.visible)
        self._model.visible = False
        self.assertFalse(self._model.visible)

    def test_transform(self) -> None:
        self.assertEqual(self._model.transform, self._mock.transform)
        transform = Transform(
            translation=Vector3(1, 2, 3),
            rotation=Quaternion(1, 2, 3, 4),
            scale=Vector3(4, 5, 6)
        )
        self._model.transform = transform
        self.assertEqual(self._model.transform, transform)

    def test_position(self) -> None:
        self.assertEqual(self._model.position, self._mock.bounds.center)
        position = Vector3(1, 2, 3)
        self._model.position = position
        self.assertEqual(self._model.position, position)

    def test_orientation(self) -> None:
        self.assertEqual(
            self._model.orientation,
            self._mock.transform.rotation
        )
        orientation = Quaternion(1, 2, 3, 4)
        self._model.orientation = orientation
        self.assertEqual(self._model.orientation, orientation)

    def test_translate(self) -> None:
        ref = self._model.transform.translation
        translation = Vector3(1, 2, 3)
        self._model.translate(translation)
        self.assertEqual(self._model.transform.translation, ref + translation)

    def test_rotate(self) -> None:
        rotation = Quaternion(4, 5, 6, 7)
        center = Vector3(1, 2, 3)
        orientation = self._model.transform.rotation
        translation = self._model.transform.translation
        self._model.rotate(rotation)
        self.assertAlmostEqual(
            self._model.transform.translation,
            rotation.rotate(translation)
        )
        self.assertAlmostEqual(
            self._model.transform.rotation,
            rotation * orientation
        )
        self._model.rotate(rotation.inverse)
        self._model.rotate(rotation, center)
        self.assertAlmostEqual(
            self._model.transform.translation,
            rotation.rotate(translation, center)
        )
        self.assertAlmostEqual(
            self._model.transform.rotation,
            rotation * orientation
        )

    def test_rescale(self) -> None:
        scale = Vector3(1, 2, 3)
        ref = self._model.transform.scale
        self._model.rescale(scale)
        self.assertEqual(self._model.transform.scale, ref * scale)


if __name__ == '__main__':
    unittest.main()
