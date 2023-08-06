'''_2134.py

WormGearSet
'''


from typing import List

from mastapy.gears.gear_designs.worm import _725
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2133, _2114
from mastapy.system_model.connections_and_sockets.gears import _1930
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSet',)


class WormGearSet(_2114.GearSet):
    '''WormGearSet

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_725.WormGearSetDesign':
        '''WormGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_725.WormGearSetDesign)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign else None

    @property
    def worm_gear_set_design(self) -> '_725.WormGearSetDesign':
        '''WormGearSetDesign: 'WormGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_725.WormGearSetDesign)(self.wrapped.WormGearSetDesign) if self.wrapped.WormGearSetDesign else None

    @property
    def worm_gears(self) -> 'List[_2133.WormGear]':
        '''List[WormGear]: 'WormGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGears, constructor.new(_2133.WormGear))
        return value

    @property
    def worm_meshes(self) -> 'List[_1930.WormGearMesh]':
        '''List[WormGearMesh]: 'WormMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshes, constructor.new(_1930.WormGearMesh))
        return value
