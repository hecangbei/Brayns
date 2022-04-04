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
from brayns.instance.camera.camera_view import CameraView


class Camera:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    @property
    def name(self) -> str:
        return self._client.request('get-camera-type')

    @property
    def view(self) -> CameraView:
        message = self._client.request('get-camera-look-at')
        return CameraView.from_dict(message)

    @view.setter
    def view(self, value: CameraView) -> None:
        self._client.request('set-camera-look-at', value.to_dict())
