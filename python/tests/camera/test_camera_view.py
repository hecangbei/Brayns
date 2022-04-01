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

from brayns.camera.camera_view import CameraView
from brayns.geometry.vector3 import Vector3


class TestCameraView(unittest.TestCase):

    def setUp(self) -> None:
        self._view = CameraView(
            Vector3(1, 2, 3),
            Vector3(4, 5, 6),
            Vector3(7, 8, 9)
        )
        self._message = {
            'position': [1, 2, 3],
            'target': [4, 5, 6],
            'up': [7, 8, 9]
        }

    def test_from_dict(self) -> None:
        self.assertEqual(CameraView.from_dict(self._message), self._view)

    def test_to_dict(self) -> None:
        self.assertEqual(self._view.to_dict(), self._message)

    def test_update(self, **kwargs) -> None:
        view = CameraView()
        position = Vector3(1, 2, 3)
        test = view.update(position=position)
        self.assertEqual(test.position, position)


if __name__ == '__main__':
    unittest.main()
