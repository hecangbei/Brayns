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

from typing import Iterator, TypeVar

from brayns.camera.camera_projection import CameraProjection
from brayns.client.client_protocol import ClientProtocol


class ProjectionRegistry:

    ProjectionType = TypeVar('ProjectionType', bound=CameraProjection)

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client
        self._types = dict[str, ProjectionRegistry.ProjectionType]()

    def __contains__(self, name: str) -> bool:
        return name in self._types

    def __len__(self) -> int:
        return len(self._types)

    def __iter__(self) -> Iterator[str]:
        yield from self._types.keys()

    def add_projection_type(self, projection_type: ProjectionType) -> None:
        name = projection_type.get_name()
        if name in self._types:
            raise RuntimeError(f'{name} registered twice')
        self._types[name] = projection_type

    def get_current_projection_name(self) -> str:
        return self._client.request('get-camera-type')

    def get_current_projection(self) -> CameraProjection:
        name = self.get_current_projection_name()
        message = self._client.request(f'get-camera-{name}')
        return self._types[name].from_dict(message)

    def set_current_projection(self, projection: CameraProjection) -> None:
        name = projection.get_name()
        self._client.request(f'set-camera-{name}', projection.to_dict())
