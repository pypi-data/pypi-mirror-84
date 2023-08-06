'''_6230.py

SpiralBevelGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6228, _6229, _6114
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpiralBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetLoadCase',)


class SpiralBevelGearSetLoadCase(_6114.BevelGearSetLoadCase):
    '''SpiralBevelGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2126.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_load_case(self) -> 'List[_6228.SpiralBevelGearLoadCase]':
        '''List[SpiralBevelGearLoadCase]: 'SpiralBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsLoadCase, constructor.new(_6228.SpiralBevelGearLoadCase))
        return value

    @property
    def spiral_bevel_meshes_load_case(self) -> 'List[_6229.SpiralBevelGearMeshLoadCase]':
        '''List[SpiralBevelGearMeshLoadCase]: 'SpiralBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesLoadCase, constructor.new(_6229.SpiralBevelGearMeshLoadCase))
        return value
