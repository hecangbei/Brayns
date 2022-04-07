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

from brayns.client.client_protocol import ClientProtocol
from brayns.common.image.image_format import ImageFormat
from brayns.core.snapshot.snapshot_request import SnapshotRequest
from brayns.core.snapshot.snapshot_settings import SnapshotSettings


class Snapshot:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    def save(
        self,
        path: str,
        settings: SnapshotSettings = SnapshotSettings()
    ) -> None:
        SnapshotRequest(
            format=ImageFormat.from_path(path),
            save_as=path,
            settings=settings
        ).send(self._client)

    def download(
        self,
        format: ImageFormat = ImageFormat.PNG,
        settings: SnapshotSettings = SnapshotSettings()
    ) -> bytes:
        return SnapshotRequest(
            format=format,
            settings=settings
        ).send(self._client)

    def download_and_save(
        self,
        path: str,
        settings: SnapshotSettings = SnapshotSettings()
    ) -> None:
        format = ImageFormat.from_path(path)
        data = self.download(format, settings)
        with open(path, 'wb') as file:
            file.write(data)
