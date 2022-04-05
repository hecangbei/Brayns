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

from brayns.common.image.image_format import ImageFormat
from brayns.instance.snapshot.snapshot import Snapshot
from brayns.instance.snapshot.snapshot_settings import SnapshotSettings
from tests.instance.snapshot.mock_snapshot_client import MockSnapshotClient


class TestSnapshot(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSnapshotClient()
        self._snapshot = Snapshot(self._client)

    def test_save(self) -> None:
        self._snapshot.save('test.jpg', SnapshotSettings(jpeg_quality=50))
        params = self._client.params
        image: dict = params['image_settings']
        self.assertEqual(params['path'], 'test.jpg')
        self.assertEqual(image['format'], 'jpg')
        self.assertEqual(image['quality'], 50)
        self.assertIsNone(image.get('size'))
        self.assertIsNone(params.get('animation_frame'))

    def test_download(self) -> None:
        data = self._snapshot.download(ImageFormat.PNG, SnapshotSettings(
            resolution=(1920, 1080),
            frame=12
        ))
        self.assertEqual(data, self._client.data)
        params = self._client.params
        image: dict = params['image_settings']
        self.assertIsNone(params.get('path'))
        self.assertEqual(image['format'], 'png')
        self.assertEqual(list(image['size']), [1920, 1080])
        self.assertEqual(params['animation_frame'], 12)


if __name__ == '__main__':
    unittest.main()
