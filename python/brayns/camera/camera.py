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

from brayns.camera.camera_projection import CameraProjection
from brayns.camera.camera_view import CameraView
from brayns.client.client import Client
from brayns.geometry.quaternion import Quaternion
from brayns.geometry.vector3 import Vector3


class Camera:

    def __init__(self, client: Client) -> None:
        self._client = client

    @property
    def view(self) -> CameraView:
        return CameraView.from_dict(self._client.request('get-camera-look-at'))

    @view.setter
    def view(self, value: CameraView) -> None:
        self._client.request('set-camera-look-at', value.to_dict())

    @property
    def position(self) -> Vector3:
        return self.view.position

    @position.setter
    def position(self, value: Vector3) -> None:
        self.view = self.view.update(position=value)

    @property
    def target(self) -> Vector3:
        return self.view.target

    @target.setter
    def target(self, value: Vector3) -> None:
        self.view = self.view.update(target=value)

    @property
    def up(self) -> Vector3:
        return self.view.up

    @up.setter
    def up(self, value: Vector3) -> None:
        self.view = self.view.update(up=value)

    def set_projection(self, projection: CameraProjection) -> None:
        self._client.request(
            method=f'set-camera-{projection.get_name()}',
            params=projection.get_properties()
        )

    def reset(self) -> None:
        self.view = CameraView()

    def rotate(self, rotation: Quaternion) -> None:
        self.position = rotation.rotate(self.position, self.target)
