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

from types import MappingProxyType

from brayns.core.geometry.box import Box
from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.transform import Transform
from brayns.core.geometry.vector3 import Vector3
from brayns.instance.instance_protocol import InstanceProtocol


class Model:

    @staticmethod
    def from_instance(instance: InstanceProtocol, id: int) -> 'Model':
        result = instance.request('get-model', {'id': id})
        return Model.deserialize(result)

    @staticmethod
    def deserialize(message: dict) -> 'Model':
        return Model(
            id=message['id'],
            bounds=Box.deserialize(message['bounds']),
            metadata=MappingProxyType(message['metadata']),
            visible=message['visible'],
            transform=Transform.deserialize(message['transformation'])
        )

    def __init__(
        self,
        id: int,
        bounds: Box,
        metadata: MappingProxyType[str, str],
        visible: bool,
        transform: Transform
    ) -> None:
        self._id = id
        self._bounds = bounds
        self._metadata = metadata
        self._visible = visible
        self._transform = transform

    @property
    def id(self) -> int:
        return self._id

    @property
    def bounds(self) -> Box:
        return self._bounds

    @property
    def metadata(self) -> MappingProxyType[str, str]:
        return self._metadata

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value

    @property
    def transform(self) -> Transform:
        return self._transform

    @transform.setter
    def transform(self, value: Transform) -> None:
        self._transform = value

    @property
    def translation(self) -> Vector3:
        return self._transform.translation

    @translation.setter
    def translation(self, value: Vector3) -> None:
        self._transform = self._transform.with_translation(value)

    @property
    def rotation(self) -> Quaternion:
        return self._transform.rotation

    @rotation.setter
    def rotation(self, value: Quaternion) -> None:
        self._transform = self._transform.with_rotation(value)

    @property
    def scale(self) -> Vector3:
        return self._transform.scale

    @scale.setter
    def scale(self, value: Vector3) -> None:
        self._transform = self._transform.with_scale(value)

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'visible': self.visible,
            'transformation': self.transform.serialize()
        }

    def update(self, instance: InstanceProtocol) -> None:
        params = self.serialize()
        instance.request('update-model', params)

    def translate(self, translation: Vector3) -> None:
        self.translation += translation

    def rotate(self, rotation: Quaternion, center: Vector3 = Vector3.zero) -> None:
        self._transform = self._transform.rotate(rotation, center)

    def rescale(self, scale: Vector3) -> None:
        self.scale *= scale
