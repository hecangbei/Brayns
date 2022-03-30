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

from brayns.client.client import Client
from brayns.instance.camera.camera_projection import CameraProjection
from brayns.utils.quaternion import Quaternion
from brayns.utils.vector3 import Vector3


class Camera:

    def __init__(self, client: Client) -> None:
        self._client = client

    @property
    def position(self) -> Vector3:
        return Vector3(*self._get()['position'])

    @position.setter
    def position(self, value: Vector3) -> None:
        self._update({'position': list(value)})

    @property
    def target(self) -> Vector3:
        return Vector3(*self._get()['target'])

    @target.setter
    def target(self, value: Vector3) -> None:
        self._update({'target': list(value)})

    @property
    def up(self) -> Vector3:
        return Vector3(*self._get()['up'])

    @up.setter
    def up(self, value: Vector3) -> None:
        self._update({'up': list(value)})

    def set_projection(self, projection: CameraProjection) -> None:
        self._client.request(
            method=f'set-camera-{projection.get_name()}',
            params=projection.get_properties()
        )

    def reset(self) -> None:
        self.position = Vector3.zero()
        self.target = Vector3.zero()
        self.up = Vector3.up()

    def rotate_around_target(self, rotation: Quaternion) -> None:
        self.position = rotation.rotate(self.position, self.target)

    def _get(self) -> dict:
        return self._client.request('get-camera-look-at')

    def _update(self, values: dict) -> None:
        self._client.request('set-camera-look-at', values)
