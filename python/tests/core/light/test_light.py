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
from brayns.core.light.light import Light
from tests.core.light.mock_light import MockLight
from tests.core.light.mock_light_instance import MockLightInstance


class TestLight(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockLightInstance()

    def test_remove(self) -> None:
        self._instance.names = 3 * [MockLight.name]
        self._instance.lights = 3 * [MockLight().serialize()]
        Light.remove(self._instance, [0, 1, 2])
        self.assertEqual(self._instance.method, 'remove-lights')
        self.assertEqual(self._instance.params, {'ids': [0, 1, 2]})

    def test_clear(self) -> None:
        self._instance.names = 3 * [MockLight.name]
        self._instance.lights = 3 * [MockLight().serialize()]
        Light.clear(self._instance)
        self.assertEqual(self._instance.method, 'clear-lights')
        self.assertEqual(self._instance.params, None)

    def test_add(self) -> None:
        light = MockLight(Color.pure_red, 3, False, 'test')
        id = light.add(self._instance)
        self.assertEqual(id, 0)
        self.assertEqual(self._instance.method, 'add-light-test')
        self.assertEqual(self._instance.params, light.serialize())


if __name__ == '__main__':
    unittest.main()
