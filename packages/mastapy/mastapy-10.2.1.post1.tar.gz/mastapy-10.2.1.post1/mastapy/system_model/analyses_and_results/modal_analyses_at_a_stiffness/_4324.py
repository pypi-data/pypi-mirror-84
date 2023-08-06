'''_4324.py

KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2121
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6194
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4323, _4322, _4321
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness',)


class KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness(_4321.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness):
    '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2121.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6194.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6194.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4323.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtAStiffness, constructor.new(_4323.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4322.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtAStiffness, constructor.new(_4322.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness))
        return value
