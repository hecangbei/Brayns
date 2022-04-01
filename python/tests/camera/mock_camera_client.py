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

from typing import Any

from brayns.camera.camera_view import CameraView
from brayns.client.client_protocol import ClientProtocol
from tests.camera.mock_camera_projection import MockCameraProjection


class MockCameraClient(ClientProtocol):

    def __init__(self) -> None:
        self.view = CameraView()
        self.name = MockCameraProjection.get_name()
        self.projection = MockCameraProjection().to_dict()

    def request(self, method: str, params: Any = None) -> Any:
        if method == 'get-camera-look-at':
            return self.view.to_dict()
        if method == 'set-camera-look-at':
            self.view = CameraView.from_dict(params)
            return
        if method == 'get-camera-type':
            return self.name
        if method.startswith('get-camera-'):
            if method.split('-')[2] != self.name:
                raise RuntimeError('Not the current camera type')
            return self.projection
        if method.startswith('set-camera-'):
            self.name = method.split('-')[2]
            self.projection = params
            return
        raise RuntimeError('Invalid request')
