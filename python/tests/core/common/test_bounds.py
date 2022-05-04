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

from brayns.core.common.bounds import Bounds
from brayns.core.common.vector3 import Vector3


class TestBounds(unittest.TestCase):

    def setUp(self) -> None:
        self._box = Bounds(
            min=Vector3(1, 2, 3),
            max=Vector3(3, 6, 9)
        )
        self._message = {
            'min': [1, 2, 3],
            'max': [3, 6, 9]
        }

    def test_deserialize(self) -> None:
        test = Bounds.deserialize(self._message)
        self.assertEqual(test, self._box)

    def test_merge(self) -> None:
        tests = [
            Bounds(Vector3.one, 2 * Vector3.one),
            Bounds(-Vector3.one, 2 * Vector3.one),
            Bounds(3 * Vector3.one, 12 * Vector3.one)
        ]
        test = Bounds.merge(tests)
        ref = Bounds(-Vector3.one, 12 * Vector3.one)
        self.assertEqual(test, ref)

    def test_from_size(self) -> None:
        from_size = Bounds.from_size(Vector3.one)
        self.assertEqual(from_size, Bounds.one)
        with_center = Bounds.from_size(Vector3(1, 2, 3), Vector3.one)
        ref = Bounds(Vector3(0.5, 0, -0.5), Vector3(1.5, 2, 2.5))
        self.assertEqual(with_center, ref)

    def test_cube(self) -> None:
        test = Bounds.cube(0.5)
        ref = Bounds.from_size(0.5 * Vector3.one)
        self.assertEqual(test, ref)
        test = Bounds.cube(0.5, Vector3.one)
        ref = ref.with_center(Vector3.one)
        self.assertEqual(test, ref)

    def test_empty(self) -> None:
        self.assertEqual(Bounds.empty, Bounds())

    def test_one(self) -> None:
        one_half = Vector3.full(0.5)
        self.assertEqual(Bounds.one, Bounds(-one_half, one_half))

    def test_post_init(self) -> None:
        with self.assertRaises(ValueError):
            Bounds(Vector3.one, -Vector3.one)

    def test_or(self) -> None:
        test1 = Bounds(-Vector3.one, 2 * Vector3.one)
        test2 = Bounds(Vector3.one, 3 * Vector3.one)
        test = test1 | test2
        ref = Bounds(-Vector3.one, 3 * Vector3.one)
        self.assertEqual(test, ref)

    def test_contains(self) -> None:
        test = Bounds.one
        self.assertIn(Vector3.zero, test)
        self.assertNotIn(Vector3(0, 0, 2), test)
        self.assertIn(Bounds.cube(0.5), test)
        self.assertNotIn(Bounds.cube(0.5, Vector3.one), test)

    def test_center(self) -> None:
        self.assertEqual(self._box.center, Vector3(2, 4, 6))

    def test_size(self) -> None:
        self.assertEqual(self._box.size, Vector3(2, 4, 6))

    def test_width(self) -> None:
        self.assertEqual(self._box.width, 2)

    def test_height(self) -> None:
        self.assertEqual(self._box.height, 4)

    def test_depth(self) -> None:
        self.assertEqual(self._box.depth, 6)

    def test_serialize(self) -> None:
        test = self._box.serialize()
        self.assertEqual(test, self._message)

    def test_with_min(self) -> None:
        test = Bounds.cube(4).with_min(Vector3.one)
        ref = Bounds(Vector3.one, 2 * Vector3.one)
        self.assertEqual(test, ref)

    def test_with_max(self) -> None:
        test = Bounds.cube(4).with_max(Vector3.one)
        ref = Bounds(-2 * Vector3.one, Vector3.one)
        self.assertEqual(test, ref)

    def test_with_size(self) -> None:
        test = Bounds.one.with_size(2 * Vector3.one)
        ref = Bounds(-Vector3.one, Vector3.one)
        self.assertEqual(test, ref)

    def test_with_center(self) -> None:
        test = Bounds.one.with_center(Vector3.one)
        ref = Bounds(Vector3.one * 0.5, Vector3.one * 1.5)
        self.assertEqual(test, ref)

    def test_translate(self) -> None:
        test = Bounds.one.translate(Vector3.one)
        ref = Bounds(Vector3.one * 0.5, Vector3.one * 1.5)
        self.assertEqual(test, ref)

    def test_rescale(self) -> None:
        test = Bounds.one.rescale(3 * Vector3.one)
        ref = Bounds.cube(3)
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
