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

from typing import Optional

from brayns.client.client_protocol import ClientProtocol
from brayns.core.camera.camera_type import CameraType
from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.camera.perspective_camera_manager import PerspectiveCameraManager
from brayns.core.geometry.box import Box


class PerspectiveCameraController:

    def __init__(self, client: ClientProtocol) -> None:
        self._manager = PerspectiveCameraManager(client)

    def center_camera(self, target: Box, camera: Optional[PerspectiveCamera] = None) -> None:
        camera = self._get_camera(camera)
        view = camera.get_default_view(target)
        self._manager.set_camera_view(view)

    def _get_camera(self, camera: Optional[PerspectiveCamera]) -> PerspectiveCamera:
        if camera is None:
            return self._get_current_camera()
        self._manager.set_camera(camera)
        return camera

    def _get_current_camera(self) -> PerspectiveCamera:
        if self._manager.get_camera_type() == CameraType.PERSPECTIVE:
            return self._manager.get_camera()
        camera = PerspectiveCamera()
        self._manager.set_camera(camera)
        return camera
