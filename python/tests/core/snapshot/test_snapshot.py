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

from brayns.core.camera.camera_view import CameraView
from brayns.core.common.resolution import Resolution
from brayns.core.renderer.interactive_renderer import InteractiveRenderer
from brayns.core.renderer.production_renderer import ProductionRenderer
from brayns.core.snapshot.image_format import ImageFormat
from brayns.core.snapshot.snapshot import Snapshot
from tests.core.camera.mock_camera import MockCamera
from tests.core.renderer.mock_renderer import MockRenderer
from tests.core.snapshot.mock_snapshot_instance import MockSnapshotInstance


class TestSnapshot(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSnapshotInstance()

    def test_for_production(self) -> None:
        test = Snapshot.for_production()
        self.assertEqual(test.resolution, Resolution.production)
        self.assertEqual(test.renderer, ProductionRenderer.default())

    def test_for_testing(self) -> None:
        test = Snapshot.for_testing()
        self.assertEqual(test.resolution, Resolution.full_hd)
        self.assertEqual(test.renderer, InteractiveRenderer.default())

    def test_save_remotely(self) -> None:
        snapshot = Snapshot()
        path = 'test.jpg'
        snapshot.save_remotely(self._instance, path)
        self.assertEqual(self._instance.method, 'snapshot')
        self.assertEqual(self._instance.params, {
            'path': path,
            'image_settings': {
                'format': 'jpg',
                'quality': 100
            }
        })

    def test_download_not_params(self) -> None:
        snapshot = Snapshot()
        data = snapshot.download(self._instance, ImageFormat.PNG)
        self.assertEqual(data, self._instance.data)
        self.assertEqual(self._instance.method, 'snapshot')
        self.assertEqual(self._instance.params, {
            'image_settings': {
                'format': 'png'
            }
        })

    def test_download_all_params(self) -> None:
        snapshot = Snapshot(
            jpeg_quality=50,
            resolution=(1920, 1080),
            frame=12,
            view=CameraView(),
            camera=MockCamera(),
            renderer=MockRenderer()
        )
        snapshot.download(self._instance, ImageFormat.JPEG)
        ref = {
            'image_settings': {
                'format': 'jpg',
                'quality': 50,
                'size': [1920, 1080]
            },
            'animation_settings': {
                'frame': 12,
            },
            'camera_view': CameraView().serialize(),
            'camera': MockCamera().serialize(),
            'renderer': MockRenderer().serialize()
        }
        test = self._instance.params
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
