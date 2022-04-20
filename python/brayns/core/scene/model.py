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

from dataclasses import dataclass

from brayns.core.geometry.box import Box
from brayns.core.geometry.transform import Transform
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class Model:

    id: int
    bounds: Box
    metadata: dict[str, str]
    visible: bool
    transform: Transform

    @staticmethod
    def from_instance(instance: InstanceProtocol, id: int) -> 'Model':
        result = instance.request('get-model', {'id': id})
        return Model.deserialize(result)

    @staticmethod
    def deserialize(message: dict) -> 'Model':
        return Model(
            id=message['id'],
            bounds=Box.deserialize(message['bounds']),
            metadata=message['metadata'],
            visible=message['visible'],
            transform=Transform.deserialize(message['transformation'])
        )

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'visible': self.visible,
            'transformation': self.transform.serialize()
        }

    def update(self, instance: InstanceProtocol) -> None:
        params = self.serialize()
        instance.request('update-model', params)
