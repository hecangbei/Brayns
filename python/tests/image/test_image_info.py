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

from brayns.image.image_format import ImageFormat
from brayns.image.image_info import ImageInfo


class TestImageInfo(unittest.TestCase):

    def test_from_path(self) -> None:
        path = 'test/test.png'
        test = ImageInfo.from_path(path)
        self.assertIs(test.format, ImageFormat.PNG)

    def test_to_dict_png(self) -> None:
        test = ImageInfo(
            format=ImageFormat.PNG,
            resolution=(1920, 1080)
        )
        message = test.to_dict()
        ref = {
            'format': 'png',
            'size': [1920, 1080]
        }
        self.assertEqual(message, ref)

    def test_to_dict_jpeg(self) -> None:
        test = ImageInfo(
            format=ImageFormat.JPEG,
            jpeg_quality=50
        )
        message = test.to_dict()
        ref = {
            'format': 'jpg',
            'quality': 50
        }
        self.assertEqual(message, ref)


if __name__ == '__main__':
    unittest.main()
