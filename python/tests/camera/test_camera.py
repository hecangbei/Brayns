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

from brayns.camera.camera import Camera
from brayns.geometry.box import Box
from brayns.geometry.quaternion import Quaternion
from brayns.geometry.vector3 import Vector3
from tests.camera.mock_camera_client import MockCameraClient
from tests.camera.mock_camera_projection import MockCameraProjection


class TestCamera(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._camera = Camera(self._client)

    def test_view(self) -> None:
        self.assertEqual(self._camera.view, self._client.camera)

    def test_position(self) -> None:
        self.assertEqual(self._camera.position, self._client.camera.position)
        position = Vector3(1, 2, 3)
        self._camera.position = position
        self.assertEqual(self._client.camera.position, position)

    def test_target(self) -> None:
        self.assertEqual(self._camera.target, self._client.camera.target)
        target = Vector3(1, 2, 3)
        self._camera.target = target
        self.assertEqual(self._client.camera.target, target)

    def test_up(self) -> None:
        self.assertEqual(self._camera.up, self._client.camera.up)
        up = Vector3(1, 2, 3)
        self._camera.up = up
        self.assertEqual(self._client.camera.up, up)

    def test_set_projection(self) -> None:
        projection = MockCameraProjection()
        self._camera.set_projection(projection)
        self.assertEqual(self._client.projection_name, projection.get_name())
        self.assertEqual(
            self._client.projection_properties,
            projection.get_properties()
        )

    def test_reset(self) -> None:
        self._camera.reset()
        self.assertEqual(self._camera.position, Vector3.zero())
        self.assertEqual(self._camera.target, Vector3.zero())
        self.assertEqual(self._camera.up, Vector3.up())

    def test_rotate_around_target(self) -> None:
        self._camera.target = Vector3(1, 1, 0)
        rotation = Quaternion.from_euler(Vector3(0, 0, 180), degrees=True)
        self._camera.rotate(rotation)
        self.assertAlmostEqual(self._camera.position, Vector3(2, 2, 0))


if __name__ == '__main__':
    unittest.main()
