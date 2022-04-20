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

from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.vector3 import Vector3
from tests.core.camera.mock_camera_instance import MockCameraInstance


class TestCameraView(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockCameraInstance()
        self._instance.view = CameraView(
            position=Vector3.one,
            target=2 * Vector3.one,
            up=Axis.right
        )

    def test_from_instance(self) -> None:
        view = CameraView.from_instance(self._instance)
        self.assertEqual(view, self._instance.view)
        self.assertEqual(self._instance.method, 'get-camera-look-at')
        self.assertEqual(self._instance.params, None)

    def test_deserialize(self) -> None:
        test = {
            'position': [1, 2, 3],
            'target': [4, 5, 6],
            'up': [7, 8, 9]
        }
        view = CameraView.deserialize(test)
        self.assertEqual(view.position, Vector3(1, 2, 3))
        self.assertEqual(view.target, Vector3(4, 5, 6))
        self.assertEqual(view.up, Vector3(7, 8, 9))

    def test_use_for_main_camera(self) -> None:
        view = CameraView()
        view.use_for_main_camera(self._instance)
        self.assertEqual(self._instance.view, view)
        self.assertEqual(self._instance.method, 'set-camera-look-at')
        self.assertEqual(self._instance.params, view.serialize())

    def test_serialize(self) -> None:
        view = CameraView()
        test = view.serialize()
        ref = {
            'position': [0, 0, 0],
            'target': [0, 0, 0],
            'up': [0, 1, 0]
        }
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
