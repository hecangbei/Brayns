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
    'async': True,
    'description': 'Add model from path and return model descriptor on success',
    'params': [
        {
            'additionalProperties': False,
            'properties': {
                'bounding_box': {
                    'description': 'Display bounding box',
                    'type': 'boolean'
                },
                'loader_name': {
                    'description': 'Name of the loader',
                    'type': 'string'
                },
                'loader_properties': {
                    'description': 'Loader properties',
                    'type': 'object'
                },
                'name': {
                    'description': 'Model name',
                    'type': 'string'
                },
                'path': {
                    'description': 'Model file path',
                    'type': 'string'
                },
                'transformation': {
                    'additionalProperties': False,
                    'description': 'Model transformation',
                    'properties': {
                        'rotation': {
                            'description': 'Rotation XYZW',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 4,
                            'minItems': 4,
                            'type': 'array'
                        },
                        'rotation_center': {
                            'description': 'Rotation center XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'scale': {
                            'description': 'Scale XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'translation': {
                            'description': 'Translation XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        }
                    },
                    'title': 'Transformation',
                    'type': 'object'
                },
                'visible': {
                    'description': 'Is visible',
                    'type': 'boolean'
                }
            },
            'title': 'ModelParams',
            'type': 'object'
        }
    ],
    'plugin': 'Core',
    'returns': {
        'items': {
            'additionalProperties': False,
            'properties': {
                'bounding_box': {
                    'description': 'Display bounding box',
                    'type': 'boolean'
                },
                'bounds': {
                    'additionalProperties': False,
                    'description': 'Model bounds',
                    'properties': {
                        'max': {
                            'description': 'Top-right XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'min': {
                            'description': 'Bottom-left XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        }
                    },
                    'readOnly': True,
                    'title': 'Boxd',
                    'type': 'object'
                },
                'id': {
                    'description': 'Model ID',
                    'minimum': 0,
                    'type': 'integer'
                },
                'loader_name': {
                    'description': 'Name of the loader',
                    'type': 'string'
                },
                'loader_properties': {
                    'description': 'Loader properties',
                    'type': 'object'
                },
                'metadata': {
                    'additionalProperties': {
                        'type': 'string'
                    },
                    'description': 'Key-value data',
                    'type': 'object'
                },
                'name': {
                    'description': 'Model name',
                    'type': 'string'
                },
                'path': {
                    'description': 'Model file path',
                    'type': 'string'
                },
                'transformation': {
                    'additionalProperties': False,
                    'description': 'Model transformation',
                    'properties': {
                        'rotation': {
                            'description': 'Rotation XYZW',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 4,
                            'minItems': 4,
                            'type': 'array'
                        },
                        'rotation_center': {
                            'description': 'Rotation center XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'scale': {
                            'description': 'Scale XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        },
                        'translation': {
                            'description': 'Translation XYZ',
                            'items': {
                                'type': 'number'
                            },
                            'maxItems': 3,
                            'minItems': 3,
                            'type': 'array'
                        }
                    },
                    'title': 'Transformation',
                    'type': 'object'
                },
                'visible': {
                    'description': 'Is visible',
                    'type': 'boolean'
                }
            },
            'title': 'ModelDescriptor',
            'type': 'object'
        },
        'type': 'array'
    },
    'title': 'add-model',
    'type': 'method'
}

params = {
    'name': 'My Mesh',
    'path': '/home/acfleury/Test/circuit5000_99983_decimated.off',
    'loader_name': 'mesh',
    'loader_properties': {
        'geometryQuality': 1
    }
}

result = {
    'check': 0.5825772088075298
}
