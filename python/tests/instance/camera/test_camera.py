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

from brayns.common.geometry.vector3 import Vector3
from brayns.instance.camera.camera import Camera
from brayns.instance.camera.camera_view import CameraView
from tests.instance.camera.mock_camera_client import MockCameraClient


class TestCamera(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._camera = Camera(self._client)

    def test_name(self) -> None:
        self._client.name = 'test'
        self.assertEqual(self._camera.name, self._client.name)

    def test_view(self) -> None:
        self.assertEqual(self._camera.view, self._client.view)
        test = CameraView(
            position=3 * Vector3.one(),
            target=2*Vector3.one(),
            up=Vector3.left()
        )
        self._camera.view = test
        self.assertEqual(self._client.view, test)

    def test_position(self) -> None:
        test = Vector3.one()
        self._client.view = CameraView(position=test)
        self.assertEqual(self._camera.position, test)
        test *= 3
        self._camera.position = test
        self.assertEqual(self._client.view.position, test)

    def test_target(self) -> None:
        test = Vector3.one()
        self._client.view = CameraView(target=test)
        self.assertEqual(self._camera.target, test)
        test *= 3
        self._camera.target = test
        self.assertEqual(self._client.view.target, test)

    def test_up(self) -> None:
        test = Vector3.one()
        self._client.view = CameraView(up=test)
        self.assertEqual(self._camera.up, test)
        test *= 3
        self._camera.up = test
        self.assertEqual(self._client.view.up, test)

    def test_direction(self) -> None:
        self._client.view = CameraView(-Vector3.one(), Vector3.one())
        self.assertEqual(self._camera.direction, 2 * Vector3.one())

    def test_update(self) -> None:
        self._camera.update('test', {'test': 1})
        self.assertEqual(self._client.name, 'test')
        self.assertEqual(self._client.properties, {'test': 1})


if __name__ == '__main__':
    unittest.main()
