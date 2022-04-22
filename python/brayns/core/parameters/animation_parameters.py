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

from brayns.core.parameters.time_unit import TimeUnit
from brayns.instance.instance_protocol import InstanceProtocol


class AnimationParameters:

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

    def __init__(
        self,
        start_frame: int,
        end_frame: int,
        current_frame: int,
        delta_time: float = 0.0,
        time_unit: TimeUnit = TimeUnit.MILLISECOND
    ) -> None:
        self._start_frame = start_frame
        self._end_frame = end_frame
        self._current_frame = current_frame
        self._delta_time = delta_time
        self._time_unit = time_unit

    @property
    def start_frame(self) -> int:
        return self._start_frame

    @start_frame.setter
    def start_frame(self, value: int) -> None:
        self._start_frame = value

    @property
    def end_frame(self) -> int:
        return self._end_frame

    @end_frame.setter
    def end_frame(self, value: int) -> None:
        self._end_frame = value

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value: int) -> None:
        self._current_frame = value

    @property
    def delta_time(self) -> float:
        return self._delta_time

    @property
    def time_unit(self) -> TimeUnit:
        return self._time_unit

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
