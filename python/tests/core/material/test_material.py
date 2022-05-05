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

from brayns.core.common.color import Color
from brayns.core.material.material import Material
from tests.core.material.mock_material import MockMaterial
from tests.core.material.mock_material_instance import MockMaterialInstance


class TestMaterial(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockMaterialInstance()

    def test_get_material_name(self) -> None:
        test = Material.get_material_name(self._instance, 0)
        self.assertEqual(test, self._instance.name)
        self.assertEqual(self._instance.method, 'get-material-type')
        self.assertEqual(self._instance.params, {'id': 0})

    def test_from_model(self) -> None:
        test = MockMaterial.from_model(self._instance, 0)
        ref = MockMaterial.deserialize(self._instance.material)
        self.assertEqual(test, ref)
        self.assertEqual(self._instance.method, 'get-material-test')
        self.assertEqual(self._instance.params, {'id': 0})

    def test_is_applied(self) -> None:
        self.assertTrue(MockMaterial.is_applied(self._instance, 0))

    def test_apply(self) -> None:
        material = MockMaterial(Color.pure_blue, test1='test', test2=3)
        material.apply(self._instance, 0)
        self.assertEqual(self._instance.method, 'set-material-test')
        self.assertEqual(self._instance.params, {
            'model_id': 0,
            'material': material.serialize()
        })


if __name__ == '__main__':
    unittest.main()
