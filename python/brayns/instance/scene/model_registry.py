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

from typing import Iterable, Iterator, Union

from brayns.client.client_protocol import ClientProtocol
from brayns.instance.scene.model_instance import ModelInstance
from brayns.instance.scene.model_protocol import ModelProtocol


class ModelRegistry:

    def __init__(self, client: ClientProtocol) -> None:
        self._client = client

    def __len__(self) -> int:
        return len(self._get_models())

    def __contains__(self, item: Union[int, ModelInstance]) -> bool:
        id = item if isinstance(item, int) else item.id
        return id in (model.id for model in self)

    def __iter__(self) -> Iterator[ModelInstance]:
        yield from (
            self._create_instance(model)
            for model in self._get_models()
        )

    def __getitem__(self, id: int) -> ModelInstance:
        self._check_model_exists(id)
        return ModelInstance(self._client, id)

    def add(self, model: ModelProtocol) -> list[ModelInstance]:
        return [
            self._create_instance(message)
            for message in self._client.request('add-model', {
                'path': model.get_path(),
                'loader_name': model.get_loader(),
                'loader_properties': model.get_loader_properties()
            })
        ]

    def remove(self, ids: Iterable[int]) -> None:
        self._client.request('remove-model', {'ids': list(ids)})

    def clear(self) -> None:
        self.remove([model['id'] for model in self._get_models()])

    def _check_model_exists(self, id: int) -> None:
        self._client.request('get-model', {'id': id})

    def _get_models(self) -> list[dict]:
        return self._client.request('get-scene')['models']

    def _create_instance(self, message: dict) -> ModelInstance:
        return ModelInstance(self._client, message['id'])
