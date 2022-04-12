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
from brayns.core.image.image_format import ImageFormat
from brayns.core.serializers.snapshot_serializer import SnapshotSerializer
from brayns.core.snapshot.snapshot_info import SnapshotInfo


class SnapshotManager:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client
        self._serializer = SnapshotSerializer()

    def save(self, path: str, info: SnapshotInfo = SnapshotInfo()) -> None:
        self._request(path, ImageFormat.from_path(path), info)

    def download(self, format: ImageFormat = ImageFormat.PNG, info: SnapshotInfo = SnapshotInfo()) -> bytes:
        result = self._request(None, format, info)
        return base64.b64decode(result['data'])

    def download_and_save(self, path: str, info: SnapshotInfo = SnapshotInfo()) -> None:
        format = ImageFormat.from_path(path)
        data = self.download(format, info)
        with open(path, 'wb') as file:
            file.write(data)

    def _request(self, path: Optional[str], format: ImageFormat, info: SnapshotInfo) -> dict:
        params = self._serializer.serialize(path, format, info)
        return self._client.request('snapshot', params)
