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

from brayns.core.geometry.axis import Axis
from brayns.core.geometry.quaternion import Quaternion


class View:

    @classmethod
    @property
    def default(cls) -> Quaternion:
        return cls.front

    @classmethod
    @property
    def left(cls) -> Quaternion:
        return Quaternion.from_axis_angle(Axis.up, -90, degrees=True)

    @classmethod
    @property
    def right(cls) -> Quaternion:
        return Quaternion.from_axis_angle(Axis.up, 90, degrees=True)

    @classmethod
    @property
    def top(cls) -> Quaternion:
        return Quaternion.from_axis_angle(Axis.right, -90, degrees=True)

    @classmethod
    @property
    def bottom(cls) -> Quaternion:
        return Quaternion.from_axis_angle(Axis.right, 90, degrees=True)

    @classmethod
    @property
    def front(cls) -> Quaternion:
        return Quaternion.identity

    @classmethod
    @property
    def back(cls) -> Quaternion:
        return Quaternion.from_axis_angle(Axis.right, 180, degrees=True)
