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

from brayns.core.renderer.renderer import Renderer
from tests.core.renderer.mock_renderer import MockRenderer
from tests.core.renderer.mock_renderer_instance import MockRendererInstance


class TestRenderer(unittest.TestCase):

    def test_get_main_renderer_name(self) -> None:
        instance = MockRendererInstance()
        test = Renderer.get_main_renderer_name(instance)
        ref = instance.name
        self.assertEqual(test, ref)
        self.assertEqual(instance.method, 'get-renderer-type')
        self.assertEqual(instance.params, None)

    def test_from_instance(self) -> None:
        instance = MockRendererInstance()
        test = MockRenderer.from_instance(instance)
        ref = MockRenderer.deserialize(instance.renderer)
        self.assertEqual(test, ref)
        self.assertEqual(instance.method, 'get-renderer-test')
        self.assertEqual(instance.params, None)

    def test_is_main_renderer(self) -> None:
        instance = MockRendererInstance()
        test = MockRenderer.is_main_renderer(instance)
        self.assertTrue(test)
        self.assertEqual(instance.method, 'get-renderer-type')
        self.assertEqual(instance.params, None)

    def test_use_as_main_renderer(self) -> None:
        instance = MockRendererInstance()
        test = MockRenderer()
        test.use_as_main_renderer(instance)
        self.assertEqual(instance.method, 'set-renderer-test')
        self.assertEqual(instance.params, test.serialize())


if __name__ == '__main__':
    unittest.main()
