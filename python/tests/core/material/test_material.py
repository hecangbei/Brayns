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
        ref = MockMaterial.name
        self._instance.names.append(ref)
        test = Material.get_material_name(self._instance, 0)
        self.assertEqual(test, ref)
        self.assertEqual(self._instance.method, 'get-material-type')
        self.assertEqual(self._instance.params, {'id': 0})

    def test_from_dict(self) -> None:
        common = {'color': [1, 0, 0]}
        test = MockMaterial.from_dict(common, test1='test', test2=3)
        self.assertEqual(test.color, Color.pure_red)
        self.assertEqual(test.test1, 'test')
        self.assertEqual(test.test2, 3)

    def test_from_model(self) -> None:
        ref = MockMaterial(Color.pure_blue, 'test', 12)
        self._instance.names.append(ref.name)
        self._instance.properties.append(ref.serialize())
        test = MockMaterial.from_model(self._instance, 0)
        self.assertEqual(test, ref)
        self.assertEqual(self._instance.method, 'get-material-test')
        self.assertEqual(self._instance.params, {'id': 0})

    def test_is_applied(self) -> None:
        self._instance.names.append(MockMaterial.name)
        self.assertTrue(MockMaterial.is_applied(self._instance, 0))

    def test_to_dict(self) -> None:
        material = MockMaterial(Color.pure_red)
        test = material.to_dict({'test': 0})
        ref = {
            'color': [1, 0, 0],
            'test': 0
        }
        self.assertEqual(test, ref)

    def test_apply(self) -> None:
        material = MockMaterial(Color.pure_blue, test1='test', test2=3)
        self._instance.names.append(material.name)
        self._instance.properties.append({})
        material.apply(self._instance, 0)
        params = {
            'model_id': 0,
            'material': material.serialize()
        }
        self.assertEqual(self._instance.method, 'set-material-test')
        self.assertEqual(self._instance.params, params)


if __name__ == '__main__':
    unittest.main()
