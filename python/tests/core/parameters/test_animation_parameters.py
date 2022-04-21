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

from brayns.core.parameters.animation_parameters import AnimationParameters
from tests.core.parameters.mock_parameters_instance import MockParametersInstance


class TestAnimationParameters(unittest.TestCase):

    def setUp(self) -> None:
        self._instance = MockParametersInstance()

    def test_from_instance(self) -> None:
        test = AnimationParameters.from_instance(self._instance)
        self.assertEqual(self._instance.method, 'get-animation-parameters')
        self.assertEqual(self._instance.params, None)
        ref = self._instance.animation
        self.assertEqual(test, AnimationParameters.deserialize(ref))

    def test_deserialize(self) -> None:
        test = {
            'start_frame': 0,
            'end_frame': 10,
            'current': 5,
            'dt': 1,
            'unit': 'ms'
        }
        ref = AnimationParameters(0, 10, 5, 1)
        test = AnimationParameters.deserialize(ref)
        self.assertEqual(test, ref)

    def test_update(self) -> None:
        test = AnimationParameters()
        test.update(self._instance)
        self.assertEqual(self._instance.method, 'set-animation-parameters')
        self.assertEqual(self._instance.params, test.serialize())

    def test_serialize(self) -> None:
        test = AnimationParameters(0, 10, 5)
        ref = {
            'start_frame': 0,
            'end_frame': 10,
            'current': 5
        }
        self.assertEqual(test.serialize(), ref)

    def test_clamp(self) -> None:
        test = AnimationParameters(2, 10)
        self.assertEqual(test.clamp(3), 3)
        self.assertEqual(test.clamp(1), 2)
        self.assertEqual(test.clamp(11), 10)

    def test_get_timestamp(self) -> None:
        test = AnimationParameters(1, 10, delta_time=0.1)
        self.assertAlmostEqual(test.get_timestamp(3), 0.2)
        self.assertAlmostEqual(test.get_timestamp(1), 0)
        self.assertAlmostEqual(test.get_timestamp(10), 0.9)

    def test_get_frame(self) -> None:
        test = AnimationParameters(1, 10, delta_time=0.1)
        self.assertEqual(test.get_frame(0.2), 3)
        self.assertEqual(test.get_frame(0), 1)
        self.assertEqual(test.get_frame(0.9), 10)

    def test_get_frames(self) -> None:
        test = AnimationParameters(1, 10, delta_time=0.1)
        frames = test.get_frames(0.5)
        self.assertEqual(frames, [1, 2, 3, 4, 5, 6])
        frames = test.get_frames(0.5, 0.2)
        self.assertEqual(frames, [1, 3, 5])


if __name__ == '__main__':
    unittest.main()
