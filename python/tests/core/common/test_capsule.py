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

from brayns.core.common.capsule import Capsule
from brayns.core.common.quaternion import Quaternion
from brayns.core.common.vector3 import Vector3


class TestCapsule(unittest.TestCase):

    def test_center(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.center
        ref = Vector3.one / 2
        self.assertEqual(test, ref)

    def test_serialize(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.serialize()
        ref = {
            'p0': [0, 0, 0],
            'r0': 1,
            'p1': [1, 1, 1],
            'p1': 2
        }
        self.assertEqual(test, ref)

    def test_with_start_point(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.with_start_point(Vector3.one / 2)
        ref = Capsule(Vector3.one / 2, 1, Vector3.one, 2)
        self.assertEqual(test, ref)

    def test_with_start_radius(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.with_start_radius(2)
        ref = Capsule(Vector3.zero, 2, Vector3.one, 2)
        self.assertEqual(test, ref)

    def test_with_end_point(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.with_end_point(Vector3.one / 2)
        ref = Capsule(Vector3.zero, 1, Vector3.one / 2, 2)
        self.assertEqual(test, ref)

    def test_with_end_radius(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.with_end_radius(1)
        ref = Capsule(Vector3.zero, 1, Vector3.one, 1)
        self.assertEqual(test, ref)

    def test_with_radius(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.with_radius(3)
        ref = Capsule(Vector3.zero, 3, Vector3.one, 3)
        self.assertEqual(test, ref)

    def test_translate(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.translate(Vector3.one)
        ref = Capsule(Vector3.one, 1, 2 * Vector3.one, 2)
        self.assertEqual(test, ref)

    def test_rotate(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        rotation = Quaternion.from_axis_angle(Vector3.up, 90, degrees=True)
        test = capsule.rotate(rotation)
        self.assertEqual(test.start_point, Vector3.zero)
        self.assertEqual(test.start_radius, 1)
        self.assertAlmostEqual(test.end_point.x, 1)
        self.assertAlmostEqual(test.end_point.y, 1)
        self.assertAlmostEqual(test.end_point.z, -1)
        self.assertEqual(test.end_radius, 2)

    def test_multiply_radius(self) -> None:
        capsule = Capsule(Vector3.zero, 1, Vector3.one, 2)
        test = capsule.multiply_radius(3)
        ref = Capsule(Vector3.zero, 3, Vector3.one, 6)
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
