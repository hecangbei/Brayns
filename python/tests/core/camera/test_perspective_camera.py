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


class TestPerspectiveCamera(unittest.TestCase):

    def test_fovy_radians(self) -> None:
        fovy = math.radians(45)
        camera = PerspectiveCamera(fovy)
        self.assertEqual(camera.fovy_radians, fovy)

    def test_fovy_degrees(self) -> None:
        fovy = 45
        camera = PerspectiveCamera(fovy, degrees=True)
        self.assertEqual(camera.fovy_degrees, fovy)

    def test_get_full_screen_distance(self) -> None:
        camera = PerspectiveCamera(90, degrees=True)
        test = camera.get_full_screen_distance(2)
        self.assertAlmostEqual(test, 1)


if __name__ == '__main__':
    unittest.main()
