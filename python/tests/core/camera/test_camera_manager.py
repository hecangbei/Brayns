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

from brayns.core.camera.camera_manager import CameraManager
from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.vector3 import Vector3
from tests.core.camera.mock_camera import MockCamera
from tests.core.camera.mock_camera_client import MockCameraClient


class TestCameraManager(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._manager = CameraManager(self._client)

    def test_get_camera_name(self) -> None:
        test = self._manager.get_camera_name()
        ref = self._client.name
        self.assertEqual(test, ref)

    def test_get_camera(self) -> None:
        camera = MockCamera()
        self._client.name = camera.get_name()
        self._client.properties = camera.to_dict()
        test = self._manager.get_camera(MockCamera)
        ref = self._client.properties
        self.assertEqual(test.to_dict(), ref)

    def test_set_camera(self) -> None:
        camera = MockCamera()
        self._manager.set_camera(camera)
        self.assertEqual(self._client.name, camera.get_name())
        self.assertEqual(self._client.properties, camera.to_dict())

    def test_get_camera_view(self) -> None:
        ref = CameraView(
            position=Vector3.one,
            target=3*Vector3.one,
            up=Vector3.right
        )
        self._client.view = ref
        test = self._manager.get_camera_view()
        self.assertEqual(test, ref)

    def test_set_camera_view(self) -> None:
        ref = CameraView(
            position=Vector3.one,
            target=3*Vector3.one,
            up=Vector3.right
        )
        self._manager.set_camera_view(ref)
        test = self._client.view
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
