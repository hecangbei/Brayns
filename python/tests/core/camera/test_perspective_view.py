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

from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.camera.perspective_view import PerspectiveView
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.box import Box
from brayns.core.geometry.vector3 import Vector3
from brayns.core.geometry.view import View


class TestPerspectiveView(unittest.TestCase):

    def test_get_full_screen_distance(self) -> None:
        view = PerspectiveView()
        camera = PerspectiveCamera(fovy=90, degrees=True)
        height = 2
        test = view.get_full_screen_distance(camera, height)
        self.assertAlmostEqual(test, 1)

    def test_get_default_view(self) -> None:
        view = PerspectiveView()
        camera = PerspectiveCamera(fovy=90, degrees=True)
        target = Box(-Vector3.one, Vector3.one)
        test = view.get_full_screen_view(camera, target)
        self.assertAlmostEqual(test.position, Axis.forward)
        self.assertAlmostEqual(test.target, Vector3.zero)
        self.assertAlmostEqual(test.up, Axis.up)

    def test_get_default_view_adjusted(self) -> None:
        view = PerspectiveView()
        camera = PerspectiveCamera(fovy=90, degrees=True)
        target = Box(-Vector3.one, Vector3.one)
        translation = Axis.left
        rotation = View.left
        test = view.get_full_screen_view(camera, target, translation, rotation)
        self.assertAlmostEqual(test.position, Vector3(-1, 0, -1))
        self.assertAlmostEqual(test.target, Vector3.zero)
        self.assertAlmostEqual(test.up, Axis.up)


if __name__ == '__main__':
    unittest.main()
