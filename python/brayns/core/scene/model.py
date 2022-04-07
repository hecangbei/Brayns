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

from dataclasses import InitVar, dataclass

from brayns.core.geometry.box import Box
from brayns.core.geometry.transform import Transform


@dataclass
class Model:

    id: InitVar[int]
    bounds: InitVar[Box]
    metadata: InitVar[dict[str, str]]
    visible: bool
    transform: Transform

    def __post_init__(
        self,
        id: int,
        bounds: Box,
        metadata: dict[str, str]
    ) -> None:
        self._id = id
        self._bounds = bounds
        self._metadata = metadata

    @property
    def id(self) -> int:
        return self._id

    @property
    def bounds(self) -> Box:
        return self._bounds

    @property
    def metadata(self) -> dict[str, str]:
        return self._metadata
