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

from brayns.core.scene.model import Model
from brayns.core.scene.model_loader import ModelLoader
from brayns.instance.instance_protocol import InstanceProtocol
from brayns.plugins.circuit.cells import Cells
from brayns.plugins.circuit.report import Report


@dataclass
class CircuitLoader:

    cells: Cells = Cells.all()
    report: Report = Report.none()
    radius_multiplier: float = 1.0
    load_soma: bool = True
    load_axon: bool = False
    load_dendrites: bool = False
    load_afferent_synapses: bool = False
    load_efferent_synapses: bool = False

    def load_circuit(self, instance: InstanceProtocol, path: str) -> list[Model]:
        loader = ModelLoader(
            properties={
                'percentage': self.cells.density,
                'targets': self.cells.targets,
                'gids': self.cells.gids,
                'report_type': self.report.type,
                'report_name': self.report.name,
                'spike_transition_time': self.report.spike_transition_time,
                'neuron_morphology_parameters': {
                    'radius_multiplier': self.radius_multiplier,
                    'load_soma': self.load_soma,
                    'load_axon': self.load_axon,
                    'load_dendrites': self.load_dendrites
                },
                'load_afferent_synapses': self.load_afferent_synapses,
                'load_efferent_synapses': self.load_efferent_synapses
            }
        )
        return loader.add_model(instance, path)
