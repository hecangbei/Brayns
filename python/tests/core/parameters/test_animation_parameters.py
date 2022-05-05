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
from brayns.core.parameters.time_unit import TimeUnit
from tests.core.parameters.mock_parameters_instance import MockParametersInstance


class TestAnimationParameters(unittest.TestCase):

    def test_from_instance(self) -> None:
        instance = MockParametersInstance()
        test = AnimationParameters.from_instance(instance)
        ref = AnimationParameters.deserialize(instance.animation)
        self.assertEqual(test, ref)
        self.assertEqual(instance.method, 'get-animation-parameters')
        self.assertEqual(instance.params, None)

    def test_deserialize(self) -> None:
        message = {
            'start_frame': 0,
            'end_frame': 10,
            'current': 5,
            'dt': 0.1,
            'unit': 'ms'
        }
        test = AnimationParameters.deserialize(message)
        ref = AnimationParameters(
            start_frame=0,
            end_frame=10,
            current_frame=5,
            delta_time=0.1,
            time_unit=TimeUnit.MILLISECOND
        )
        self.assertEqual(test, ref)

    def test_update(self) -> None:
        instance = MockParametersInstance()
        AnimationParameters.update(
            instance,
            start_frame=0,
            end_frame=10,
            current_frame=5
        )
        self.assertEqual(instance.method, 'set-animation-parameters')
        self.assertEqual(instance.params, {
            'start_frame': 0,
            'end_frame': 10,
            'current': 5
        })


if __name__ == '__main__':
    unittest.main()
