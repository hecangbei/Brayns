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

from brayns.core.image.image_format import ImageFormat
from brayns.core.snapshot.snapshot_task import SnapshotTask
from brayns.instance.instance_protocol import InstanceProtocol
from brayns.instance.request_future import RequestFuture


@dataclass
class Snapshot:

    jpeg_quality: int = 100
    resolution: Optional[tuple[int, int]] = (1920, 1080)
    frame: Optional[int] = None

    def save(self, instance: InstanceProtocol, path: str, remote: bool = False) -> SnapshotTask:
        format = ImageFormat.from_path(path)
        message_path = path if remote else None
        task = self._task(instance, message_path, format)
        return SnapshotTask(task, path, remote)

    def download(self, instance: InstanceProtocol, format: ImageFormat = ImageFormat.PNG) -> bytes:
        task = self._task(instance, None, format)
        return SnapshotTask(task)

    def _task(self, instance: InstanceProtocol, path: Optional[str], format: ImageFormat) -> RequestFuture:
        params = {
            'path': path,
            'image_settings': {
                'format': format.value,
                'quality': self.jpeg_quality,
                'size': self.resolution
            },
            'animation_frame': self.frame
        }
        return instance.task('snapshot', params)
