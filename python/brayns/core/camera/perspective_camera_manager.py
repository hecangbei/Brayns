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
from brayns.core.camera.camera_manager import CameraManager
from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.serializers.perspective_camera_serializer import \
    PerspectiveCameraSerializer


class PerspectiveCameraManager(CameraManager):

    def __init__(self, client: ClientProtocol) -> None:
        super().__init__(client)
        self._client = client
        self._serializer = PerspectiveCameraSerializer()

    def get_camera(self) -> PerspectiveCamera:
        result = self._client.request('get-camera-perspective')
        return self._serializer.deserialize(result)

    def set_camera(self, camera: PerspectiveCamera) -> None:
        params = self._serializer.serialize(camera)
        self._client.request('set-camera-perspective', params)
