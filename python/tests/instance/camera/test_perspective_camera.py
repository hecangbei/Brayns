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

from brayns.instance.camera.perspective_camera import PerspectiveCamera


class TestPerspectiveProjection(unittest.TestCase):

    def setUp(self) -> None:
        self._camera = PerspectiveCamera()

    def test_fovy_radians(self) -> None:
        camera = PerspectiveCamera(math.radians(60))
        self.assertEqual(camera.fovy_radians, math.radians(60))

    def test_fovy_degrees(self) -> None:
        camera = PerspectiveCamera(60, degrees=True)
        self.assertAlmostEqual(camera.fovy_degrees, 60)

    def test_aperture_radius(self) -> None:
        camera = PerspectiveCamera(aperture_radius=1.5)
        self.assertEqual(camera.aperture_radius, 1.5)

    def test_focus_distance(self) -> None:
        camera = PerspectiveCamera(focus_distance=1.5)
        self.assertEqual(camera.focus_distance, 1.5)

    def test_get_name(self) -> None:
        camera = PerspectiveCamera()
        self.assertEqual(camera.get_name(), 'perspective')

    def test_get_properties(self) -> None:
        camera = PerspectiveCamera()
        ref = {
            'fovy': 45,
            'aperture_radius': 0,
            'focus_distance': 1
        }
        self.assertEqual(camera.get_properties(), ref)


if __name__ == '__main__':
    unittest.main()
