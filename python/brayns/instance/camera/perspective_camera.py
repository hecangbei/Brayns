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

from brayns.client.client import Client
from brayns.utils.box import Box
from brayns.utils.quaternion import Quaternion
from brayns.utils.vector3 import Vector3


class PerspectiveCamera:

    def __init__(self, client: Client) -> None:
        self._client = client

    @property
    def fovy(self) -> float:
        return self['fovy']

    @fovy.setter
    def fovy(self, value: float) -> None:
        self['fovy'] = value

    @property
    def aspect(self) -> float:
        return self['aspect']

    @aspect.setter
    def aspect(self, value: float) -> None:
        self._update_params({'aspect': value})

    @property
    def aperture_radius(self) -> float:
        return self['apertureRadius']

    @aperture_radius.setter
    def aperture_radius(self, value: float) -> None:
        self._update_params({'apertureRadius': value})

    @property
    def focus_distance(self) -> float:
        return self['focusDistance']

    @focus_distance.setter
    def focus_distance(self, value: float) -> None:
        self._update_params({'focusDistance': value})

    @property
    def enable_clipping_planes(self) -> bool:
        return self['enableClippingPlanes']

    @enable_clipping_planes.setter
    def enable_clipping_planes(self, value: bool) -> None:
        self._update_params({'enableClippingPlanes': value})

    def center(self, scene: Box) -> None:
        self.orientation = Quaternion.identity()
        self.target = scene.center
        position = scene.center
        dezoom = scene.size.y / 2 / math.tan(self.fovy / 2)
        position += dezoom * Vector3.forward()
        self.position = position
