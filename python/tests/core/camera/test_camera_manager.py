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
from brayns.core.camera.camera_type import CameraType
from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.vector3 import Vector3
from tests.core.camera.mock_camera_client import MockCameraClient


class TestCameraManager(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._manager = CameraManager(self._client)

    def test_get_camera_type(self) -> None:
        self._client.name = CameraType.PERSPECTIVE.value
        test = self._manager.get_camera_type()
        self.assertEqual(test, CameraType.PERSPECTIVE)

    def test_get_camera_view(self) -> None:
        self._client.view = CameraView(
            position=Vector3.one,
            target=Vector3.zero,
            up=Axis.right
        )
        test = self._manager.get_camera_view()
        ref = self._client.view
        self.assertEqual(test, ref)

    def test_set_camera_view(self) -> None:
        test = CameraView(
            position=Vector3.one,
            target=Vector3.zero,
            up=Axis.right
        )
        self._manager.set_camera_view(test)
        ref = self._client.view
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
