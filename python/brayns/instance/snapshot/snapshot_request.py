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
from brayns.instance.snapshot.snapshot_settings import SnapshotSettings


@dataclass
class SnapshotRequest:

    format: ImageFormat = ImageFormat.PNG
    save_as: Optional[str] = None
    settings: SnapshotSettings = SnapshotSettings()

    def to_dict(self) -> dict:
        return {
            'path': self.save_as,
            'image_settings': {
                'format': self.format.value,
                'quality': self.settings.jpeg_quality,
                'size': self.settings.resolution
            },
            'animation_frame': self.settings.frame
        }

    def send(self, client: ClientProtocol) -> bytes:
        result = client.request('snapshot', self.to_dict())
        if self.save_as is not None:
            return b''
        return base64.b64decode(result['data'])
