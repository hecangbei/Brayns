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

from brayns.core.model.model import Model
from tests.core.model.mock_model_instance import MockModelInstance
from tests.core.model.mock_model_loader import MockModelLoader


class TestModelLoader(unittest.TestCase):

    def test_load(self) -> None:
        loader = MockModelLoader(1, 'test')
        instance = MockModelInstance()
        path = 'path/test.model'
        models = loader.load(instance, path)
        ref = [Model.deserialize(model) for model in instance.models]
        self.assertEqual(models, ref)
        self.assertEqual(instance.method, 'add-model')
        self.assertEqual(instance.params, {
            'path': path,
            'loader': MockModelLoader.name,
            'loader_properties': loader.properties
        })


if __name__ == '__main__':
    unittest.main()
