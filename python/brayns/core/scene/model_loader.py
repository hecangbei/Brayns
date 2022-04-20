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

from dataclasses import dataclass, field

from brayns.core.scene.model import Model
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class ModelLoader:

    name: str = ''
    properties: dict = field(default_factory=dict)

    def add_model(self, instance: InstanceProtocol, path: str) -> Model:
        params = {
            'path': path,
            'loader': self.name,
            'loader-properties': self.properties
        }
        result = instance.request('add-model', params)
        return Model.deserialize(result)
