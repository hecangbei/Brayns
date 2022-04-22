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

from brayns.core.snapshot.image_format import ImageFormat
from brayns.core.snapshot.snapshot import Snapshot
from tests.core.snapshot.mock_snapshot_instance import MockSnapshotInstance


class TestSnapshot(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSnapshotInstance()
        self._snapshot = Snapshot(
            jpeg_quality=50,
            resolution=(600, 900),
            frame=12
        )

    def test_save_remotely(self) -> None:
        path = 'test.jpg'
        self._snapshot.save_remotely(self._instance, path)
        self.assertEqual(self._instance.method, 'snapshot')
        self.assertEqual(self._instance.params, {
            'path': path,
            'image_settings': {
                'quality': self._snapshot.jpeg_quality,
                'size': self._snapshot.resolution,
                'format': 'jpg'
            },
            'animation_frame': self._snapshot.frame
        })

    def test_download(self) -> None:
        data = self._snapshot.download(self._instance, ImageFormat.JPEG)
        self.assertEqual(data, self._instance.data)
        self.assertEqual(self._instance.method, 'snapshot')
        self.assertEqual(self._instance.params, {
            'path': None,
            'image_settings': {
                'quality': self._snapshot.jpeg_quality,
                'size': self._snapshot.resolution,
                'format': 'jpg'
            },
            'animation_frame': self._snapshot.frame
        })


if __name__ == '__main__':
    unittest.main()
