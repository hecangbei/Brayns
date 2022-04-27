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

from brayns.core.common.transform import Transform
from brayns.core.scene.model import Model
from brayns.instance.instance_protocol import InstanceProtocol


class MockSceneInstance(InstanceProtocol):

    def __init__(self) -> None:
        self.models = list[dict]()
        self.bounds = {
            'min': [-1, -1, -1],
            'max': [1, 1, 1]
        }
        self.method = ''
        self.params = None
        self._id = 0

    def create_model(self) -> Model:
        self._id += 1
        return {
            'id': self._id,
            'bounds': self.bounds,
            'metadata': {
                'test1': '1',
                'test2': '2'
            },
            'visible': True,
            'transformation': Transform.identity.serialize()
        }

    def get_scene(self) -> dict:
        return {
            'models': self.models,
            'bounds': self.bounds
        }

    def add_model(self) -> dict:
        model = self.create_model()
        self.models.append(model)
        return model

    def get_model(self, id: int) -> dict:
        return next(model for model in self.models if model['id'] == id)

    def update_model(self, params: dict) -> None:
        model = self.get_model(params['id'])
        model.update(params)

    def remove_model(self, params: dict) -> None:
        self.models = [
            model for model in self.models
            if model['id'] not in params['ids']
        ]

    def request(self, method: str, params: Any = None) -> Any:
        self.method = method
        self.params = params
        if method == 'get-scene':
            return self.get_scene()
        if method == 'get-model':
            return self.get_model(params['id'])
        if method == 'add-model':
            return [self.add_model()]
        if method == 'update-model':
            return self.update_model(params)
        if method == 'remove-model':
            return self.remove_model(params)
        raise RuntimeError('Test error')
