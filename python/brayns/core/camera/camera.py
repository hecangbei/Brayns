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

from abc import ABC, abstractmethod
from typing import TypeVar

from brayns.instance.instance_protocol import InstanceProtocol

CameraType = TypeVar('CameraType', bound='Camera')


class Camera(ABC):

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls: type[CameraType], message: dict) -> CameraType:
        pass

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @staticmethod
    def get_current_camera_name(instance: InstanceProtocol) -> str:
        return instance.request('get-camera-type')

    @classmethod
    def from_instance(cls: type[CameraType], instance: InstanceProtocol) -> CameraType:
        name = cls.get_name()
        result = instance.request(f'get-camera-{name}')
        return cls.deserialize(result)

    @classmethod
    def is_main_camera(cls, instance: InstanceProtocol) -> None:
        return cls.get_name() == Camera.get_current_camera_name(instance)

    def use_as_main_camera(self, instance: InstanceProtocol) -> None:
        name = self.get_name()
        params = self.serialize()
        instance.request(f'set-camera-{name}', params)
