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

from brayns.core.common.resolution import Resolution
from brayns.core.parameters.application_parameters import ApplicationParameters
from tests.core.parameters.mock_parameters_instance import MockParametersInstance


class TestApplicationParameters(unittest.TestCase):

    def test_from_instance(self) -> None:
        instance = MockParametersInstance()
        test = ApplicationParameters.from_instance(instance)
        ref = ApplicationParameters.deserialize(instance.application)
        self.assertEqual(test, ref)
        self.assertEqual(instance.method, 'get-application-parameters')
        self.assertEqual(instance.params, None)

    def test_deserialize(self) -> None:
        message = {
            'plugins': ['test1', 'test2'],
            'viewport': [1920, 1080]
        }
        test = ApplicationParameters.deserialize(message)
        ref = ApplicationParameters(
            plugins=['test1', 'test2'],
            resolution=Resolution(1920, 1080)
        )
        self.assertEqual(test, ref)

    def test_update(self) -> None:
        instance = MockParametersInstance()
        ApplicationParameters.update(instance, Resolution(100, 200))
        self.assertEqual(instance.method, 'set-application-parameters')
        self.assertEqual(instance.params, {
            'viewport': [100, 200]
        })


if __name__ == '__main__':
    unittest.main()
