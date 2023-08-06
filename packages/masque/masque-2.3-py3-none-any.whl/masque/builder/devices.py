from typing import Dict, Iterable, List, Tuple, Union, TypeVar, Any
import copy
import warnings

import numpy        # type: ignore
from numpy import pi

from ..pattern import Pattern
from ..subpattern import SubPattern
from ..traits import PositionableImpl, RotatableImpl, PivotableImpl, Copyable
from ..utils import AutoSlots, rotation_matrix_2d


P = TypeVar('P', bound='Port')
D = TypeVar('D', bound='Device')


class Port(PositionableImpl, RotatableImpl, PivotableImpl, Copyable, metaclass=AutoSlots):
    __slots__ = ('ptype',)

    ptype: int = 0
    """ Port types must match to be plugged together if both are non-zero """

    def __init__(self,
                 offset: numpy.ndarray,
                 angle: float,
                 ptype: int = 0,
                 ) -> None:
        self.offset = offset
        self.angle = angle
        self.ptype = ptype

    def get_bounds(self):
        return numpy.vstack((self.offset, self.offset))

class Device:
    __slots__ = ('pattern', 'ports')

    pattern: Pattern
    """ Layout of this device """

    ports: Dict[str, Port]
    """ Uniquely-named ports which can be used to snap to other Device instances"""

    def __init__(self,
                 pattern: Union[Pattern, str],
                 ports: Dict[str, Port] = None,
                 ) -> None:
        if isinstance(pattern, str):
            self.pattern = Pattern(name=pattern)
        else:
            self.pattern = pattern

        if ports is None:
            self.ports = {
                'left':  Port([0, 0], angle=0, ptype=0),
                'right': Port([0, 0], angle=pi, ptype=0),
                }
        else:
            self.ports = numpy.array(ports)

    def __getitem__(self, key: Union[str, Iterable[str]]) -> numpy.ndarray:
        if isinstance(key, str):
            return self.ports[key]
        else:
            return [self.ports[k] for k in key]

    def build(self: D,
              name: str,
              *args: Any,
              **kwargs: Any,
              ) -> D:
        pat = Pattern(name)
        pat.addsp(self.pattern)
        new = type(self)(pat, ports=self.ports)
        new.plug(*args, **kwargs)
        return new

    def plug(self: D,
             other: D,
             map_in: Dict[str, str],
             map_out: Dict[str, str] = {},
             mirrored: Tuple[bool, bool] = (False, False),
             ) -> D:
        orig_keys = set(self.ports.keys()) - set(map_in.keys())
        other_keys = set(other.ports.keys()) - set(map_out.keys()) - set(map_in.values())
        mapped_keys = set(map_out.values())

        conflicts_final = orig_keys & (other_keys | mapped_keys)
        if conflicts_final:
            raise DeviceError(f'Duplicate port names in requested plug: {conflicts_final}')

        conflicts_partial = other_keys & mapped_keys
        if conflicts_partial:
            raise DeviceError(f'Duplicate port names in output after map_out: {conflicts_partial}')

        translation, rotation, pivot = self.find_transform(other, map_in, map_out, mirrored)

        sp = SubPattern(other.pattern, mirrored=mirrored)
        sp.rotate_around(pivot, rotation)
        sp.translate(translation)
        self.pattern.subpatterns.append(sp)

        other_ports = copy.copy(other.ports)
        # get rid of plugged ports
        for ki, vi in map_in.items():
            del self.ports[ki]
            del other_ports[vi]

        for ko in map_out:
            del other_ports[ko]         # needs separate loop in case of overlap between keys/values
        for ko, vo in map_out.items():
            other_ports[vo] = other.ports[ko]   # pull from original ports

        for name, port in other_ports.items():
            p = port.deepcopy()
            p.rotate_around(pivot, rotation)
            p.translate(translation)
            self.ports[name] = p
        return self

    def find_transform(self,
                       other: Device,
                       map_in: Dict[str, str],
                       map_out: Dict[str, str],
                       mirrored: Tuple[bool, bool] = (False, False),
                       ) -> Tuple[numpy.ndarray, float, numpy.ndarray]:
        s_ports = self[map_in.keys()]
        o_ports = other[map_in.values()]

        s_offsets = numpy.array([p.offset for p in s_ports])
        o_offsets = numpy.array([p.offset for p in o_ports])
        s_angles = numpy.array([p.angle for p in s_ports])
        o_angles = numpy.array([p.angle for p in o_ports])
        s_types = numpy.array([p.type for p in s_ports], dtype=int)
        o_types = numpy.array([p.type for p in o_ports], dtype=int)

        if mirrored[0]:
            o_offsets[:, 1] *= -1
            o_angles += pi
        if mirrored[1]:
            o_offsets[:, 0] *= -1
            o_angles += pi

        type_conflicts = (s_types != o_types) & (s_types != 0) & (o_types != 0)
        if type_conflicts.any():
            ports = numpy.where(type_conflicts)
            msg = 'Ports have conflicting types:\n'
            for nn, (k, v) in enumerate(map_in.items()):
                if type_conflicts[nn]:
                    msg += f'{k} | {s_types[nn]:g}:{o_types[nn]:g} | {v}\n'
            warnings.warn(msg, stacklevel=2)

        rotations = numpy.mod(s_angles - o_angles - pi, 2 * pi)
        if not numpy.allclose(rotations[:1], rotations):
            rot_deg = numpy.rad2deg(rotations)
            msg = f'Port orientations do not match:\n'
            for nn, (k, v) in enumerate(map_in.items()):
                msg += f'{k} | {rot_deg[nn]:g} | {v}\n'
            raise DeviceError(msg)

        rotate_offsets_around(o_offsets, o_offsets[0], rotations[0])
        translations = s_offsets - o_offsets
        if not numpy.allclose(translations[:1], translations):
            msg = f'Port translations do not match:\n'
            for nn, (k, v) in enumerate(map_in.items()):
                msg += f'{k} | {translations[nn]:g} | {v}\n'
            raise DeviceError(msg)

        return translations[0], rotations[0], o_offsets[0]


def rotate_offsets_around(offsets: numpy.ndarray, pivot: numpy.ndarray, angle: float) -> numpy.ndarray:
    offsets -= pivot
    offsets = (rotation_matrix_2d(angle) @ offsets.T).T
    offsets += pivot
    return offsets


class DeviceError(Exception):
    pass
