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

from brayns.instance.instance_protocol import InstanceProtocol
from brayns.core.geometry.box import Box
from brayns.core.geometry.transform import Transform
from brayns.core.geometry.vector3 import Vector3
from brayns.core.scene.model import Model
from brayns.core.scene.scene import Scene
from brayns.core.serializers.transform_serializer import TransformSerializer


def serialize_box(box: Box) -> dict:
    return {
        'min': list(box.min),
        'max': list(box.max)
    }


def serialize_model(model: Model) -> dict:
    return {
        'id': model.id,
        'bounds': serialize_box(model.bounds),
        'metadata': model.metadata,
        'visible': model.visible,
        'transformation': TransformSerializer().serialize(model.transform)
    }


def serialize_scene(scene: Scene) -> dict:
    return {
        'bounds': serialize_box(scene.bounds),
        'models': [serialize_model(model) for model in scene.models]
    }


class MockSceneClient(InstanceProtocol):

    def __init__(self) -> None:
        self.scene = Scene()
        self.received_params = []
        self._id = 0

    @property
    def models(self) -> list[Model]:
        return self.scene.models

    def create_model(self) -> Model:
        self._id += 1
        return Model(
            id=self._id,
            bounds=Box(-Vector3.one, Vector3.one),
            metadata={},
            visible=True,
            transform=Transform.identity
        )

    def get_scene(self) -> dict:
        return serialize_scene(self.scene)

    def add_model(self) -> Model:
        model = self.create_model()
        self.models.append(model)
        return model

    def get_model(self, id: int) -> Model:
        return next(model for model in self.models if model.id == id)

    def update_model(self, params: dict) -> None:
        model = self.get_model(params['id'])
        model.visible = params['visible']
        model.transform = TransformSerializer().deserialize(
            params['transformation']
        )

    def remove_model(self, params: dict) -> None:
        self.scene.models = [
            model for model in self.models
            if model.id not in params['ids']
        ]

    def request(self, method: str, params: Any = None) -> Any:
        self.received_params.append(params)
        if method == 'get-scene':
            return self.get_scene()
        if method == 'get-model':
            model = self.get_model(params['id'])
            return serialize_model(model)
        if method == 'add-model':
            model = self.add_model()
            return [serialize_model(model)]
        if method == 'update-model':
            return self.update_model(params)
        if method == 'remove-model':
            return self.remove_model(params)
        raise RuntimeError('Test error')
