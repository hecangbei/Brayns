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

from brayns.core.version.version import Version
from tests.core.version.mock_version_instance import MockVersionInstance


class TestVersion(unittest.TestCase):

    def test_of(self) -> None:
        instance = MockVersionInstance()
        test = Version.of(instance)
        ref = Version.deserialize(instance.version)
        self.assertEqual(test, ref)

    def test_deserialize(self) -> None:
        message = {
            'major': 0,
            'minor': 1,
            'patch': 2,
            'revision': '3'
        }
        test = Version.deserialize(message)
        ref = Version(
            major=0,
            minor=1,
            patch=2,
            revision='3'
        )
        self.assertEqual(test, ref)

    def test_release(self) -> None:
        test = Version(
            major=0,
            minor=1,
            patch=2,
            revision='3'
        ).release
        ref = (0, 1, 2)
        self.assertEqual(test, ref)


if __name__ == '__main__':
    unittest.main()
