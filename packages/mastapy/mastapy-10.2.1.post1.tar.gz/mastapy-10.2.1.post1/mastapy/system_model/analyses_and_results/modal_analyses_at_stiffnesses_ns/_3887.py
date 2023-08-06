'''_3887.py

WormGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6261
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3886, _3885, _3821
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'WormGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetModalAnalysesAtStiffnesses',)


class WormGearSetModalAnalysesAtStiffnesses(_3821.GearSetModalAnalysesAtStiffnesses):
    '''WormGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetModalAnalysesAtStiffnesses.TYPE'):
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
    def worm_gears_modal_analyses_at_stiffnesses(self) -> 'List[_3886.WormGearModalAnalysesAtStiffnesses]':
        '''List[WormGearModalAnalysesAtStiffnesses]: 'WormGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsModalAnalysesAtStiffnesses, constructor.new(_3886.WormGearModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_3885.WormGearMeshModalAnalysesAtStiffnesses]':
        '''List[WormGearMeshModalAnalysesAtStiffnesses]: 'WormMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesModalAnalysesAtStiffnesses, constructor.new(_3885.WormGearMeshModalAnalysesAtStiffnesses))
        return value
