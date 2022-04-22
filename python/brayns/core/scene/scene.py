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

from brayns.core.geometry.box import Box
from brayns.core.scene.model import Model
from brayns.instance.instance_protocol import InstanceProtocol


class Scene:

    @staticmethod
    def from_instance(instance: InstanceProtocol) -> 'Scene':
        result = instance.request('get-scene')
        return Scene.deserialize(result)

    @staticmethod
    def deserialize(message: dict) -> 'Scene':
        return Scene(
            bounds=Box.deserialize(message['bounds']),
            models=tuple(
                Model.deserialize(model)
                for model in message['models']
            )
        )

    @staticmethod
    def remove_models(instance: InstanceProtocol, ids: list[int]) -> None:
        instance.request('remove-model', {'ids': ids})

    @staticmethod
    def clear_models(instance: InstanceProtocol) -> None:
        scene = Scene.from_instance(instance)
        ids = [model.id for model in scene.models]
        Scene.remove_models(instance, ids)

    def __init__(
        self,
        bounds: Box,
        models: tuple[Model]
    ) -> None:
        self._bounds = bounds
        self._models = models

    @property
    def bounds(self) -> Box:
        return self._bounds
    
    @property
    def models(self) -> tuple[Model]:
        return self._models
