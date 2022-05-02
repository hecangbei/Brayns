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

from brayns.core.common.plane import Plane
from brayns.core.common.quaternion import Quaternion
from brayns.core.common.vector3 import Vector3


class TestPlane(unittest.TestCase):

    def test_horizonal(self) -> None:
        self.assertEqual(Plane.horizonal, Plane(Vector3.up))

    def test_front(self) -> None:
        self.assertEqual(Plane.front, Plane(Vector3.forward))

    def test_side(self) -> None:
        self.assertEqual(Plane.side, Plane(Vector3.right))

    def test_serialize(self) -> list[float]:
        plane = Plane(Vector3(1, 2, 3), 4)
        test = plane.serialize()
        ref = [1, 2, 3, 4]
        self.assertEqual(test, ref)

    def test_with_distance(self) -> None:
        plane = Plane(Vector3.one)
        test = plane.with_distance(0.5)
        ref = Plane(Vector3.one, 0.5)
        self.assertEqual(test, ref)

    def test_translate(self) -> None:
        plane = Plane(Vector3.one)
        test = plane.translate(0.5)
        ref = Plane(Vector3.one, 0.5)
        self.assertEqual(test, ref)

    def test_with_normal(self) -> None:
        plane = Plane(Vector3.one)
        test = plane.with_normal(Vector3.right)
        ref = Plane(Vector3.right)
        self.assertEqual(test, ref)

    def test_rotate(self) -> None:
        plane = Plane(Vector3.up)
        rotation = Quaternion.from_axis_angle(Vector3.right, 90, degrees=True)
        test = plane.rotate(rotation)
        ref = Plane(Vector3.forward)
        self.assertEqual(test.distance, ref.distance)
        self.assertAlmostEqual(test.normal.x, ref.normal.x)
        self.assertAlmostEqual(test.normal.y, ref.normal.y)
        self.assertAlmostEqual(test.normal.z, ref.normal.z)


if __name__ == '__main__':
    unittest.main()
