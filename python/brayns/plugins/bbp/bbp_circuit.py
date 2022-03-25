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

from brayns.instance.scene.model_protocol import ModelProtocol
from brayns.plugins.bbp.bbp_cells import BbpCells
from brayns.plugins.bbp.bbp_report import BbpReport
from brayns.plugins.common.neuron_morphology import NeuronMorphology


@dataclass
class BbpCircuit(ModelProtocol):

    path: str
    cells: BbpCells = BbpCells.all()
    report: BbpReport = BbpReport.none()
    morphology: NeuronMorphology = NeuronMorphology()
    load_afferent_synapses: bool = False
    load_efferent_synapses: bool = False

    def get_path(self) -> str:
        return self.path

    def get_loader(self) -> str:
        return 'BBP loader'

    def get_loader_properties(self) -> dict:
        return {
            'percentage': self.cells.density,
            'targets': self.cells.targets,
            'gids': self.cells.gids,
            'report_type': self.report.type,
            'report_name': self.report.name,
            'spike_transition_time': self.report.spike_transition_time,
            'load_afferent_synapses': self.load_afferent_synapses,
            'load_efferent_synapses': self.load_efferent_synapses,
            'neuron_morphology_parameters': self.morphology.to_dict()
        }
