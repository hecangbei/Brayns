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

from brayns.instance.instance_protocol import InstanceProtocol
from brayns.core.scene.model import Model
from brayns.core.scene.model_info import ModelInfo
from brayns.core.scene.scene_manager import SceneManager
from brayns.plugins.circuit.circuit_info import CircuitInfo
from brayns.plugins.serializers.circuit_info_serializer import CircuitInfoSerializer


class CircuitManager(SceneManager):

    def __init__(self, client: InstanceProtocol) -> None:
        self._scene = SceneManager(client)
        self._serializer = CircuitInfoSerializer()

    def load_circuit(
        self,
        path: str,
        info: CircuitInfo = CircuitInfo()
    ) -> Model:
        properties = self._serializer.serialize(info)
        model = ModelInfo(
            path=path,
            loader_properties=properties
        )
        return self._scene.add_model(model)
