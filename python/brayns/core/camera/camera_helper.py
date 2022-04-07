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

from brayns.core.camera.camera_view import CameraView
from brayns.core.camera.perspective_camera import PerspectiveCamera
from brayns.core.geometry.vector3 import Vector3


class CameraHelper:

    @staticmethod
    def serialize_view(view: CameraView) -> dict:
        return {
            'position': list(view.position),
            'target': list(view.target),
            'up': list(view.up),
        }

    @staticmethod
    def deserialize_view(message: dict) -> CameraView:
        return CameraView(
            position=Vector3(*message['position']),
            target=Vector3(*message['target']),
            up=Vector3(*message['up'])
        )

    @staticmethod
    def serialize_perspective(camera: PerspectiveCamera) -> dict:
        return {
            'fovy': camera.fovy_degrees,
            'aperture_radius': camera.aperture_radius,
            'focus_distance': camera.focus_distance
        }

    @staticmethod
    def deserialize_perspective(message: dict) -> PerspectiveCamera:
        return PerspectiveCamera(
            fovy=message['fovy'],
            aperture_radius=message['aperture_radius'],
            focus_distance=message['focus_distance'],
            degrees=True
        )
