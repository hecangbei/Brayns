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

from brayns.client.client_protocol import ClientProtocol
from brayns.common.image.image_format import ImageFormat


@dataclass
class Snapshot:

    quality: int = 100
    resolution: Optional[tuple[int, int]] = None
    frame: Optional[int] = None

    def save(self, client: ClientProtocol, path: str) -> None:
        format = ImageFormat.from_path(path)
        params = self._get_params(format, path)
        self._request(client, params)

    def download(self, client: ClientProtocol, format: ImageFormat = ImageFormat.PNG) -> bytes:
        params = self._get_params(format)
        result = self._request(client, params)
        return base64.b64decode(result['data'])

    def download_and_save(self, client: ClientProtocol, path: str) -> None:
        format = ImageFormat.from_path(path)
        data = self.download(client, format)
        with open(path, 'wb') as file:
            file.write(data)

    def _get_params(self, format: ImageFormat, path: Optional[str] = None) -> dict:
        return {
            'path': path,
            'image_settings': {
                'format': format.value,
                'quality': self.quality,
                'size': self.resolution
            },
            'animation_frame': self.frame
        }

    def _request(self, client: ClientProtocol, params: dict) -> dict:
        return client.request('snapshot', params)
