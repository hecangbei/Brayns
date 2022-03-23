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
import sys
import unittest

from brayns.client.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.client.jsonrpc.json_rpc_error import JsonRpcError
from brayns.client.jsonrpc.json_rpc_progress import JsonRpcProgress
from brayns.client.jsonrpc.json_rpc_reply import JsonRpcReply
from brayns.client.jsonrpc.json_rpc_request import JsonRpcRequest
from brayns.client.request_error import RequestError
from brayns.client.request_progress import RequestProgress

from client.websocket.mock_web_socket import MockWebSocket


class TestJsonRpcClient(unittest.TestCase):

    def setUp(self) -> None:
        self._logger = logging.Logger('Test')
        self._websocket = MockWebSocket()

    def test_connection(self) -> None:
        with self._connect():
            pass
        self.assertTrue(self._websocket.closed)

    def test_notification(self) -> None:
        notification = JsonRpcRequest(None, 'test', 1)
        with self._connect() as client:
            task = client.send(notification)
            self.assertTrue(self._websocket.has_received([notification]))
            self.assertEqual(len(client.get_active_tasks()), 0)
            self.assertEqual(task.get_result(), None)

    def test_request(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        reply = JsonRpcReply(0, 456)
        with self._connect() as client:
            task = client.send(request)
            self.assertTrue(self._websocket.has_received([request]))
            self.assertFalse(task.is_ready())
            self.assertEqual(len(client.get_active_tasks()), 1)
            self._websocket.reply(reply)
            client.poll()
            self.assertEqual(task.get_result(), reply.result)
            self.assertEqual(len(client.get_active_tasks()), 0)

    def test_multiple_requests(self) -> None:
        requests = [
            JsonRpcRequest(0, 'test1', 123),
            JsonRpcRequest(1, 'test2', 456),
            JsonRpcRequest(2, 'test3', 789)
        ]
        replies = [
            JsonRpcReply(0, 12),
            JsonRpcReply(1, 34)
        ]
        with self._connect() as client:
            tasks = [client.send(request) for request in requests]
            self.assertTrue(self._websocket.has_received(requests))
            self.assertEqual(len(client.get_active_tasks()), 3)
            for task in tasks:
                self.assertFalse(task.is_ready())
            for reply in replies:
                self._websocket.reply(reply)
                client.poll()
            self.assertEqual(len(client.get_active_tasks()), 1)
            for task, reply in zip(tasks, replies):
                self.assertEqual(task.get_result(), reply.result)

    def test_progress(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        progress = RequestProgress('test', 0.5)
        message = JsonRpcProgress(0, progress)
        with self._connect() as client:
            task = client.send(request)
            self._websocket.progress(message)
            client.poll()
            self.assertFalse(task.is_ready())
            self.assertEqual(task.get_progress(), progress)

    def test_error(self) -> None:
        request = JsonRpcRequest(0, 'test', 123)
        error = RequestError('test', 2, 123)
        message = JsonRpcError(0, error)
        with self._connect() as client:
            task = client.send(request)
            self._websocket.error(message)
            client.poll()
            self.assertTrue(task.is_ready())
            with self.assertRaises(RequestError) as context:
                task.get_result()
            self.assertEqual(context.exception, error)

    def test_general_error(self) -> None:
        requests = [
            JsonRpcRequest(0, 'test1', 123),
            JsonRpcRequest(1, 'test2', 456),
            JsonRpcRequest(2, 'test3', 789)
        ]
        error = RequestError('test', 3, 123)
        message = JsonRpcError(None, error)
        with self._connect() as client:
            tasks = [client.send(request) for request in requests]
            self._websocket.error(message)
            client.poll()
            self.assertEqual(len(client.get_active_tasks()), 0)
            for task in tasks:
                with self.assertRaises(RequestError) as context:
                    task.get_result()
                self.assertEqual(context.exception, error)

    def test_logging(self) -> None:
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        with self.assertLogs(self._logger, logging.DEBUG) as context:
            with self._connect() as client:
                client.send(JsonRpcRequest(0, 'test', 123))
                self._websocket.reply(JsonRpcReply(0, 456))
                client.poll()
                client.send(JsonRpcRequest(0, 'test', 123))
                self._websocket.error(JsonRpcError(0, RequestError('test')))
                client.poll()
                self._websocket.progress(JsonRpcProgress(
                    0, RequestProgress('test', 0.5)))
                client.poll()
        self.assertEqual(len(context.output), 9)

    def _connect(self) -> JsonRpcClient:
        return JsonRpcClient(
            websocket=self._websocket,
            logger=self._logger
        )


if __name__ == '__main__':
    unittest.main()
