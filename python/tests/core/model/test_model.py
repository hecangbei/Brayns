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
from brayns.core.common.quaternion import Quaternion
from brayns.core.common.transform import Transform
from brayns.core.common.vector3 import Vector3
from brayns.core.model.model import Model
from tests.core.model.mock_model_instance import MockModelInstance


class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockModelInstance()
        self._model = Model(
            id=1,
            bounds=Bounds(Vector3.zero, Vector3.one),
            metadata={'test': '1'},
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
        test = Model.from_instance(self._instance, 0)
        ref = Model.deserialize(self._instance.model)
        self.assertEqual(test, ref)

    def test_deserialize(self) -> None:
        test = Model.deserialize(self._message)
        self.assertEqual(test, self._model)

    def test_remove(self) -> None:
        ids = [1, 2, 3]
        Model.remove(self._instance, ids)
        self.assertEqual(self._instance.method, 'remove-model')
        self.assertEqual(self._instance.params, {'ids': ids})

    def test_update(self) -> None:
        Model.update(
            self._instance,
            id=0,
            visible=True,
            transform=Transform.identity
        )
        self.assertEqual(self._instance.method, 'update-model')
        self.assertEqual(self._instance.params, {
            'id': 0,
            'visible': True,
            'transformation': Transform.identity.serialize()
        })

    def test_enable_simulation(self) -> None:
        Model.enable_simulation(self._instance, 1, True)
        self.assertEqual(self._instance.method, 'enable-simulation')
        self.assertEqual(self._instance.params, {
            'model_id': 1,
            'enabled': True
        })


if __name__ == '__main__':
    unittest.main()
