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

from brayns.instance.instance_protocol import InstanceProtocol
from brayns.core.camera.camera_view import CameraView
from brayns.core.serializers.camera_view_serializer import CameraViewSerializer


class MockCameraClient(InstanceProtocol):

    def __init__(self) -> None:
        self.view = CameraView()
        self.name = ''
        self.properties = {}
        self._serializer = CameraViewSerializer()

    def request(self, method: str, params: Any = None) -> Any:
        if method == 'get-camera-look-at':
            return self._serializer.serialize(self.view)
        if method == 'set-camera-look-at':
            self.view = self._serializer.deserialize(params)
            return None
        if method == 'get-camera-type':
            return self.name
        if method.startswith('get-camera-'):
            name = method.split('-')[2]
            if name != self.name:
                raise RuntimeError(f'Current camera is {self.name} not {name}')
            return self.properties
        if method.startswith('set-camera-'):
            self.name = method.split('-')[2]
            self.properties = params
            return None
        raise RuntimeError('Invalid request')
