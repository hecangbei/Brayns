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

from brayns.instance.camera.perspective_projection import PerspectiveProjection
from brayns.common.geometry.box import Box
from brayns.common.geometry.vector3 import Vector3


class TestPerspectiveProjection(unittest.TestCase):

    def test_get_name(self) -> None:
        self.assertEqual(PerspectiveProjection.get_name(), 'perspective')

    def test_from_dict(self) -> None:
        ref = {
            'fovy': 45,
            'aperture_radius': 0,
            'focus_distance': 1
        }
        projection = PerspectiveProjection.from_dict(ref)
        self.assertEqual(projection.fovy_degrees, 45)
        self.assertEqual(projection.aperture_radius, 0)
        self.assertEqual(projection.focus_distance, 1)

    def test_to_dict(self) -> None:
        ref = {
            'fovy': 45,
            'aperture_radius': 1.5,
            'focus_distance': 5.5
        }
        projection = PerspectiveProjection.from_dict(ref)
        self.assertEqual(projection.to_dict(), ref)

    def test_get_full_screen_distance(self) -> None:
        projection = PerspectiveProjection(90, degrees=True)
        test = Box(-Vector3.one(), Vector3.one())
        distance = projection.get_full_screen_distance(test)
        self.assertAlmostEqual(distance, 1)


if __name__ == '__main__':
    unittest.main()
