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

from brayns.camera.projection_registry import ProjectionRegistry
from tests.camera.mock_camera_client import MockCameraClient
from tests.camera.mock_camera_projection import MockCameraProjection


class TestProjectionRegistry(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MockCameraClient()
        self._projections = ProjectionRegistry(self._client)
        self._projections.add_projection_type(MockCameraProjection)

    def test_contains(self) -> None:
        self.assertIn(MockCameraProjection.get_name(), self._projections)

    def test_len(self) -> None:
        self.assertEqual(len(self._projections), 1)

    def test_iter(self) -> None:
        names = [MockCameraProjection.get_name()]
        self.assertEqual(list(self._projections), names)

    def test_add_projection_type(self) -> None:
        with self.assertRaises(RuntimeError):
            self._projections.add_projection_type(MockCameraProjection)

    def test_get_current_projection_name(self) -> None:
        ref = MockCameraProjection.get_name()
        self._client.name = ref
        current = self._projections.get_current_projection_name()
        self.assertEqual(current, ref)

    def test_get_current_projection(self) -> None:
        ref = MockCameraProjection(2, 3)
        self._client.name = ref.get_name()
        self._client.projection = ref.to_dict()
        projection = self._projections.get_current_projection()
        self.assertEqual(projection.to_dict(), ref.to_dict())

    def test_set_current_projection(self) -> None:
        ref = MockCameraProjection(2, 3)
        self._projections.set_current_projection(ref)
        self.assertEqual(self._client.name, ref.get_name())
        self.assertEqual(self._client.projection, ref.to_dict())


if __name__ == '__main__':
    unittest.main()
