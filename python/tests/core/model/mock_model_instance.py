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
from brayns.instance.instance import Instance


class MockModelInstance(Instance):

    def __init__(self) -> None:
        self.bounds = {
            'min': [0, 0, 0],
            'max': [1, 1, 1]
        }
        self.model = {
            'id': 1,
            'bounds': self.bounds,
            'metadata': {},
            'visible': True,
            'transformation': Transform.identity.serialize()
        }
        self.models = [
            self.model | {'id': 0},
            self.model | {'id': 1},
        ]
        self.scene = {
            'bounds': self.bounds,
            'models': self.models
        }
        self.method = ''
        self.params = None

    def request(self, method: str, params: Any = None) -> Any:
        self.method = method
        self.params = params
        if method == 'get-scene':
            return self.scene
        if method == 'get-model':
            return self.model
        if method == 'add-model':
            return self.models
        if method == 'update-model':
            return None
        if method == 'remove-model':
            return None
        if method == 'enable-simulation':
            return None
        raise RuntimeError('Test error')
