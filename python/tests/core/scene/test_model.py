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
from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.transform import Transform
from brayns.core.geometry.vector3 import Vector3
from brayns.core.scene.model import Model
from tests.core.scene.mock_scene_instance import MockSceneInstance


class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSceneInstance()

    def test_from_instance(self) -> None:
        ref = self._instance.add_model()
        model = Model.from_instance(self._instance, ref['id'])
        self.assertEqual(model.id, ref['id'])
        self.assertEqual(model.bounds, Box.deserialize(ref['bounds']))
        self.assertEqual(model.metadata, ref['metadata'])
        self.assertEqual(model.visible, ref['visible'])
        self.assertEqual(
            model.transform,
            Transform.deserialize(ref['transformation'])
        )
        self.assertEqual(self._instance.methods, ['get-model'])
        self.assertEqual(self._instance.params, [{'id': ref['id']}])

    def test_deserialize(self) -> None:
        message = {
            'id': 0,
            'bounds': {
                'min': [0, 0, 0],
                'max': [1, 1, 1]
            },
            'metadata': {
                'test1': '1'
            },
            'visible': True,
            'transformation': Transform.identity.serialize()
        }
        test = Model.deserialize(message)
        ref = Model(
            id=0,
            bounds=Box(Vector3.zero, Vector3.one),
            metadata={
                'test1': '1'
            },
            visible=True,
            transform=Transform.identity
        )
        self.assertEqual(test, ref)

    def test_serialize(self) -> None:
        ref = {
            'id': 1,
            'visible': True,
            'transformation': Transform.identity.serialize()
        }
        model = Model(
            id=1,
            bounds=Box.empty,
            metadata={},
            visible=True,
            transform=Transform.identity
        )
        test = model.serialize()
        self.assertEqual(test, ref)

    def test_update(self) -> None:
        result = self._instance.add_model()
        model = Model.deserialize(result)
        model.transform = Transform(
            Vector3.one,
            Quaternion(1, 2, 3, 4),
            Vector3.zero
        )
        model.visible = False
        model.update(self._instance)
        self.assertEqual(self._instance.methods, ['update-model'])
        ref = {
            'id': model.id,
            'visible': model.visible,
            'transformation': model.transform.serialize()
        }
        self.assertEqual(self._instance.params, [ref])


if __name__ == '__main__':
    unittest.main()
