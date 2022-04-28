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

from brayns.core.common.box import Box
from brayns.core.scene.model import Model
from brayns.core.scene.scene import Scene
from tests.core.scene.mock_scene_instance import MockSceneInstance


class TestScene(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSceneInstance()

    def test_from_instance(self) -> None:
        message = self._instance.add_model()
        scene = Scene.from_instance(self._instance)
        self.assertEqual(self._instance.method, 'get-scene')
        self.assertEqual(self._instance.params, None)
        self.assertEqual(scene.bounds, Box.deserialize(self._instance.bounds))
        self.assertEqual(len(scene.models), 1)
        model = scene.models[0]
        ref = Model.deserialize(message)
        self.assertEqual(model.id, ref.id)
        self.assertEqual(model.bounds, ref.bounds)
        self.assertEqual(model.metadata, ref.metadata)
        self.assertEqual(model.visible, ref.visible)
        self.assertEqual(model.transform, ref.transform)

    def test_deserialize(self) -> None:
        self._instance.add_model()
        message = self._instance.get_scene()
        scene = Scene.deserialize(message)
        self.assertEqual(scene.bounds, Box.deserialize(self._instance.bounds))
        self.assertEqual(len(scene.models), 1)
        model = scene.models[0]
        ref = Model.deserialize(self._instance.models[0])
        self.assertEqual(model.id, ref.id)
        self.assertEqual(model.bounds, ref.bounds)
        self.assertEqual(model.metadata, ref.metadata)
        self.assertEqual(model.visible, ref.visible)
        self.assertEqual(model.transform, ref.transform)


if __name__ == '__main__':
    unittest.main()
