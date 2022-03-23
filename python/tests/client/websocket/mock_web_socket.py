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
        self.closed = False
        self.received = []
        self.replies = []

    def has_received(self, requests: list[JsonRpcRequest]) -> bool:
        expected = [request.to_dict() for request in requests]
        received = [json.loads(message) for message in self.received]
        return received == expected

    def got_request(self, method: str, params: Any) -> bool:
        message = json.loads(self.received[-1])
        return message['method'] == method and message['params'] == params

    def reply(self, reply: JsonRpcReply) -> None:
        self.replies.append(json.dumps({
            'id': reply.id,
            'result': reply.result
        }))

    def progress(self, progress: JsonRpcProgress) -> None:
        self.replies.append(json.dumps({
            'params': {
                'id': progress.id,
                'operation': progress.params.operation,
                'amount': progress.params.amount
            }
        }))

    def error(self, error: JsonRpcError) -> None:
        self.replies.append(json.dumps({
            'id': error.id,
            'error': {
                'code': error.error.code,
                'message': error.error.message,
                'data': error.error.data
            }
        }))

    def close(self) -> None:
        self.closed = True

    def receive(self) -> Union[bytes, str]:
        return self.replies.pop(0)

    def send(self, data: Union[bytes, str]) -> None:
        self.received.append(data)
