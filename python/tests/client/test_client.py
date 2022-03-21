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

from brayns.client.client import Client
from brayns.client.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.client.jsonrpc.json_rpc_error import JsonRpcError
from brayns.client.jsonrpc.json_rpc_progress import JsonRpcProgress
from brayns.client.jsonrpc.json_rpc_reply import JsonRpcReply
from brayns.client.request_error import RequestError
from brayns.client.request_progress import RequestProgress

from client.helpers.mock_web_socket import MockWebSocket

class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        self._websocket = MockWebSocket()

    def test_request(self) -> None:
        method = 'test'
        params = 123
        result = 456
        with self._connect() as client:
            self._websocket.reply(JsonRpcReply(0, result))
            reply = client.request(method, params)
            self.assertTrue(self._websocket.got_request(method, params))
            self.assertEqual(reply, result)

    def test_error(self) -> None:
        error = RequestError('test', 2, [1, 2, 3])
        with self._connect() as client:
            self._websocket.error(JsonRpcError(0, error))
            with self.assertRaises(RequestError) as context:
                client.request('test', 123)
            self.assertEqual(context.exception, error)

    def test_task(self) -> None:
        method = 'test'
        params = 123
        result = 456
        progresses = [
            RequestProgress('test', 0.1 * i)
            for i in range(10)
        ]
        with self._connect() as client:
            for progress in progresses:
                self._websocket.progress(JsonRpcProgress(0, progress))
            self._websocket.reply(JsonRpcReply(0, result))
            task = client.task(method, params)
            self.assertTrue(self._websocket.got_request(method, params))
            self.assertEqual([progress for progress in task], progresses)
            self.assertEqual(task.wait_for_result(), result)

    def test_cancel(self) -> None:
        error = RequestError('Task cancelled')
        with self._connect() as client:
            self._websocket.reply(JsonRpcReply(1, None))
            self._websocket.error(JsonRpcError(0, error))
            task = client.task('test', 123)
            task.cancel()
            self.assertTrue(self._websocket.got_request('cancel', {'id': 0}))
            with self.assertRaises(RequestError) as context:
                task.wait_for_result()
            self.assertEqual(context.exception, error)

    def _connect(self) -> Client:
        return Client(
            JsonRpcClient(
                websocket=self._websocket,
                logger=logging.Logger('Test')
            )
        )


if __name__ == '__main__':
    unittest.main()
