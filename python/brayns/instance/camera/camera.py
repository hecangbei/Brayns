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

from brayns.client.client import Client
from brayns.utils.quaternion import Quaternion
from brayns.utils.vector3 import Vector3


class Camera:

    def __init__(self, client: Client) -> None:
        self._client = client

    def __getitem__(self, key: str) -> Any:
        self._client.request('get-camera-params')[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._client.request('set-camera-params', {key: value})

    @property
    def name(self) -> str:
        return self._get()['current']

    @property
    def position(self) -> Vector3:
        return self._get()['position']

    @position.setter
    def position(self, value: Vector3) -> None:
        return self._update({'position': list(value)})

    @property
    def orientation(self) -> Quaternion:
        return self._get()['orientation']

    @orientation.setter
    def orientation(self, value: Quaternion) -> None:
        return self._update({'orientation': list(value)})

    @property
    def target(self) -> Vector3:
        return self._get()['target']

    @target.setter
    def target(self, value: Vector3) -> None:
        return self._update({'target': list(value)})

    def rotate_around_target(self, rotation: Quaternion) -> None:
        self.orientation = rotation * self.orientation
        self.position = rotation.rotate(self.position, self.target)

    def reset(self) -> None:
        self.position = Vector3.zero()
        self.orientation = Quaternion.identity()
        self.target = Vector3.zero()

    def _get(self) -> dict:
        return self._client.request('get-camera')

    def _update(self, values: dict) -> None:
        self._client.request('set-camera', values)
