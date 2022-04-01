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
from brayns.camera.camera_controller import CameraController
from brayns.camera.projection_registry import ProjectionRegistry
from brayns.geometry.box import Box
from brayns.geometry.quaternion import Quaternion
from brayns.geometry.vector3 import Vector3
from tests.camera.mock_camera_client import MockCameraClient
from tests.camera.mock_camera_projection import MockCameraProjection


class TestCameraController(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        projections = ProjectionRegistry(self._client)
        projections.add_projection_type(MockCameraProjection)
        self._camera = Camera(self._client, projections)
        self._controller = CameraController(self._camera)

    def test_reset(self) -> None:
        self._controller.reset()
        self.assertEqual(self._camera.position, Vector3.zero())
        self.assertEqual(self._camera.target, Vector3.zero())
        self.assertEqual(self._camera.up, Vector3.up())

    def test_translate(self) -> None:
        ref = self._camera.position
        translation = Vector3.one()
        self._controller.translate(translation)
        self.assertEqual(self._camera.position, ref + translation)

    def test_rotate_around_target(self) -> None:
        self._camera.target = Vector3(1, 1, 0)
        rotation = Quaternion.from_euler(Vector3(0, 0, 180), degrees=True)
        self._controller.rotate_around_target(rotation)
        self.assertAlmostEqual(self._camera.position, Vector3(2, 2, 0))

    def test_look_at(self) -> None:
        test = Box(-Vector3.one(), Vector3.one())
        distance = self._camera.get_full_screen_distance(test)
        self._controller.look_at(test)
        self.assertEqual(self._camera.position, distance * Vector3.forward())


if __name__ == '__main__':
    unittest.main()
