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

from brayns.core.model.model_loader import ModelLoader
from tests.core.model.mock_scene_instance import MockSceneInstance


class TestSceneManager(unittest.TestCase):

    def test_add_model(self) -> None:
        instance = MockSceneInstance()
        name = 'test'
        path = 'path/test.model'
        properties = {'test1': 1, 'test2': 2}
        loader = ModelLoader(name, properties)
        loader.add_model(instance, path)
        self.assertEqual(instance.method, 'add-model')
        self.assertEqual(instance.params, {
            'path': path,
            'loader': name,
            'loader_properties': properties
        })


if __name__ == '__main__':
    unittest.main()
