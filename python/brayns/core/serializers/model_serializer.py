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

from brayns.core.scene.model import Model
from brayns.core.serializers.box_serializer import BoxSerializer
from brayns.core.serializers.transform_serializer import TransformSerializer


class ModelSerializer:

    def __init__(self) -> None:
        self._box_serializer = BoxSerializer()
        self._transform_serializer = TransformSerializer()

    def serialize(self, model: Model) -> dict:
        return {
            'id': model.id,
            'visible': model.visible,
            'transformation': self._transform_serializer.serialize(
                model.transform
            )
        }

    def deserialize(self, message: dict) -> Model:
        return Model(
            id=message['id'],
            bounds=self._box_serializer.deserialize(
                message['bounds']
            ),
            metadata=message['metadata'],
            visible=message['visible'],
            transform=self._transform_serializer.deserialize(
                message['transformation']
            )
        )
