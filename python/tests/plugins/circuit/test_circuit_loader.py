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

from brayns.plugins.circuit.cells import Cells
from brayns.plugins.circuit.circuit_loader import CircuitLoader
from brayns.plugins.circuit.report import Report
from tests.core.scene.mock_scene_instance import MockSceneInstance


class TestCircuit(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockSceneInstance()
        self._loader = CircuitLoader(
            cells=Cells.all(),
            report=Report.compartment('test'),
            radius_multiplier=3,
            load_soma=True,
            load_axon=True,
            load_dendrites=True,
            load_afferent_synapses=True,
            load_efferent_synapses=True
        )
        self._properties = {
            'percentage': 1.0,
            'targets': [],
            'gids': [],
            'report_type': 'compartment',
            'report_name': 'test',
            'spike_transition_time': 1.0,
            'load_afferent_synapses': True,
            'load_efferent_synapses': True,
            'neuron_morphology_parameters': {
                'radius_multiplier': 3.0,
                'load_soma': True,
                'load_axon': True,
                'load_dendrites': True
            }
        }

    def test_for_soma_only(self) -> None:
        loader = CircuitLoader.for_soma_only()
        self.assertEqual(loader.cells.density, 0.1)
        self.assertEqual(loader.radius_multiplier, 10.0)
        self.assertTrue(loader.load_soma)

    def test_for_morphology(self) -> None:
        loader = CircuitLoader.for_morphology()
        self.assertEqual(loader.cells.density, 0.001)
        self.assertEqual(loader.radius_multiplier, 1.0)
        self.assertTrue(loader.load_soma)
        self.assertTrue(loader.load_dendrites)

    def test_load_circuit(self) -> None:
        self._loader.load_circuit(self._instance, 'path')
        test = self._instance.params
        self.assertEqual(test['path'], 'path')
        self.assertEqual(test['loader'], '')
        self.assertEqual(test['loader_properties'], self._properties)


if __name__ == '__main__':
    unittest.main()
