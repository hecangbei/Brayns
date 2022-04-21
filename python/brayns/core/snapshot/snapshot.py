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

import base64
from dataclasses import dataclass
from typing import Optional

from brayns.core.snapshot.image_format import ImageFormat
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class Snapshot:

    jpeg_quality: int = 100
    resolution: Optional[tuple[int, int]] = (1920, 1080)
    frame: Optional[int] = None

    def save(self, instance: InstanceProtocol, path: str) -> None:
        format = ImageFormat.from_path(path)
        data = self.download(instance, format)
        with open(path, 'wb') as file:
            file.write(data)

    def save_remotely(self, instance: InstanceProtocol, path: str) -> None:
        format = ImageFormat.from_path(path)
        params = self._get_params(format, path)
        self._request(instance, params)

    def download(self, instance: InstanceProtocol, format: ImageFormat = ImageFormat.PNG) -> bytes:
        params = self._get_params(format)
        result = self._request(instance, params)
        return base64.b64decode(result['data'])

    def _get_params(self, format: ImageFormat, path: Optional[str] = None) -> dict:
        return {
            'path': path,
            'image_settings': {
                'format': format.value,
                'quality': self.jpeg_quality,
                'size': list(self.resolution)
            },
            'animation_frame': self.frame
        }

    def _request(self, instance: InstanceProtocol, params: dict) -> dict:
        return instance.request('snapshot', params)
