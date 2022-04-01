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

import unittest

from brayns.scene.scene import Scene
from brayns.plugins.bbp.bbp_cells import BbpCells
from brayns.plugins.bbp.bbp_circuit import BbpCircuit
from brayns.plugins.bbp.bbp_report import BbpReport
from brayns.plugins.common.neuron_radius import NeuronRadius
from tests.scene.mock_scene_client import MockSceneClient


class TestBbpCircuit(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._scene = Scene(self._client)
        self._circuit = BbpCircuit(
            path='path',
            cells=BbpCells.all(),
            report=BbpReport.compartment('test'),
            radius=NeuronRadius.override(3.0),
            load_soma=True,
            load_axon=True,
            load_dendrites=True,
            load_afferent_synapses=True,
            load_efferent_synapses=True
        )

    def test_get_path(self) -> None:
        self.assertEqual(self._circuit.get_path(), self._circuit.path)

    def test_get_loader(self) -> None:
        self.assertEqual(self._circuit.get_loader(), 'BBP loader')

    def test_get_loader_properties(self) -> None:
        ref = {
            'percentage': 1.0,
            'targets': [],
            'gids': [],
            'report_type': 'compartment',
            'report_name': 'test',
            'spike_transition_time': 1.0,
            'load_afferent_synapses': True,
            'load_efferent_synapses': True,
            'neuron_morphology_parameters': {
                'radius_multiplier': 1.0,
                'radius_override': 3.0,
                'load_soma': True,
                'load_axon': True,
                'load_dendrites': True
            }
        }
        self.assertEqual(self._circuit.get_loader_properties(), ref)


if __name__ == '__main__':
    unittest.main()
