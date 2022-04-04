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
from brayns.client.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.client.jsonrpc.json_rpc_request import JsonRpcRequest
from brayns.client.request_future import RequestFuture


class Client(ClientProtocol):

    def __init__(self, client: JsonRpcClient) -> None:
        self._client = client

    def __enter__(self) -> 'Client':
        return self

    def __exit__(self, *_) -> None:
        self.disconnect()

    def disconnect(self) -> None:
        self._client.disconnect()

    def request(self, method: str, params: Any = None) -> Any:
        return self.task(method, params).wait_for_result()

    def task(self, method: str, params: Any = None) -> RequestFuture:
        id = 0
        while id in self._client.get_active_tasks():
            id += 1
        return RequestFuture(
            cancel=lambda: self.request('cancel', {'id': id}),
            poll=self._client.poll,
            task=self._client.send(JsonRpcRequest(id, method, params))
        )
