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
from brayns.common.geometry.box import Box
from brayns.common.geometry.transform import Transform


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

    def _get(self) -> Any:
        return self._client.request('get-model', {'id': self._id})

    def _update(self, values: dict) -> None:
        message = {'id': self._id}
        message.update(values)
        self._client.request('update-model', message)
