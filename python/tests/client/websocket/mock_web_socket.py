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

import json
from typing import Any, Union

from brayns.client.jsonrpc.json_rpc_error import JsonRpcError
from brayns.client.jsonrpc.json_rpc_progress import JsonRpcProgress
from brayns.client.jsonrpc.json_rpc_reply import JsonRpcReply
from brayns.client.jsonrpc.json_rpc_request import JsonRpcRequest
from brayns.client.websocket.web_socket_protocol import WebSocketProtocol


class MockWebSocket(WebSocketProtocol):

    def __init__(self) -> None:
        self._closed = False
        self._requests = []
        self._replies = []

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def requests(self) -> list[JsonRpcRequest]:
        return self._requests

    def reply(self, reply: JsonRpcReply) -> None:
        self._replies.append(json.dumps({
            'id': reply.id,
            'result': reply.result
        }))

    def progress(self, progress: JsonRpcProgress) -> None:
        self._replies.append(json.dumps({
            'params': {
                'id': progress.id,
                'operation': progress.params.operation,
                'amount': progress.params.amount
            }
        }))

    def error(self, error: JsonRpcError) -> None:
        self._replies.append(json.dumps({
            'id': error.id,
            'error': {
                'code': error.error.code,
                'message': error.error.message,
                'data': error.error.data
            }
        }))

    def close(self) -> None:
        self._closed = True

    def receive(self) -> Union[bytes, str]:
        return self._replies.pop(0)

    def send(self, data: Union[bytes, str]) -> None:
        message: dict = json.loads(data)
        self._requests.append(JsonRpcRequest(
            id=message.get('id'),
            method=message['method'],
            params=message.get('params')
        ))
