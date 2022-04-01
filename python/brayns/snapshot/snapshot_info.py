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

from brayns.camera.camera_view import CameraView
from brayns.image.image_info import ImageInfo


@dataclass
class SnapshotInfo:

    path: Optional[str] = None
    image_info: ImageInfo = ImageInfo()
    camera: Optional[CameraView] = None
    animation_frame: Optional[int] = None

    def to_dict(self) -> dict:
        message = {
            'image_settings': self.image_info
        }
        if self.path is not None:
            message['path'] = self.path
        if self.camera is not None:
            message['camera_view'] = self.path
        if self.animation_frame is not None:
            message['animation_frame'] = self.animation_frame
        return message
