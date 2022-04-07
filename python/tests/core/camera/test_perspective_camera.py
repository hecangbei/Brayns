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

import math
import unittest

from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.geometry.box import Box
from brayns.core.geometry.vector3 import Vector3


class TestPerspectiveProjection(unittest.TestCase):

    def test_get_name(self) -> None:
        camera = PerspectiveCamera()
        test1 = camera.get_name()
        self.assertEqual(test1, 'perspective')
        test2 = PerspectiveCamera.get_name()
        self.assertEqual(test2, test1)

    def test_from_dict(self) -> None:
        message = {
            'fovy': 45,
            'aperture_radius': 0,
            'focus_distance': 1
        }
        test = PerspectiveCamera.from_dict(message)
        self.assertEqual(test.fovy_degrees, 45)
        self.assertEqual(test.aperture_radius, 0)
        self.assertEqual(test.focus_distance, 1)

    def test_fovy_radians(self) -> None:
        camera = PerspectiveCamera(math.radians(60))
        self.assertEqual(camera.fovy_radians, math.radians(60))
        camera.fovy_radians = math.radians(45)
        self.assertEqual(camera.fovy_radians, math.radians(45))

    def test_fovy_degrees(self) -> None:
        camera = PerspectiveCamera(60, degrees=True)
        self.assertAlmostEqual(camera.fovy_degrees, 60)
        camera.fovy_degrees = 45
        self.assertAlmostEqual(camera.fovy_degrees, 45)

    def test_to_dict(self) -> None:
        camera = PerspectiveCamera(45, 0, 1, degrees=True)
        ref = {
            'fovy': 45,
            'aperture_radius': 0,
            'focus_distance': 1
        }
        test = camera.to_dict()
        self.assertEqual(test, ref)

    def test_get_full_screen_distance(self) -> None:
        bounds = Box(-Vector3.one, Vector3.one)


if __name__ == '__main__':
    unittest.main()
