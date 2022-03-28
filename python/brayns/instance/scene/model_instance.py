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
from brayns.utils.box import Box
from brayns.utils.quaternion import Quaternion
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3


class ModelInstance:

    def __init__(self, client: ClientProtocol, id: int) -> None:
        self._client = client
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    @property
    def bounds(self) -> Box:
        return Box.from_dict(self._get()['bounds'])

    @property
    def metadata(self) -> dict[str, str]:
        return self._get()['metadata']

    @property
    def visible(self) -> bool:
        return self._get()['visible']

    @visible.setter
    def visible(self, value: bool) -> None:
        self._update({'visible': value})

    @property
    def transform(self) -> Transform:
        return Transform.from_dict(self._get()['transformation'])

    @transform.setter
    def transform(self, value: Transform) -> None:
        self._update({'transformation': value.to_dict()})

    @property
    def position(self) -> Vector3:
        return self.bounds.center + self.transform.translation

    @position.setter
    def position(self, value: Vector3) -> None:
        self.translate(value - self.position)

    @property
    def orientation(self) -> Quaternion:
        return self.transform.rotation

    @orientation.setter
    def orientation(self, value: Quaternion) -> None:
        self.transform = self.transform.update(rotation=value)

    def translate(self, translation: Vector3) -> None:
        self.transform = self.transform.translate(translation)

    def rotate(self, rotation: Quaternion, center=Vector3.full(0)) -> None:
        self.transform = self.transform.rotate(rotation, center)

    def rescale(self, scale: Vector3) -> None:
        self.transform = self.transform.rescale(scale)

    def _get(self) -> Any:
        return self._client.request('get-model', {'id': self._id})

    def _update(self, values: dict) -> None:
        message = {'id': self._id}
        message.update(values)
        self._client.request('update-model', message)
