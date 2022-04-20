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

import math
from dataclasses import InitVar, dataclass

from brayns.core.camera.camera import Camera
from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.box import Box
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class PerspectiveCamera(Camera):

    fovy: InitVar[float] = math.radians(45)
    aperture_radius: float = 0.0
    focus_distance: float = 1.0
    degrees: InitVar[bool] = False

    @classmethod
    def get_name(cls) -> str:
        return 'perspective'

    @classmethod
    def from_main_camera(cls, instance: InstanceProtocol) -> 'PerspectiveCamera':
        result = instance.request('get-camera-perspective')
        return PerspectiveCamera.deserialize(result)

    @classmethod
    def deserialize(cls, message) -> 'PerspectiveCamera':
        return PerspectiveCamera(
            fovy=message['fovy'],
            aperture_radius=message['aperture_radius'],
            focus_distance=message['focus_distance'],
            degrees=True
        )

    def __post_init__(self, fovy: float, degrees: bool) -> None:
        self._fovy = math.radians(fovy) if degrees else fovy

    @property
    def fovy_radians(self) -> float:
        return self._fovy

    @fovy_radians.setter
    def fovy_radians(self, value: float) -> None:
        self._fovy = value

    @property
    def fovy_degrees(self) -> float:
        return math.degrees(self._fovy)

    @fovy_degrees.setter
    def fovy_degrees(self, value: float) -> None:
        self._fovy = math.radians(value)

    def use_as_main_camera(self, instance: InstanceProtocol) -> None:
        instance.request('set-camera-perspective', self.serialize())

    def serialize(self) -> dict:
        return {
            'fovy': self.fovy_degrees,
            'aperture_radius': self.aperture_radius,
            'focus_distance': self.focus_distance
        }

    def center(self, instance: InstanceProtocol, target: Box) -> None:
        view = self.get_full_screen_view(target)
        view.use_for_main_camera(instance)

    def get_full_screen_view(self, target: Box) -> CameraView:
        center = target.center
        distance = target.height / 2 / math.tan(self.fovy_radians / 2)
        position = center + distance * Axis.forward
        return CameraView(position, center)
