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

from brayns.core.common.quaternion import Quaternion
from brayns.core.common.transform import Transform
from brayns.core.common.vector3 import Vector3


class TestTransform(unittest.TestCase):

    def setUp(self) -> None:
        self._transform = Transform(
            translation=Vector3(1, 2, 3),
            rotation=Quaternion(1, 2, 3, 4),
            scale=Vector3(4, 5, 6)
        )
        self._message = {
            'translation': [1, 2, 3],
            'rotation': [1, 2, 3, 4],
            'rotation_center': [1, 2, 3],
            'scale': [4, 5, 6]
        }

    def test_deserialize(self) -> None:
        test = Transform.deserialize(self._message)
        ref = self._transform
        self.assertEqual(test, ref)

    def test_identity(self) -> None:
        test = Transform.identity
        self.assertEqual(test.translation, Vector3.zero)
        self.assertEqual(test.rotation, Quaternion.identity)
        self.assertEqual(test.scale, Vector3.one)

    def test_serialize(self) -> None:
        test = self._transform.serialize()
        ref = self._message
        self.assertEqual(test, ref)

    def test_with_translation(self) -> None:
        translation = Vector3.one
        test = self._transform.with_translation(translation)
        self.assertEqual(test.translation, translation)
        self.assertEqual(test.rotation, self._transform.rotation)
        self.assertEqual(test.scale, self._transform.scale)

    def test_with_rotation(self) -> None:
        rotation = Quaternion.identity
        test = self._transform.with_rotation(rotation)
        self.assertEqual(test.translation, self._transform.translation)
        self.assertEqual(test.rotation, rotation)
        self.assertEqual(test.scale, self._transform.scale)

    def test_with_scale(self) -> None:
        scale = Vector3.one
        test = self._transform.with_scale(scale)
        self.assertEqual(test.translation, self._transform.translation)
        self.assertEqual(test.rotation, self._transform.rotation)
        self.assertEqual(test.scale, scale)

    def test_translate(self) -> None:
        translation = Vector3.one
        test = self._transform.translate(translation)
        ref = self._transform.translation + translation
        self.assertEqual(test.translation, ref)
        self.assertEqual(test.rotation, self._transform.rotation)
        self.assertEqual(test.scale, self._transform.scale)

    def test_rotate(self) -> None:
        rotation = Quaternion.from_axis_angle(Vector3.up, 90, degrees=True)
        test = self._transform.rotate(rotation)
        self.assertEqual(test.translation, self._transform.translation)
        self.assertEqual(test.rotation, rotation * self._transform.rotation)
        self.assertEqual(test.scale, self._transform.scale)

    def test_rotate_with_center(self) -> None:
        rotation = Quaternion.from_axis_angle(Vector3.up, 90, degrees=True)
        center = Vector3.one
        test = self._transform.rotate(rotation, center)
        ref = self._transform.translation
        ref += center - rotation.rotate(center)
        self.assertEqual(test.translation, ref)
        self.assertEqual(test.rotation, rotation * self._transform.rotation)
        self.assertEqual(test.scale, self._transform.scale)

    def test_rescale(self) -> None:
        scale = 2 * Vector3.one
        test = self._transform.rescale(scale)
        self.assertEqual(test.translation, self._transform.translation)
        self.assertEqual(test.rotation, self._transform.rotation)
        self.assertEqual(test.scale, scale * self._transform.scale)


if __name__ == '__main__':
    unittest.main()
