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
from types import MappingProxyType

from brayns.core.common.box import Box
from brayns.core.common.quaternion import Quaternion
from brayns.core.common.transform import Transform
from brayns.core.common.vector3 import Vector3
from brayns.core.scene.model import Model
from tests.core.scene.mock_scene_instance import MockSceneInstance


class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSceneInstance()
        self._model = Model(
            id=1,
            bounds=Box(Vector3.zero, Vector3.one),
            metadata=MappingProxyType({'test': '1'}),
            visible=True,
            transform=Transform(
                Vector3.one,
                Quaternion(1, 2, 3, 4),
                Vector3.zero
            )
        )
        self._message = {
            'id': 1,
            'bounds': {
                'min': [0, 0, 0],
                'max': [1, 1, 1]
            },
            'metadata': {'test': '1'},
            'visible': True,
            'transformation': self._model.transform.serialize()
        }

    def test_from_instance(self) -> None:
        message = self._instance.add_model()
        ref = Model.deserialize(message)
        model = Model.from_instance(self._instance, ref.id)
        self.assertEqual(model.id, ref.id)
        self.assertEqual(model.bounds, ref.bounds)
        self.assertEqual(model.metadata, ref.metadata)
        self.assertEqual(model.visible, ref.visible)
        self.assertEqual(model.transform, ref.transform)

    def test_deserialize(self) -> None:
        test = Model.deserialize(self._message)
        self.assertEqual(test.id, self._model.id)
        self.assertEqual(test.bounds, self._model.bounds)
        self.assertEqual(test.metadata, self._model.metadata)
        self.assertEqual(test.visible, self._model.visible)
        self.assertEqual(test.transform, self._model.transform)

    def test_remove(self) -> None:
        ids = [1, 2, 3]
        Model.remove(self._instance, ids)
        self.assertEqual(self._instance.method, 'remove-model')
        self.assertEqual(self._instance.params, {'ids': ids})

    def test_serialize(self) -> None:
        ref = {
            'id': self._model.id,
            'visible': self._model.visible,
            'transformation': self._model.transform.serialize()
        }
        test = self._model.serialize()
        self.assertEqual(test, ref)

    def test_update(self) -> None:
        message = self._instance.add_model()
        model = Model.deserialize(message)
        model.transform = self._model.transform
        model.visible = False
        model.update(self._instance)
        self.assertEqual(self._instance.method, 'update-model')
        self.assertEqual(self._instance.params, {
            'id': model.id,
            'visible': model.visible,
            'transformation': model.transform.serialize()
        })

    def test_translate(self) -> None:
        translation = 3 * Vector3.one
        ref = self._model.transform.translate(translation)
        self._model.translate(translation)
        self.assertEqual(self._model.transform, ref)

    def test_rotate(self) -> None:
        rotation = Quaternion(1, 2, 3, 4)
        center = Vector3(4, 5, 6)
        ref = self._model.transform.rotate(rotation, center)
        self._model.rotate(rotation, center)
        self.assertEqual(self._model.transform, ref)

    def test_rescale(self) -> None:
        scale = 3 * Vector3.one
        ref = self._model.transform.rescale(scale)
        self._model.rescale(scale)
        self.assertEqual(self._model.transform, ref)


if __name__ == '__main__':
    unittest.main()
