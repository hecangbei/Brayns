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

from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.vector3 import Vector3


class TestQuaternion(unittest.TestCase):

    def test_identity(self) -> None:
        self.assertEqual(Quaternion.identity, Quaternion(0, 0, 0, 1))

    def test_from_euler(self) -> None:
        test = Quaternion.from_euler(Vector3(34, -22, -80), degrees=True)
        ref = Quaternion(0.10256431, -0.32426137, -0.56067163, 0.75497182)
        self.assertAlmostEqual(test, ref)
        self.assertAlmostEqual(test.norm, 1)

    def test_from_axis_angle(self) -> None:
        axis = Vector3(1, 2, 3)
        angle = 30
        test = Quaternion.from_axis_angle(axis, angle, degrees=True)
        ref = Quaternion(0.0691723, 0.1383446, 0.2075169, 0.96592583)
        self.assertAlmostEqual(test.norm, 1)
        self.assertAlmostEqual(test, ref)

    def test_from_vector(self) -> None:
        vector = Vector3(1, 2, 3)
        test = Quaternion.from_vector(vector)
        self.assertEqual(Vector3(test.x, test.y, test.z), vector)

    def test_unpack(self) -> None:
        values = [1, 2, 3, 4]
        self.assertEqual(Quaternion.unpack(values), Quaternion(*values))

    def test_iter(self) -> None:
        values = [1, 2, 3, 4]
        test = Quaternion(*values)
        self.assertEqual(list(test), values)
        self.assertEqual([test.x, test.y, test.z, test.w], values)

    def test_abs(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertEqual(abs(test), test.norm)

    def test_neg(self) -> None:
        self.assertEqual(-Quaternion(1, 2, 3, 4), Quaternion(-1, -2, -3, -4))

    def test_add(self) -> None:
        self.assertEqual(
            Quaternion(1, 2, 3, 4) + Quaternion(5, 6, 7, 8),
            Quaternion(6, 8, 10, 12)
        )

    def test_sub(self) -> None:
        self.assertEqual(
            Quaternion(1, 2, 3, 4) - Quaternion(5, 6, 7, 8),
            Quaternion(-4, -4, -4, -4)
        )

    def test_mul(self) -> None:
        self.assertEqual(Quaternion(1, 2, 3, 4) * 2, Quaternion(2, 4, 6, 8))
        self.assertEqual(2 * Quaternion(1, 2, 3, 4), Quaternion(2, 4, 6, 8))
        test1 = Quaternion(1, 2, 3, 4)
        test2 = Quaternion(5, 6, 7, 8)
        test = test1 * test2
        ref = Quaternion(24, 48, 48, -6)
        self.assertAlmostEqual(test, ref)

    def test_div(self) -> None:
        self.assertEqual(Quaternion(2, 4, 6, 8) / 2, Quaternion(1, 2, 3, 4))
        self.assertAlmostEqual(
            2 / Quaternion(2, 4, 8, 10),
            Quaternion(1, 0.5, 0.25, 0.2)
        )
        test = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(test * test.inverse, Quaternion.identity)

    def test_vector(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertEqual(test.vector, Vector3(1, 2, 3))

    def test_square_norm(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(test.square_norm, 30)

    def test_norm(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(test.norm, math.sqrt(30))

    def test_normalized(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(test.normalized.norm, 1)
        self.assertAlmostEqual(test.normalized * test.norm, test)

    def test_conjugate(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        ref = Quaternion(-1, -2, -3, 4)
        self.assertEqual(test.conjugate, ref)
        self.assertAlmostEqual(
            test * test.conjugate,
            Quaternion(0, 0, 0, test.square_norm)
        )

    def test_inverse(self) -> None:
        test = Quaternion(1, 2, 3, 4)
        self.assertAlmostEqual(test * test.inverse, Quaternion.identity)

    def test_rotate(self) -> None:
        rotation = Quaternion.from_euler(Vector3(22, 35, 68), degrees=True)
        value = Vector3(1, 2, 3)
        ref = Vector3(0.3881471,  2.91087149, 2.31865673)
        self.assertAlmostEqual(rotation.rotate(value), ref)
        center = Vector3(4, 5, 6)
        ref = Vector3(3.77731325, 0.02357039, 4.52163639)
        self.assertAlmostEqual(rotation.rotate(value, center), ref)


if __name__ == '__main__':
    unittest.main()
