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

from typing import Any, Optional

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
    def transform(self) -> Transform:
        return Transform.from_dict(self._get_transform())

    @transform.setter
    def transform(self, value: Transform) -> None:
        self._update_transform(value.to_dict())

    @property
    def position(self) -> Vector3:
        return self.transform.translation

    @position.setter
    def position(self, value: Vector3) -> None:
        self._update_transform({'translation': list(value)})

    @property
    def orientation(self) -> Quaternion:
        return self.transform.rotation

    @orientation.setter
    def orientation(self, value: Quaternion) -> None:
        self._update_transform({'rotation': list(value)})

    @property
    def visible(self) -> bool:
        return self._get()['visible']

    @visible.setter
    def visible(self, value: bool) -> None:
        self._update({'visible': value})

    def translate(self, value: Vector3) -> None:
        self.position = self.position + value

    def rotate(self, value: Quaternion, around: Optional[Vector3] = None) -> None:
        if around is not None:
            self.position = value.apply_around(value, around)
        self.rotation = value * self.rotation

    def _get(self) -> Any:
        return self._client.request('get-model', {'id': self._id})

    def _update(self, values: dict) -> None:
        self._client.request('update-model', values)

    def _get_transform(self) -> dict:
        return self._get()['transformation']

    def _update_transform(self, values: dict) -> None:
        transform = self._get_transform()
        transform.update(values)
        self._update({'transformation': transform})
