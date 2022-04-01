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

from brayns.camera.camera_projection import CameraProjection
from brayns.geometry.box import Box


class MockCameraProjection(CameraProjection):

    @staticmethod
    def get_name() -> str:
        return 'test'

    @staticmethod
    def from_dict(message: dict) -> 'CameraProjection':
        return MockCameraProjection(
            message['test1'],
            message['test2'],
        )

    def __init__(self, test1: int = 1, test2: int = 2) -> None:
        self.test1 = test1
        self.test2 = test2

    def to_dict(self) -> dict:
        return {
            'test1': self.test1,
            'test2': self.test2
        }

    def get_full_screen_distance(self, bounds: Box) -> float:
        return bounds.center
