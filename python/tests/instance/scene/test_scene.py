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

from brayns.instance.scene.model_protocol import ModelProtocol
from brayns.instance.scene.scene import Scene
from tests.instance.scene.mock_scene_client import MockSceneClient


class MockModel(ModelProtocol):

    def get_path(self) -> str:
        return 'path'

    def get_loader(self) -> str:
        return 'loader'

    def get_loader_properties(self) -> dict:
        return 'properties'


class TestScene(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._scene = Scene(self._client)
        self._client.add_model()

    def test_models(self) -> None:
        self.assertEqual(len(self._scene.models), len(self._client.models))

    def test_bounds(self) -> None:
        self.assertEqual(self._scene.bounds, self._client.scene.bounds)


if __name__ == '__main__':
    unittest.main()
