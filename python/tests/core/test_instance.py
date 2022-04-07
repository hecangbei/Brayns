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

from brayns.core.camera.camera_protocol import Camera
from brayns.core.instance import Instance
from brayns.core.scene.scene_manager import Scene
from brayns.core.snapshot.snapshot import Snapshot
from tests.core.camera.mock_camera import MockCamera
from tests.core.camera.mock_camera_client import MockCameraClient
from tests.core.scene.mock_scene_client import MockSceneClient
from tests.core.snapshot.mock_snapshot_client import MockSnapshotClient


class TestInstance(unittest.TestCase):

    def test_scene(self) -> None:
        client = MockSceneClient()
        instance = Instance(client)
        self.assertIsInstance(instance.scene, Scene)

    def test_camera(self) -> None:
        client = MockCameraClient()
        instance = Instance(client)
        self.assertIsInstance(instance.camera, Camera)
        test = MockCamera()
        instance.camera = test
        self.assertEqual(client.name, test.get_name())
        self.assertEqual(client.properties, test.get_properties())

    def test_snapshot(self) -> None:
        client = MockSnapshotClient()
        instance = Instance(client)
        self.assertIsInstance(instance.snapshot, Snapshot)


if __name__ == '__main__':
    unittest.main()
