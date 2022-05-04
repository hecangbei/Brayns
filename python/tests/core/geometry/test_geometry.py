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

from brayns.core.common.bounds import Bounds
from brayns.core.common.capsule import Capsule
from brayns.core.common.color import Color
from brayns.core.common.plane import Plane
from brayns.core.common.sphere import Sphere
from brayns.core.common.vector3 import Vector3
from brayns.core.geometry.geometry import Geometry
from tests.core.geometry.mock_geometry_instance import MockGeometryInstance


class TestGeometry(unittest.TestCase):

    def test_add_boxes(self) -> None:
        instance = MockGeometryInstance()
        boxes = [
            (Bounds.cube(2), Color.pure_red),
            (Bounds.cube(4, Vector3.one), Color.pure_blue)
        ]
        model = Geometry.add_boxes(instance, boxes)
        self.assertEqual(model.id, instance.model['id'])
        self.assertEqual(instance.method, 'add-boxes')
        self.assertEqual(instance.params, [
            {
                'geometry': {
                    'min': [-1, -1, -1],
                    'max': [1, 1, 1]
                },
                'color': [1, 0, 0, 1]
            },
            {
                'geometry': {
                    'min': [-1, -1, -1],
                    'max': [3, 3, 3]
                },
                'color': [0, 0, 1, 1]
            }
        ])

    def test_add_capsules(self) -> None:
        instance = MockGeometryInstance()
        capsules = [
            (Capsule(Vector3.zero, 1, Vector3.one, 2), Color.pure_red),
            (Capsule(Vector3.one, 2, 2 * Vector3.one, 3), Color.pure_blue)
        ]
        model = Geometry.add_capsules(instance, capsules)
        self.assertEqual(model.id, instance.model['id'])
        self.assertEqual(instance.method, 'add-capsules')
        self.assertEqual(instance.params, [
            {
                'geometry': {
                    'p0': [0, 0, 0],
                    'r0': 1,
                    'p1': [1, 1, 1],
                    'p1': 2
                },
                'color': [1, 0, 0, 1]
            },
            {
                'geometry': {
                    'p0': [1, 1, 1],
                    'r0': 2,
                    'p1': [2, 2, 2],
                    'p1': 3
                },
                'color': [0, 0, 1, 1]
            }
        ])

    def test_add_planes(self) -> None:
        instance = MockGeometryInstance()
        planes = [
            (Plane(Vector3.one), Color.pure_red),
            (Plane(3 * Vector3.one, 3), Color.pure_blue)
        ]
        model = Geometry.add_planes(instance, planes)
        self.assertEqual(model.id, instance.model['id'])
        self.assertEqual(instance.method, 'add-planes')
        self.assertEqual(instance.params, [
            {
                'geometry': {
                    'coefficients': [1, 1, 1, 0]
                },
                'color': [1, 0, 0, 1]
            },
            {
                'geometry': {
                    'coefficients': [3, 3, 3, 3]
                },
                'color': [0, 0, 1, 1]
            }
        ])

    def test_add_spheres(self) -> None:
        instance = MockGeometryInstance()
        spheres = [
            (Sphere(1), Color.pure_red),
            (Sphere(2, Vector3.one), Color.pure_blue)
        ]
        model = Geometry.add_spheres(instance, spheres)
        self.assertEqual(model.id, instance.model['id'])
        self.assertEqual(instance.method, 'add-spheres')
        self.assertEqual(instance.params, [
            {
                'geometry': {
                    'center': [0, 0, 0],
                    'radius': 1
                },
                'color': [1, 0, 0, 1]
            },
            {
                'geometry': {
                    'center': [1, 1, 1],
                    'radius': 2
                },
                'color': [0, 0, 1, 1]
            }
        ])


if __name__ == '__main__':
    unittest.main()
