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


if __name__ == '__main__':
    unittest.main()
