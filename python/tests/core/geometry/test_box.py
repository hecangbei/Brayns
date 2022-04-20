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

from brayns.core.geometry.box import Box
from brayns.core.geometry.vector3 import Vector3


class TestBox(unittest.TestCase):

    def setUp(self) -> None:
        self._box = Box(
            min=Vector3(1, 2, 3),
            max=Vector3(3, 6, 9)
        )

    def test_deserialize(self) -> None:
        message = {
            'min': [1, 2, 3],
            'max': [3, 6, 9]
        }
        test = Box.deserialize(message)
        self.assertEqual(test, self._box)

    def test_empty(self) -> None:
        test = Box.empty
        self.assertEqual(test.min, Vector3.zero)
        self.assertEqual(test.max, Vector3.zero)

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


if __name__ == '__main__':
    unittest.main()
