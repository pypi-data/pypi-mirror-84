'''_4133.py

WormGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6261
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4132, _4131, _4066
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'WormGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetModalAnalysesAtSpeeds',)


class WormGearSetModalAnalysesAtSpeeds(_4066.GearSetModalAnalysesAtSpeeds):
    '''WormGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2134.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6261.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6261.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_modal_analyses_at_speeds(self) -> 'List[_4132.WormGearModalAnalysesAtSpeeds]':
        '''List[WormGearModalAnalysesAtSpeeds]: 'WormGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsModalAnalysesAtSpeeds, constructor.new(_4132.WormGearModalAnalysesAtSpeeds))
        return value

    @property
    def worm_meshes_modal_analyses_at_speeds(self) -> 'List[_4131.WormGearMeshModalAnalysesAtSpeeds]':
        '''List[WormGearMeshModalAnalysesAtSpeeds]: 'WormMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesModalAnalysesAtSpeeds, constructor.new(_4131.WormGearMeshModalAnalysesAtSpeeds))
        return value
