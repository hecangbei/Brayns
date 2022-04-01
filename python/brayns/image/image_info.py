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

from dataclasses import dataclass
from typing import Optional

from brayns.image.image_format import ImageFormat
from brayns.image.jpeg_quality import JpegQuality


@dataclass
class ImageInfo:

    format: ImageFormat = ImageFormat.PNG
    jpeg_quality: JpegQuality = JpegQuality.highest()
    resolution: Optional[tuple[int, int]] = None

    def to_dict(self) -> dict:
        message = {
            'format': self.format.value
        }
        if self.format == ImageFormat.JPEG:
            message['quality'] = self.jpeg_quality.value
        if self.resolution is not None:
            message['size'] = self.resolution
        return message
