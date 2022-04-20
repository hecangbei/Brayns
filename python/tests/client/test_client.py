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

import logging
import unittest

from brayns.instance.instance import Instance
from brayns.instance.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.instance.jsonrpc.json_rpc_error import JsonRpcError
from brayns.instance.jsonrpc.json_rpc_progress import JsonRpcProgress
from brayns.instance.jsonrpc.json_rpc_reply import JsonRpcReply
from brayns.instance.jsonrpc.json_rpc_request import JsonRpcRequest
from brayns.instance.request_error import RequestError
from brayns.instance.request_progress import RequestProgress
from tests.client.websocket.mock_web_socket import MockWebSocket


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        self._websocket = MockWebSocket()

    def test_context(self) -> None:
        with self._connect():
            pass
        self.assertTrue(self._websocket.closed)

    def test_disconnect(self) -> None:
        client = self._connect()
        client.disconnect()
        self.assertTrue(self._websocket.closed)

    def test_request(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        reply = JsonRpcReply(0, 456)
        with self._connect() as client:
            self._websocket.reply(reply)
            result = client.request(request.method, request.params)
            self.assertEqual(self._websocket.requests[-1], request)
            self.assertEqual(result, reply.result)
            self.assertFalse(self._websocket.closed)

    def test_request_error(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        error = JsonRpcError(0, RequestError('test', 0, 456))
        with self._connect() as client:
            self._websocket.error(error)
            with self.assertRaises(RequestError) as context:
                client.request(request.method, request.params)
            self.assertEqual(context.exception, error.error)
            self.assertFalse(self._websocket.closed)

    def test_task(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        reply = JsonRpcReply(0, 456)
        with self._connect() as client:
            task = client.task(request.method, request.params)
            self.assertEqual(self._websocket.requests[-1], request)
            self._websocket.reply(reply)
            self.assertEqual(task.wait_for_result(), reply.result)

    def test_task_progress(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        reply = JsonRpcReply(0, 456)
        progresses = [
            JsonRpcProgress(0, RequestProgress('operation', 0.1 * i))
            for i in range(10)
        ]
        with self._connect() as client:
            task = client.task(request.method, request.params)
            for progress in progresses:
                self._websocket.progress(progress)
            self._websocket.reply(reply)
            self.assertEqual(
                [JsonRpcProgress(0, progress) for progress in task],
                progresses
            )
            self.assertEqual(task.wait_for_result(), reply.result)

    def test_task_cancel(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        cancel = JsonRpcRequest(1, 'cancel', {'id': 0})
        error = JsonRpcError(0, RequestError('Task cancelled'))
        reply = JsonRpcReply(1, None)
        with self._connect() as client:
            task = client.task(request.method, request.params)
            self._websocket.reply(reply)
            task.cancel()
            self.assertEqual(self._websocket.requests[-1], cancel)
            self._websocket.error(error)
            with self.assertRaises(RequestError) as context:
                task.wait_for_result()
            self.assertEqual(context.exception, error.error)

    def _connect(self) -> Instance:
        return Instance(
            JsonRpcClient(
                websocket=self._websocket,
                logger=logging.Logger('Test')
            )
        )


if __name__ == '__main__':
    unittest.main()
