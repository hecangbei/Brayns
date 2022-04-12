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

from brayns.plugins.circuit.circuit_info import CircuitInfo


class CircuitInfoSerializer:

    def serialize(self, circuit: CircuitInfo) -> dict:
        return {
            'percentage': circuit.cells.density,
            'targets': circuit.cells.targets,
            'gids': circuit.cells.gids,
            'report_type': circuit.report.type,
            'report_name': circuit.report.name,
            'spike_transition_time': circuit.report.spike_transition_time,
            'neuron_morphology_parameters': {
                'radius_multiplier': circuit.radius.multiplier,
                'radius_override': circuit.radius.value,
                'load_soma': circuit.load_soma,
                'load_axon': circuit.load_axon,
                'load_dendrites': circuit.load_dendrites
            },
            'load_afferent_synapses': circuit.load_afferent_synapses,
            'load_efferent_synapses': circuit.load_efferent_synapses
        }
