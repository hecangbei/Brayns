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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, TypeVar

from brayns.core.geometry.color import Color
from brayns.instance.instance_protocol import InstanceProtocol

T = TypeVar('T', bound='Renderer')


@dataclass
class Renderer(ABC):

    samples_per_pixel: int = 1
    max_ray_bounces: int = 3
    background_color: Color = Color.bbp_background

    @classmethod
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls: type[T], message: dict) -> T:
        pass

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @staticmethod
    def get_main_renderer_name(instance: InstanceProtocol) -> str:
        return instance.request('get-renderer-type')

    @classmethod
    def from_dict(cls: type[T], message: dict, **kwargs) -> T:
        return cls(
            samples_per_pixel=message['samples_per_pixel'],
            max_ray_bounces=message['max_ray_bounces'],
            background_color=Color(*message['background_color']),
            **kwargs
        )

    @classmethod
    def from_instance(cls: type[T], instance: InstanceProtocol) -> T:
        result = instance.request(f'get-renderer-{cls.name}')
        return cls.deserialize(result)

    @classmethod
    def is_main_renderer(cls, instance: InstanceProtocol) -> None:
        return cls.name == Renderer.get_main_renderer_name(instance)

    def to_dict(self, properties: Optional[dict] = None) -> dict:
        properties = {} if properties is None else properties
        return {
            'samples_per_pixel': self.samples_per_pixel,
            'max_ray_bounces': self.max_ray_bounces,
            'background_color': list(self.background_color)
        } | properties

    def use_as_main_renderer(self, instance: InstanceProtocol) -> None:
        params = self.serialize()
        instance.request(f'set-renderer-{self.name}', params)
