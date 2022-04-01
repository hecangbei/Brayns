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
from typing import Optional

from brayns.client.client_protocol import ClientProtocol
from brayns.image.image_format import ImageFormat
from brayns.snapshot.snapshot_info import SnapshotInfo


class Snapshot:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    def save(
        self,
        path: str,
        resolution: Optional[tuple[int, int]] = None,
        frame: Optional[int] = None
    ) -> None:
        self._request(SnapshotInfo(
            path=path,
            format=ImageFormat.from_path(path),
            size=resolution,
            frame=frame
        ))

    def download(
        self,
        format: ImageFormat = ImageFormat.PNG,
        resolution: Optional[tuple[int, int]] = None,
        frame: Optional[int] = None
    ) -> bytes:
        data = self._request(SnapshotInfo(
            format=format,
            size=resolution,
            frame=frame
        ))
        return base64.b64decode(data)

    def download_and_save(
        self,
        path: str,
        resolution: Optional[tuple[int, int]] = None,
        frame: Optional[int] = None
    ) -> None:
        data = self.download(
            format=ImageFormat.from_path(path),
            resolution=resolution,
            frame=frame
        )
        with open(path) as file:
            file.write(data)

    def _request(self, info: SnapshotInfo) -> str:
        return self._client.request('snapshot', info.to_dict())['data']
