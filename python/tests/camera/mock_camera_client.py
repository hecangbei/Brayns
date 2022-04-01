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

from brayns.client.client_protocol import ClientProtocol
from brayns.camera.camera_view import CameraView


class MockCameraClient(ClientProtocol):

    def __init__(self) -> None:
        self.camera = CameraView()
        self.projection_name = 'perspective'
        self.projection_properties = {}

    def request(self, method: str, params: Any = None) -> Any:
        if method == 'get-camera-look-at':
            return self.camera.to_dict()
        if method == 'set-camera-look-at':
            self.camera = CameraView.from_dict(params)
            return
        if not method.startswith('set-camera-'):
            raise RuntimeError('Invalid request')
        self.projection_name = method.split('-')[2]
        self.projection_properties = params
