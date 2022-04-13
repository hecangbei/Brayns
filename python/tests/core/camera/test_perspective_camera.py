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
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.box import Box
from brayns.core.geometry.vector3 import Vector3


class TestPerspectiveCamera(unittest.TestCase):

    def test_fovy_radians(self) -> None:
        camera = PerspectiveCamera(fovy=math.radians(45))
        self.assertAlmostEqual(camera.fovy_radians, math.radians(45))
        self.assertAlmostEqual(camera.fovy_degrees, 45)

    def test_fovy_degrees(self) -> None:
        camera = PerspectiveCamera(fovy=45, degrees=True)
        self.assertAlmostEqual(camera.fovy_radians, math.radians(45))
        self.assertAlmostEqual(camera.fovy_degrees, 45)

    def test_get_full_screen_distance(self) -> None:
        camera = PerspectiveCamera(fovy=90, degrees=True)
        height = 2
        test = camera.get_full_screen_distance(height)
        self.assertAlmostEqual(test, 1)

    def test_get_default_view(self) -> None:
        camera = PerspectiveCamera(fovy=90, degrees=True)
        target = Box(-Vector3.one, Vector3.one)
        test = camera.get_default_view(target)
        self.assertAlmostEqual(test.position, Axis.forward)
        self.assertAlmostEqual(test.target, Vector3.zero)
        self.assertAlmostEqual(test.up, Axis.up)


if __name__ == '__main__':
    unittest.main()
