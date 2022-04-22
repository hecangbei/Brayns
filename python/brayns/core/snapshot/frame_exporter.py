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

from brayns.core.snapshot.image_format import ImageFormat
from brayns.core.snapshot.key_frame import KeyFrame
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class FrameExporter:

    frames: list[KeyFrame]
    format: ImageFormat = ImageFormat.PNG
    jpeg_quality: int = 100
    resolution: Optional[tuple[int, int]] = None
    sequential_naming: bool = True

    def export_frames(self, instance: InstanceProtocol, folder: str) -> None:
        params = {
            'path': folder,
            'image_settings': {
                'format': self.format.value,
                'quality': self.jpeg_quality,
                'size': self.resolution
            },
            'key_frames': [
                frame.serialize()
                for frame in self.frames
            ],
            'sequential_naming': self.sequential_naming
        }
        instance.request('export-frames', params)
