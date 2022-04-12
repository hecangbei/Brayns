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
from brayns.core.scene.model import Model
from brayns.core.scene.model_info import ModelInfo
from brayns.core.scene.scene import Scene
from brayns.core.serializers.model_info_serializer import ModelInfoSerializer
from brayns.core.serializers.model_serializer import ModelSerializer
from brayns.core.serializers.scene_serializer import SceneSerializer


class SceneManager:

    def __init__(self, client: ClientProtocol) -> None:
        self.__client = client
        self.__scene_serializer = SceneSerializer()
        self.__model_serializer = ModelSerializer()
        self.__model_info_serializer = ModelInfoSerializer()

    def get_scene(self) -> Scene:
        result = self.__client.request('get-scene')
        return self.__scene_serializer.deserialize(result)

    def get_model(self, id: int) -> Model:
        params = {'id': id}
        result = self.__client.request('get-model', params)
        return self.__model_serializer.deserialize(result)

    def update_model(self, model: Model) -> None:
        params = self.__model_serializer.serialize(model)
        self.__client.request('update-model', params)

    def add_model(self, model: ModelInfo) -> list[Model]:
        params = self.__model_info_serializer.serialize(model)
        result = self.__client.request('add-model', params)
        return [self.__model_serializer.deserialize(model) for model in result]

    def remove_models(self, ids: list[int]) -> None:
        params = {'ids': ids}
        self.__client.request('remove-model', params)

    def clear_models(self) -> None:
        scene = self.get_scene()
        ids = [model.id for model in scene.models]
        self.remove_models(ids)
