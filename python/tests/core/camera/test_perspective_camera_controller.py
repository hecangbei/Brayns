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

from brayns.core.camera.camera_type import CameraType
from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.camera.perspective_camera_controller import PerspectiveCameraController
from brayns.core.geometry.box import Box
from brayns.core.geometry.vector3 import Vector3
from brayns.core.serializers.perspective_camera_serializer import PerspectiveCameraSerializer
from tests.core.camera.mock_camera_client import MockCameraClient


class TestPerspectiveCameraController(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._controller = PerspectiveCameraController(self._client)
        self._serializer = PerspectiveCameraSerializer()
        self._target = Box(-Vector3.one, Vector3.one)
        self._camera = PerspectiveCamera(90, degrees=True, focus_distance=3)

    def test_center_camera(self) -> None:
        self._client.name = CameraType.PERSPECTIVE.value
        self._client.properties = self._serializer.serialize(self._camera)
        self._controller.center_camera(self._target, self._camera)
        test = self._client.view
        ref = self._camera.get_default_view(self._target)
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
