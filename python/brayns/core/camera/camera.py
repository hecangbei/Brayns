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

from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.box import Box
from brayns.instance.instance_protocol import InstanceProtocol

CameraType = TypeVar('CameraType', bound='Camera')


class Camera(ABC):

    @staticmethod
    def get_current_camera_name(instance: InstanceProtocol) -> str:
        return instance.request('get-camera-type')

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_main_camera(cls, instance: InstanceProtocol) -> None:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls: type[CameraType], message: dict) -> CameraType:
        pass

    @classmethod
    def is_main_camera(cls, instance: InstanceProtocol) -> None:
        return cls.get_name() == Camera.get_current_camera_name(instance)

    @abstractmethod
    def use_as_main_camera(self, instance: InstanceProtocol) -> None:
        pass

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @abstractmethod
    def center(self, instance: InstanceProtocol, target: Box) -> None:
        pass
