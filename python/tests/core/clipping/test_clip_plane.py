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

from brayns.core.clipping.clip_plane import ClipPlane
from brayns.core.common.plane import Plane
from brayns.core.common.vector3 import Vector3
from tests.core.clipping.mock_clipping_instance import MockClippingInstance


class TestClipPlane(unittest.TestCase):

    def test_remove(self) -> None:
        instance = MockClippingInstance()
        ids = [1, 2, 3]
        ClipPlane.remove(instance, ids)
        self.assertEqual(instance.method, 'remove-clip-planes')
        self.assertEqual(instance.params, {'ids': ids})

    def test_add(self) -> None:
        instance = MockClippingInstance()
        plane = Plane(Vector3(1, 2, 3), 4)
        test = ClipPlane.add(instance, plane)
        self.assertEqual(test.id, instance.id)
        self.assertEqual(test.plane, plane)
        self.assertEqual(instance.method, 'add-clip-plane')
        self.assertEqual(instance.params, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
