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

from brayns.instance.instance_protocol import InstanceProtocol
from brayns.core.camera.camera_type import CameraType
from brayns.core.camera.camera_view import CameraView
from brayns.core.serializers.camera_view_serializer import CameraViewSerializer


class CameraManager:

    def __init__(self, client: InstanceProtocol) -> None:
        self.__client = client
        self.__serializer = CameraViewSerializer()

    def get_camera_type(self) -> CameraType:
        result = self.__client.request('get-camera-type')
        return CameraType(result)

    def get_camera_view(self) -> CameraView:
        result = self.__client.request('get-camera-look-at')
        return self.__serializer.deserialize(result)

    def set_camera_view(self, view: CameraView) -> None:
        params = self.__serializer.serialize(view)
        self.__client.request('set-camera-look-at', params)
