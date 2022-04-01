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
from brayns.camera.camera_view import CameraView
from brayns.camera.projection_registry import ProjectionRegistry
from brayns.geometry.box import Box
from brayns.geometry.vector3 import Vector3
from tests.camera.mock_camera_client import MockCameraClient
from tests.camera.mock_camera_projection import MockCameraProjection


class TestCamera(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        projections = ProjectionRegistry(self._client)
        projections.add_projection_type(MockCameraProjection())
        self._camera = Camera(self._client, projections)

    def test_view_get(self) -> None:
        self.assertEqual(self._camera.view, self._client.view)

    def test_view_set(self) -> None:
        test = CameraView(position=3 * Vector3.one())
        self._camera.view = test
        self.assertEqual(self._camera.view, test)

    def test_projection_get(self) -> None:
        projection = self._camera.projection
        self.assertEqual(projection.to_dict(), self._client.projection)
        self.assertEqual(projection.get_name(), self._client.name)

    def test_projection_set(self) -> None:
        test = MockCameraProjection(3, 4)
        self._camera.projection = test
        projection = self._camera.projection
        self.assertEqual(projection.to_dict(), test.to_dict())
        self.assertEqual(projection.get_name(), test.get_name())

    def test_name(self) -> None:
        self.assertEqual(self._camera.name, self._client.name)

    def test_position(self) -> None:
        self.assertEqual(self._camera.position, self._client.view.position)
        position = Vector3(1, 2, 3)
        self._camera.position = position
        self.assertEqual(self._client.view.position, position)

    def test_target(self) -> None:
        self.assertEqual(self._camera.target, self._client.view.target)
        target = Vector3(1, 2, 3)
        self._camera.target = target
        self.assertEqual(self._client.view.target, target)

    def test_up(self) -> None:
        self.assertEqual(self._camera.up, self._client.view.up)
        up = Vector3(1, 2, 3)
        self._camera.up = up
        self.assertEqual(self._client.view.up, up)

    def test_get_full_screen_distance(self) -> None:
        test = Box(Vector3.zero(), Vector3.one())
        distance = self._camera.get_full_screen_distance(test)
        ref = self._camera.projection.get_full_screen_distance(test)
        self.assertEqual(distance, ref)


if __name__ == '__main__':
    unittest.main()
