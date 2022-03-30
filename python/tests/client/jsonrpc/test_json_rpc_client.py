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

from brayns.client.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.client.jsonrpc.json_rpc_reply import JsonRpcReply
from brayns.client.jsonrpc.json_rpc_request import JsonRpcRequest
from tests.client.websocket.mock_web_socket import MockWebSocket


class TestJsonRpcClient(unittest.TestCase):

    def setUp(self) -> None:
        self._logger = logging.Logger('Test')
        self._websocket = MockWebSocket()

    def test_context(self) -> None:
        with self._connect():
            pass
        self.assertTrue(self._websocket.closed)

    def test_disconnect(self) -> None:
        client = self._connect()
        client.disconnect()
        self.assertTrue(self._websocket.closed)

    def test_send(self) -> None:
        requests = [
            JsonRpcRequest(0, 'test', 123),
            JsonRpcRequest('0', 'test', 123),
            JsonRpcRequest(None, 'test', 123)
        ]
        with self._connect() as client:
            for request in requests:
                client.send(request)
            self.assertEqual(self._websocket.requests, requests)

    def test_poll(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        reply = JsonRpcReply(0, 456)
        with self._connect() as client:
            task = client.send(request)
            self._websocket.reply(reply)
            self.assertFalse(task.is_ready())
            client.poll()
            self.assertEqual(task.get_result(), reply.result)

    def test_poll_notification(self) -> None:
        request = JsonRpcRequest(None, 'test', 123)
        with self._connect() as client:
            task = client.send(request)
            self.assertEqual(task.get_result(), None)

    def test_active_tasks(self) -> None:
        requests = [
            JsonRpcRequest(0, 'test1', 123),
            JsonRpcRequest(1, 'test2', 456),
            JsonRpcRequest(2, 'test3', 789)
        ]
        with self._connect() as client:
            for request in requests:
                client.send(request)
            self.assertEqual(len(client.get_active_tasks()), 3)

    def _connect(self) -> JsonRpcClient:
        return JsonRpcClient(
            websocket=self._websocket,
            logger=self._logger
        )


if __name__ == '__main__':
    unittest.main()
