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


class MockLightInstance(Instance):

    def __init__(self) -> None:
        self.lights = list[dict]()
        self.names = list[str]()
        self.method = ''
        self.params = None

    def request(self, method: str, params: Any = None) -> Any:
        self.method = method
        self.params = params
        if method == 'remove-lights':
            ids = params['ids']
            self.lights = [
                light
                for id, light in enumerate(self.lights)
                if id not in ids
            ]
            self.names = [
                name
                for id, name in enumerate(self.names)
                if id not in ids
            ]
            return None
        if method == 'clear-lights':
            self.lights.clear()
            self.names.clear()
            return None
        if method.startswith('add-light-'):
            name = method.split('-')[2]
            self.names.append(name)
            self.lights.append(params)
            return len(self.names) - 1
        raise RuntimeError('Invalid request')
