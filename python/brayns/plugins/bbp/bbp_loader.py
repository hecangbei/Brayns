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

from dataclasses import dataclass
from typing import Optional

from brayns.core.model.model import Model
from brayns.core.model.model_loader import ModelLoader
from brayns.instance.instance import Instance
from brayns.plugins.bbp.bbp_cells import BbpCells
from brayns.plugins.bbp.bbp_report import BbpReport


@dataclass
class BbpLoader:

    cells: BbpCells = BbpCells.all()
    report: Optional[BbpReport] = None
    radius_multiplier: float = 1.0
    load_soma: bool = True
    load_axon: bool = False
    load_dendrites: bool = False
    load_afferent_synapses: bool = False
    load_efferent_synapses: bool = False

    @staticmethod
    def for_soma_only() -> 'BbpLoader':
        return BbpLoader(
            cells=BbpCells.from_density(0.1),
            radius_multiplier=10.0
        )

    @staticmethod
    def for_morphology() -> 'BbpLoader':
        return BbpLoader(
            cells=BbpCells.from_density(0.001),
            load_dendrites=True
        )

    def load_circuit(self, instance: Instance, path: str) -> list[Model]:
        properties = self._get_properties()
        loader = ModelLoader('BBP loader', properties)
        return loader.add_model(instance, path)

    def _get_properties(self) -> dict:
        params = {
            'percentage': self.cells.density,
            'neuron_morphology_parameters': {
                'radius_multiplier': self.radius_multiplier,
                'load_soma': self.load_soma,
                'load_axon': self.load_axon,
                'load_dendrites': self.load_dendrites
            },
            'load_afferent_synapses': self.load_afferent_synapses,
            'load_efferent_synapses': self.load_efferent_synapses
        }
        if self.cells.gids is not None:
            params['gids'] = self.cells.gids
        if self.cells.targets is not None:
            params['targets'] = self.cells.targets
        if self.report is not None:
            params['report_type'] = self.report.type
            if self.report.name is not None:
                params['report_name'] = self.report.name
            if self.report.spike_transition_time is not None:
                params['spike_transition_time'] = self.report.spike_transition_time
        return params
