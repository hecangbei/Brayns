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
from brayns.core.snapshot.frame_exporter import FrameExporter
from brayns.core.snapshot.image_format import ImageFormat
from brayns.core.snapshot.key_frame import KeyFrame
from tests.core.snapshot.mock_snapshot_instance import MockSnapshotInstance


class TestFrameExporter(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSnapshotInstance()

    def test_export_frames(self) -> None:
        exporter = FrameExporter(
            frames=[KeyFrame(i, CameraView()) for i in range(10)],
            format=ImageFormat.JPEG,
            jpeg_quality=50,
            resolution=(600, 900),
            sequential_naming=False
        )
        folder = 'test'
        exporter.export_frames(self._instance, folder)
        self.assertEqual(self._instance.method, 'export-frames')
        params = self._instance.params
        image: dict = params['image_settings']
        self.assertEqual(params['path'], folder)
        self.assertEqual(image['format'], 'jpg')
        self.assertEqual(image['quality'], 50)
        self.assertEqual(image['size'], [600, 900])
        self.assertFalse(params['sequential_naming'])
        for i, frame in enumerate(params['key_frames']):
            self.assertEqual(i, frame['frame_index'])
            self.assertEqual(frame['camera_view'], CameraView().serialize())


if __name__ == '__main__':
    unittest.main()
