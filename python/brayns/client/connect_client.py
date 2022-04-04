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
from typing import Optional

from brayns.client.client import Client
from brayns.client.client_protocol import ClientProtocol
from brayns.client.jsonrpc.json_rpc_client import JsonRpcClient
from brayns.client.websocket.web_socket_client import WebSocketClient


def connect_client(
    uri: str,
    secure: bool = False,
    cafile: Optional[str] = None,
    loglevel: int = logging.ERROR
) -> ClientProtocol:
    logger = logging.Logger('Brayns', loglevel)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    websocket = WebSocketClient.connect(
        uri=uri,
        secure=secure,
        cafile=cafile
    )
    return Client(
        JsonRpcClient(
            websocket=websocket,
            logger=logger
        )
    )
