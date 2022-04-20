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

import base64
from typing import Iterator, Optional

from brayns.instance.request_future import RequestFuture
from brayns.instance.request_progress import RequestProgress


class SnapshotTask:

    def __init__(self, task: RequestFuture, path: Optional[str] = None, remote: bool = False) -> None:
        self._task = task
        self._path = path
        self._remote = remote

    def __iter__(self) -> Iterator[RequestProgress]:
        yield from self._task

    def cancel(self) -> None:
        self._task.cancel()

    def wait_for_download(self) -> bytes:
        if self._path is not None:
            raise RuntimeError('Snapshot is not a download')
        result = self._task.wait_for_result()
        return self._decode(result)

    def wait_for_save(self) -> None:
        if self._path is None:
            raise RuntimeError('Snapshot is a download')
        result = self._task.wait_for_result()
        if self._remote:
            return
        data = self._decode(result)
        with open(self._path, 'wb') as file:
            file.write(data)

    def _decode(self, result: dict) -> bytes:
        return base64.b64decode(result['data'])
