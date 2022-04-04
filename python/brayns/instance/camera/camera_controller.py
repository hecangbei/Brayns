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

from brayns.common.geometry.box import Box
from brayns.common.geometry.quaternion import Quaternion
from brayns.common.geometry.vector3 import Vector3
from brayns.instance.camera.camera import Camera
from brayns.instance.camera.camera_view import CameraView


class CameraController:

    def __init__(self, camera: Camera) -> None:
        self._camera = camera

    def reset(self) -> None:
        self._camera.view = CameraView()

    def translate(self, translation: Vector3) -> None:
        self._camera.position += translation

    def rotate_around_target(self, rotation: Quaternion) -> None:
        self._camera.position = rotation.rotate(
            self._camera.position,
            self._camera.target
        )

    def look_at(self, bounds: Box) -> None:
        center = bounds.center
        distance = self._camera.get_full_screen_distance(bounds)
        self._camera.position = center + distance * Vector3.forward()
        self._camera.target = center
        self._camera.up = Vector3.up()
