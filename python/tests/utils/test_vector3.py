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

from brayns.utils.vector3 import Vector3


class TestVector3(unittest.TestCase):

    def test_full(self) -> None:
        test = Vector3.full(0)
        self.assertEqual(list(test), 3 * [0])

    def test_unpack(self) -> None:
        values = [1, 2, 3]
        self.assertEqual(Vector3.unpack(values), Vector3(*values))

    def test_iter(self) -> None:
        values = [1, 2, 3]
        test = Vector3(*values)
        self.assertEqual(list(test), values)
        self.assertEqual([test.x, test.y, test.z], values)

    def test_neg(self) -> None:
        self.assertEqual(-Vector3(1, 2, 3), Vector3(-1, -2, -3))

    def test_abs(self) -> None:
        test = Vector3(1, 2, 3)
        self.assertEqual(abs(test), test.norm)

    def test_add(self) -> None:
        self.assertEqual(Vector3(1, 2, 3) + Vector3(4, 5, 6), Vector3(5, 7, 9))

    def test_sub(self) -> None:
        self.assertEqual(Vector3(4, 2, 7) - Vector3(1, 2, 3), Vector3(3, 0, 4))

    def test_mul(self) -> None:
        self.assertEqual(Vector3(1, 2, 3) * Vector3(3, 4, 2), Vector3(3, 8, 6))
        self.assertEqual(3 * Vector3(1, 2, 3), Vector3(3, 6, 9))
        self.assertEqual(Vector3(1, 2, 3) * 3, Vector3(3, 6, 9))

    def test_div(self) -> None:
        self.assertEqual(
            Vector3(1, 2, 3) / Vector3(1, 2, 4),
            Vector3(1, 1, 0.75)
        )
        self.assertEqual(Vector3(1, 2, 4) / 4, Vector3(0.25, 0.5, 1))
        self.assertEqual(1 / Vector3(1, 2, 4), Vector3(1, 0.5, 0.25))

    def test_square_norm(self) -> None:
        self.assertEqual(Vector3(1, 2, 3).square_norm, 14)

    def test_norm(self) -> None:
        self.assertEqual(Vector3(1, 2, 3).norm, math.sqrt(14))

    def test_normalized(self) -> None:
        test = Vector3(1, 2, 3)
        self.assertAlmostEqual(test.normalized.norm, 1)
        self.assertAlmostEqual(test.normalized * test.norm, test)


if __name__ == '__main__':
    unittest.main()
