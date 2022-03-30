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

import ssl
from typing import Any, Callable, Coroutine, Optional

import websockets
from brayns.client.websocket.event_loop import EventLoop


class WebSocketServer:

    ConnectionHandler = Callable[
        [websockets.WebSocketServerProtocol, str],
        Coroutine[Any, Any, None]
    ]

    @staticmethod
    async def echo(
        websocket: websockets.WebSocketServerProtocol,
        path: str
    ) -> None:
        try:
            data = await websocket.recv()
            await websocket.send(data)
        except Exception:
            pass

    @staticmethod
    def start(
        connection_handler: ConnectionHandler,
        uri: str,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        password: Optional[str] = None
    ) -> 'WebSocketServer':
        async def _start():
            host, port = uri.split(':')
            context = None
            if certfile is not None:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(
                    certfile=certfile,
                    keyfile=keyfile,
                    password=password
                )
            return await websockets.serve(
                ws_handler=connection_handler,
                host=host,
                port=int(port),
                ssl=context,
                ping_interval=None,
                close_timeout=0
            )
        loop = EventLoop()
        return WebSocketServer(
            websocket=loop.run(
                _start()
            ).result(),
            loop=loop
        )

    def __init__(
        self,
        websocket: websockets.WebSocketServer,
        loop: EventLoop
    ) -> None:
        self._websocket = websocket
        self._loop = loop

    def __enter__(self) -> 'WebSocketServer':
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    def stop(self) -> None:
        self._websocket.close()
        self._loop.run(
            self._websocket.wait_closed()
        ).result()
        self._loop.close()
