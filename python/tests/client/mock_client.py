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

from typing import Any

from brayns.client.client_protocol import ClientProtocol
from brayns.client.jsonrpc.json_rpc_task import JsonRpcTask
from brayns.client.request_future import RequestFuture


class MockClient(ClientProtocol):

    def __init__(self) -> None:
        self.disconnected = False
        self.received = []
        self.results = []

    def has_received(self, method: str, params: Any) -> bool:
        return self.received[-1] == (method, params)

    def get_last_result(self) -> Any:
        return self.received[-1][1]

    def disconnect(self) -> None:
        self.disconnected = True

    def request(self, method: str, params: Any = None) -> Any:
        self.received.append((method, params))
        return self.results.pop(0)

    def task(self, method: str, params: Any = None) -> RequestFuture:
        self.received.append((method, params))
        return RequestFuture(
            cancel=lambda: None,
            poll=lambda: None,
            task=JsonRpcTask.from_result(self.results.pop(0))
        )
