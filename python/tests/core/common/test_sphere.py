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

from brayns.core.common.sphere import Sphere
from brayns.core.common.vector3 import Vector3


class TestSphere(unittest.TestCase):

    def test_one(self) -> None:
        test = Sphere.one
        ref = Sphere(1)
        self.assertEqual(test, ref)

    def test_serialize(self) -> None:
        sphere = Sphere(2, Vector3.one)
        test = sphere.serialize()
        ref = {
            'center': [1, 1, 1],
            'radius': 2
        }
        self.assertEqual(test, ref)

    def test_with_center(self) -> None:
        sphere = Sphere.one
        test = sphere.with_center(Vector3.one)
        ref = Sphere(1, Vector3.one)
        self.assertEqual(test, ref)

    def test_with_radius(self) -> None:
        sphere = Sphere(1, Vector3.one)
        test = sphere.with_radius(3)
        ref = Sphere(3, Vector3.one)
        self.assertEqual(test, ref)

    def test_translate(self) -> None:
        sphere = Sphere.one
        test = sphere.translate(Vector3.one)
        ref = Sphere(1, Vector3.one)
        self.assertEqual(test, ref)

    def test_rescale(self) -> None:
        sphere = Sphere(1, Vector3.one)
        test = sphere.rescale(3)
        ref = Sphere(3, Vector3.one)
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
