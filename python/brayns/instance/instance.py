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
from brayns.instance.camera.camera import Camera
from brayns.instance.camera.camera_protocol import CameraProtocol
from brayns.instance.scene.scene import Scene
from brayns.instance.snapshot.snapshot import Snapshot


class Instance:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client
        self._scene = Scene(client)
        self._camera = Camera(client)
        self._snapshot = Snapshot(client)

    def __enter__(self) -> 'Instance':
        return self

    def __exit__(self, *_) -> None:
        self._client.disconnect()

    @property
    def client(self) -> ClientProtocol:
        return self._client

    @property
    def scene(self) -> Scene:
        return self._scene

    @property
    def camera(self) -> Camera:
        return self._camera

    @camera.setter
    def camera(self, value: CameraProtocol) -> None:
        self._camera.update(value.get_name(), value.get_properties())

    @property
    def snapshot(self) -> Snapshot:
        return self._snapshot
