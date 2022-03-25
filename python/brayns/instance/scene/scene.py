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

from brayns.client.client_protocol import ClientProtocol
from brayns.utils.box import Box
from brayns.utils.vector3 import Vector3
from brayns.instance.scene.model_registry import ModelRegistry


class Scene:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client
        self._models = ModelRegistry(client)

    @property
    def models(self) -> ModelRegistry:
        return self._models

    @property
    def bounds(self) -> Box:
        return Box.from_dict(self._client.request('get-scene')['bounds'])

    @property
    def center(self) -> Vector3:
        return self.bounds.center

    @property
    def size(self) -> Vector3:
        return self.bounds.size
