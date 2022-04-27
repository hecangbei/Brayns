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

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Cells:

    density: float = 1.0
    targets: list[str] = field(default_factory=list)
    gids: list[int] = field(default_factory=list)

    @staticmethod
    def all() -> 'Cells':
        return Cells.from_density(1.0)

    @staticmethod
    def from_density(density: float) -> 'Cells':
        return Cells(density=density)

    @staticmethod
    def from_targets(targets: list[str], density: float = 1.0) -> 'Cells':
        return Cells(density=density, targets=targets)

    @staticmethod
    def from_gids(gids: list[int]) -> 'Cells':
        return Cells(gids=gids)
