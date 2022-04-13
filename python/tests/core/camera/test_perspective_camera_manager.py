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

from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.camera.perspective_camera_manager import PerspectiveCameraManager
from tests.core.camera.mock_camera_client import MockCameraClient


class TestPerspectiveCameraManager(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._manager = PerspectiveCameraManager(self._client)

    def test_get_camera(self) -> None:
        self._client.name = 'perspective'
        self._client.properties = {
            'fovy': 30,
            'aperture_radius': 3.0,
            'focus_distance': 2.0
        }
        camera = self._manager.get_camera()
        self.assertAlmostEqual(camera.fovy_degrees, 30)
        self.assertAlmostEqual(camera.aperture_radius, 3.0)
        self.assertAlmostEqual(camera.focus_distance, 2.0)

    def test_set_camera(self) -> None:
        self._client.name = 'perspective'
        camera = PerspectiveCamera(
            fovy=30,
            degrees=True
        )
        self._manager.set_camera(camera)
        properties = self._client.properties
        self.assertAlmostEqual(properties['fovy'], 30)
        self.assertAlmostEqual(properties['aperture_radius'], 0)
        self.assertAlmostEqual(properties['focus_distance'], 1)


if __name__ == '__main__':
    unittest.main()
