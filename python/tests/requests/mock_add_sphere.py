# Copyright (c) 2015-2021 EPFL/Blue Brain Project
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

schema = {
    'async': False,
    'description': 'Add a visual 3D sphere to the scene',
    'params': [
        {
            'additionalProperties': False,
            'properties': {
                'center': {
                    'description': 'Sphere center XYZ',
                    'items': {
                        'type': 'number'
                    },
                    'maxItems': 3,
                    'minItems': 3,
                    'type': 'array'
                },
                'color': {
                    'description': 'Sphere color RGBA normalized',
                    'items': {
                        'type': 'number'
                    },
                    'maxItems': 4,
                    'minItems': 4,
                    'type': 'array'
                },
                'name': {
                    'description': 'Name of the sphere model',
                    'type': 'string'
                },
                'radius': {
                    'description': 'Radius of the sphere',
                    'minimum': 0,
                    'type': 'number'
                }
            },
            'required': [
                'center',
                'radius',
                'color'
            ],
            'title': 'AddSphereMessage',
            'type': 'object'
        }
    ],
    'plugin': 'Circuit Explorer',
    'returns': {
        'additionalProperties': False,
        'properties': {
            'id': {
                'description': 'ID of the model of the shape added',
                'minimum': 0,
                'type': 'integer'
            }
        },
        'required': [
            'id'
        ],
        'title': 'AddShapeMessage',
        'type': 'object'
    },
    'title': 'add-sphere',
    'type': 'method'
}

params = {
    'center': [
        0,
        0,
        0
    ],
    'radius': 0.1,
    'color': [
        1,
        0,
        0,
        1
    ],
    'name': 'test'
}

result = {
    'check': 0.35432092298554063
}
