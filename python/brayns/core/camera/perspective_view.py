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

from brayns.core.camera.camera_view import CameraView
from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.geometry.axis import Axis
from brayns.core.geometry.box import Box
from brayns.core.geometry.quaternion import Quaternion
from brayns.core.geometry.vector3 import Vector3


class PerspectiveView:

    def get_full_screen_distance(
        self,
        camera: PerspectiveCamera,
        target_height: float
    ) -> float:
        return target_height / 2 / math.tan(camera.fovy_radians / 2)

    def get_full_screen_view(
        self,
        camera: PerspectiveCamera,
        target: Box,
        translation: Vector3 = Vector3.zero,
        rotation: Quaternion = Quaternion.identity
    ) -> CameraView:
        center = target.center
        height = target.height
        distance = self.get_full_screen_distance(camera, height)
        position = center + distance * Axis.forward
        position += translation
        position = rotation.rotate(position, center)
        return CameraView(
            position=position,
            target=center,
            up=Axis.up
        )
