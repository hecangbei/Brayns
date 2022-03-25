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

from brayns.utils.quaternion import Quaternion
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3


class TestTransform(unittest.TestCase):

    def setUp(self) -> None:
        self._transform = Transform(
            translation=Vector3(1, 2, 3),
            rotation=Quaternion(1, 2, 3, 4),
            scale=Vector3(1, 1, 1)
        )
        self._template = {
            'translation': [1, 2, 3],
            'scale': [1, 1, 1],
            'rotation': [1, 2, 3, 4],
            'rotation_center': [1, 2, 3]
        }

    def test_from_dict(self) -> None:
        self.assertEqual(Transform.from_dict(self._template), self._transform)

    def test_to_dict(self) -> None:
        self.assertEqual(self._transform.to_dict(), self._template)

    def test_update(self) -> None:
        translation = Vector3(3, 2, 1)
        transform = self._transform.update(translation=translation)
        self.assertEqual(transform.translation, translation)
        self.assertEqual(transform.rotation, self._transform.rotation)
        self.assertEqual(transform.scale, self._transform.scale)

    def test_translate(self) -> None:
        translation = Vector3(1, 2, 3)
        transform = self._transform.translate(translation)
        self.assertEqual(
            transform.translation,
            self._transform.translation + translation
        )
        self.assertEqual(transform.rotation, self._transform.rotation)
        self.assertEqual(transform.scale, self._transform.scale)

    def test_rotate(self) -> None:
        rotation = Quaternion.from_euler(Vector3(90, 0, 0), degrees=True)
        center = Vector3(4, 5, 6)
        transform = self._transform.rotate(rotation, center)
        self.assertEqual(
            transform.rotation,
            rotation * self._transform.rotation
        )
        self.assertEqual(
            transform.translation,
            rotation.rotate(self._transform.translation, center)
        )
        self.assertEqual(transform.scale, self._transform.scale)

    def test_rescale(self) -> None:
        scale = Vector3(1, 2, 3)
        transform = self._transform.rescale(scale)
        self.assertEqual(transform.translation, self._transform.translation)
        self.assertEqual(transform.rotation, self._transform.rotation)
        self.assertEqual(transform.scale, scale * self._transform.scale)


if __name__ == '__main__':
    unittest.main()
