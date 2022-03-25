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
from brayns.utils.quaternion import Quaternion
from brayns.utils.transform import Transform
from brayns.utils.vector3 import Vector3


class MockSceneClient(ClientProtocol):

    def __init__(self) -> None:
        self._scene = {
            'bounds': {
                'min': [1, 2, 3],
                'max': [4, 5, 6]
            },
            'models': []
        }
        self._id = 0
        self._params = []

    def get_received_params(self) -> list:
        return self._params

    def add_mock_model(self) -> dict:
        model = self._create_mock_model()
        self.get_models().append(model)
        return model

    def get_models(self) -> list[dict]:
        return self._scene['models']

    def get_model_ids(self) -> list[int]:
        return [model['id'] for model in self.get_models()]

    def get_model(self, id: int) -> dict:
        return [
            model for model in self.get_models()
            if model['id'] == id
        ][0]

    def get_bounds(self) -> dict:
        return self._scene['bounds']

    def request(self, method: str, params: Any = None) -> Any:
        self._params.append(params)
        if method == 'get-scene':
            return self._scene
        if method == 'get-model':
            return self.get_model(params['id'])
        if method == 'add-model':
            return [self.add_mock_model()]
        if method == 'update-model':
            return self._update_model(params)
        if method == 'remove-model':
            return self._remove_model(params)
        raise RuntimeError('Test error')

    def _create_mock_model(self) -> dict:
        self._id += 1
        return {
            'id': self._id - 1,
            'bounds': self._scene['bounds'],
            'metadata': {'test': '123'},
            'visible': True,
            'transformation': Transform(
                Vector3(0, 0, 0),
                Quaternion(0, 0, 0, 1),
                Vector3(1, 1, 1)
            ).to_dict()
        }

    def _update_model(self, params: dict) -> None:
        model = self.get_model(params['id'])
        model.update(params)

    def _remove_model(self, params: dict) -> None:
        self._scene['models'] = [
            model for model in self.get_models()
            if model['id'] not in params['ids']
        ]
