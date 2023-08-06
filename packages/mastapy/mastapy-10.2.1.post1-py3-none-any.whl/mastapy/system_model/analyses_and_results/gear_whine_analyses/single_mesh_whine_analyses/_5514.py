'''_5514.py

HypoidGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2117
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6185
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5515, _5513, _5461
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'HypoidGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetSingleMeshWhineAnalysis',)


class HypoidGearSetSingleMeshWhineAnalysis(_5461.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis):
    '''HypoidGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2117.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6185.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_single_mesh_whine_analysis(self) -> 'List[_5515.HypoidGearSingleMeshWhineAnalysis]':
        '''List[HypoidGearSingleMeshWhineAnalysis]: 'HypoidGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsSingleMeshWhineAnalysis, constructor.new(_5515.HypoidGearSingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_meshes_single_mesh_whine_analysis(self) -> 'List[_5513.HypoidGearMeshSingleMeshWhineAnalysis]':
        '''List[HypoidGearMeshSingleMeshWhineAnalysis]: 'HypoidMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesSingleMeshWhineAnalysis, constructor.new(_5513.HypoidGearMeshSingleMeshWhineAnalysis))
        return value
