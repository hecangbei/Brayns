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

from dataclasses import dataclass

from brayns.core.parameters.time_unit import TimeUnit
from brayns.instance.instance_protocol import InstanceProtocol


@dataclass
class AnimationParameters:

    start_frame: int = 0
    end_frame: int = 0
    current_frame: int = 0
    delta_time: float = 0.0
    time_unit: TimeUnit = TimeUnit.MILLISECOND

    @staticmethod
    def from_instance(instance: InstanceProtocol) -> 'AnimationParameters':
        result = instance.request('get-animation-parameters')
        return AnimationParameters.deserialize(result)

    @staticmethod
    def deserialize(message: dict) -> 'AnimationParameters':
        return AnimationParameters(
            start_frame=message['start_frame'],
            end_frame=message['end_frame'],
            current_frame=message['current'],
            delta_time=message['dt'],
            time_unit=TimeUnit(message['unit'])
        )

    def update(self, instance: InstanceProtocol) -> None:
        params = self.serialize()
        instance.request('set-animation-parameters', params)

    def serialize(self) -> dict:
        return {
            'start_frame': self.start_frame,
            'end_frame': self.end_frame,
            'current': self.current_frame
        }

    def clamp(self, frame: int) -> int:
        return max(min(frame, self.end_frame), self.start_frame)

    def get_timestamp(self, frame: int) -> float:
        return (frame - self.start_frame) * self.delta_time

    def get_frame(self, timestamp: float) -> int:
        frame_count = round(timestamp / self.delta_time)
        return self.start_frame + frame_count

    def get_frames(self, duration: float, timestep: float = 0.0) -> list[int]:
        frames = []
        t = 0.0
        dt = timestep if timestep > 0.0 else self.delta_time
        while t <= duration:
            frame = self.get_frame(t)
            if frame > self.end_frame:
                return frames
            frames.append(frame)
            t += dt
        return frames
