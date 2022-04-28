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

from brayns.instance.instance import Instance


class MockMaterialInstance(Instance):

    def __init__(self) -> None:
        self.properties = list[dict]()
        self.names = list[str]()
        self.method = ''
        self.params = None

    def request(self, method: str, params: Any = None) -> Any:
        self.method = method
        self.params = params
        if method == 'get-material-type':
            id = params['id']
            return self.names[id]
        if method.startswith('get-material-'):
            id = params['id']
            name = method.split('-')[2]
            if name != self.names[id]:
                raise RuntimeError(f'Current material is not {name}')
            return self.properties[id]
        if method.startswith('set-material-'):
            id = params['model_id']
            name = method.split('-')[2]
            if name != self.names[id]:
                raise RuntimeError()
            self.properties[id] = params['material']
            return None
        raise RuntimeError('Invalid request')
