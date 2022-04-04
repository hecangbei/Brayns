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

from brayns.instance.camera.camera_projection import CameraProjection
from brayns.common.geometry.box import Box


class PerspectiveProjection(CameraProjection):

    @staticmethod
    def get_name() -> str:
        return 'perspective'

    @staticmethod
    def from_dict(message: dict) -> 'PerspectiveProjection':
        return PerspectiveProjection(
            fovy=message['fovy'],
            aperture_radius=message['aperture_radius'],
            focus_distance=message['focus_distance'],
            degrees=True
        )

    def __init__(
        self,
        fovy: float = math.radians(45),
        aperture_radius: float = 0.0,
        focus_distance: float = 1.0,
        degrees: bool = False
    ) -> None:
        self._fovy = math.radians(fovy) if degrees else fovy
        self._aperture_radius = aperture_radius
        self._focus_distance = focus_distance

    @property
    def fovy_radians(self) -> float:
        return self._fovy

    @property
    def fovy_degrees(self) -> float:
        return math.degrees(self._fovy)

    @property
    def aperture_radius(self) -> float:
        return self._aperture_radius

    @property
    def focus_distance(self) -> float:
        return self._focus_distance

    def to_dict(self) -> dict:
        return {
            'fovy': self.fovy_degrees,
            'aperture_radius': self.aperture_radius,
            'focus_distance': self.focus_distance
        }

    def get_full_screen_distance(self, bounds: Box) -> float:
        return bounds.size.y / 2 / math.tan(self._fovy / 2)
