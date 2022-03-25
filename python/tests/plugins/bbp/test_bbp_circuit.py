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

from brayns.instance.scene.model_registry import ModelRegistry
from brayns.plugins.bbp.bbp_cells import BbpCells
from brayns.plugins.bbp.bbp_circuit import BbpCircuit
from brayns.plugins.bbp.bbp_report import BbpReport
from brayns.plugins.common.neuron_morphology import NeuronMorphology
from brayns.plugins.common.neuron_radius import NeuronRadius
from instance.scene.mock_scene_client import MockSceneClient


class TestBbpCircuit(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockSceneClient()
        self._models = ModelRegistry(self._client)
        self._circuit = BbpCircuit(
            path='path',
            cells=BbpCells.all(),
            report=BbpReport.compartment('test'),
            morphology=NeuronMorphology(
                radius=NeuronRadius.override(3.0),
                load_soma=True,
                load_axon=True,
                load_dendrites=True
            ),
            load_afferent_synapses=True,
            load_efferent_synapses=True
        )

    def test_get_path(self) -> None:
        self.assertEqual(self._circuit.get_path(), self._circuit.path)

    def test_get_loader(self) -> None:
        self.assertEqual(self._circuit.get_loader(), 'BBP loader')

    def test_get_loader_properties(self) -> None:
        circuit = self._circuit
        properties = circuit.get_loader_properties()
        self.assertEqual(properties['percentage'], circuit.cells.density)
        self.assertEqual(properties['targets'], circuit.cells.targets)
        self.assertEqual(properties['gids'], circuit.cells.gids)
        self.assertEqual(properties['report_type'], circuit.report.type)
        self.assertEqual(properties['report_name'], circuit.report.name)
        self.assertEqual(
            properties['spike_transition_time'],
            circuit.report.spike_transition_time
        )
        self.assertEqual(
            properties['load_afferent_synapses'],
            circuit.load_afferent_synapses
        )
        self.assertEqual(
            properties['load_efferent_synapses'],
            circuit.load_efferent_synapses
        )
        self.assertEqual(
            properties['neuron_morphology_parameters'],
            circuit.morphology.to_dict()
        )

    def test_add(self) -> None:
        circuit = self._circuit
        self._models.add(circuit)
        params = self._client.get_received_params()[-1]
        self.assertEqual(params['path'], circuit.path)
        self.assertEqual(params['loader_name'], circuit.get_loader())
        self.assertEqual(
            params['loader_properties'],
            circuit.get_loader_properties()
        )


if __name__ == '__main__':
    unittest.main()
