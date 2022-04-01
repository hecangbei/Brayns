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
from brayns.geometry.transform import Transform
from tests.scene.mock_scene import MockScene
from tests.scene.mock_scene_model import MockSceneModel


class MockSceneClient(ClientProtocol):

    def __init__(self) -> None:
        self.scene = MockScene()
        self.received_params = []
        self._id = 0

    @property
    def models(self) -> list[MockSceneModel]:
        return self.scene.models

    def create_model(self) -> MockSceneModel:
        self._id += 1
        return MockSceneModel(id=self._id)

    def add_model(self) -> MockSceneModel:
        model = self.create_model()
        self.models.append(model)
        return model

    def get_model(self, id: int) -> MockSceneModel:
        return next(model for model in self.models if model.id == id)

    def update_model(self, params: dict) -> None:
        model = self.get_model(params['id'])
        model.visible = params.get('visible', model.visible)
        model.transform = Transform.from_dict(
            params.get('transformation', model.transform.to_dict())
        )

    def remove_model(self, params: dict) -> None:
        self.scene.models = [
            model for model in self.models
            if model.id not in params['ids']
        ]

    def request(self, method: str, params: Any = None) -> Any:
        self.received_params.append(params)
        if method == 'get-scene':
            return self.scene.to_dict()
        if method == 'get-model':
            return self.get_model(params['id']).to_dict()
        if method == 'add-model':
            return [self.add_model().to_dict()]
        if method == 'update-model':
            return self.update_model(params)
        if method == 'remove-model':
            return self.remove_model(params)
        raise RuntimeError('Test error')
