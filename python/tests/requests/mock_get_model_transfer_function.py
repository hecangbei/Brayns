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
    'description': 'Get the transfer function of the given model',
    'params': [
        {
            'additionalProperties': False,
            'properties': {
                'id': {
                    'description': 'Model ID',
                    'minimum': 0,
                    'type': 'integer'
                }
            },
            'required': [
                'id'
            ],
            'title': 'GetModelMessage',
            'type': 'object'
        }
    ],
    'plugin': 'Core',
    'returns': {
        'additionalProperties': False,
        'properties': {
            'colormap': {
                'additionalProperties': False,
                'description': 'Colors to map',
                'properties': {
                    'colors': {
                        'description': 'Colors to map',
                        'items': {
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'type': 'array'
                    },
                    'name': {
                        'description': 'Label of the color map',
                        'type': 'string'
                    }
                },
                'required': [
                    'colors'
                ],
                'title': 'ColorMap',
                'type': 'object'
            },
            'opacity_curve': {
                'description': 'Control points',
                'items': {
                    'items': {
                        'type': 'number'
                    },
                    'maxItems': 2,
                    'minItems': 2,
                    'type': 'array'
                },
                'type': 'array'
            },
            'range': {
                'description': 'Values range',
                'items': {
                    'type': 'number'
                },
                'maxItems': 2,
                'minItems': 2,
                'type': 'array'
            }
        },
        'title': 'TransferFunction',
        'type': 'object'
    },
    'title': 'get-model-transfer-function',
    'type': 'method'
}

params = {
    'id': 0
}

result = {
    'check': 0.5949909700244684
}
