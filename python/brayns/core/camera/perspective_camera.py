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

from brayns.core.camera.camera_view import CameraView
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.box import Box


@dataclass
class PerspectiveCamera:

    fovy: InitVar[float] = math.radians(45)
    aperture_radius: float = 0.0
    focus_distance: float = 1.0
    degrees: InitVar[bool] = False

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

    def get_full_screen_distance(self, target_height: float) -> float:
        return target_height / 2 / math.tan(self.fovy_radians / 2)

    def get_full_screen_view(self, target: Box) -> CameraView:
        center = target.center
        height = target.height
        distance = self.get_full_screen_distance(height)
        position = center + distance * Axis.forward
        return CameraView(position, center)
