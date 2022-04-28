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

from brayns.instance.instance import Instance


class ApplicationParameters:

    @staticmethod
    def from_instance(instance: Instance) -> 'ApplicationParameters':
        result = instance.request('get-application-parameters')
        return ApplicationParameters.deserialize(result)

    @staticmethod
    def deserialize(message: dict) -> 'ApplicationParameters':
        return ApplicationParameters(
            plugins=tuple(message['plugins']),
            resolution=tuple(message['viewport'])
        )

    def __init__(
        self,
        plugins: tuple[str],
        resolution: tuple[int, int]
    ) -> None:
        self._plugins = plugins
        self._resolution = resolution

    @property
    def plugins(self) -> tuple[str]:
        return self._plugins

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution

    @resolution.setter
    def resolution(self, value: tuple[int, int]) -> None:
        self._resolution = value

    def update(self, instance: Instance) -> None:
        params = self.serialize()
        instance.request('set-application-parameters', params)

    def serialize(self) -> dict:
        return {
            'viewport': list(self.resolution)
        }
