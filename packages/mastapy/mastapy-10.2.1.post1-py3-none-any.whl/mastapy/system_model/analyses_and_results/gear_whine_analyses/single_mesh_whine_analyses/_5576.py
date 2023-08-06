'''_5576.py

WormGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6261
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5577, _5575, _5510
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'WormGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetSingleMeshWhineAnalysis',)


class WormGearSetSingleMeshWhineAnalysis(_5510.GearSetSingleMeshWhineAnalysis):
    '''WormGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetSingleMeshWhineAnalysis.TYPE'):
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
    def worm_gears_single_mesh_whine_analysis(self) -> 'List[_5577.WormGearSingleMeshWhineAnalysis]':
        '''List[WormGearSingleMeshWhineAnalysis]: 'WormGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsSingleMeshWhineAnalysis, constructor.new(_5577.WormGearSingleMeshWhineAnalysis))
        return value

    @property
    def worm_meshes_single_mesh_whine_analysis(self) -> 'List[_5575.WormGearMeshSingleMeshWhineAnalysis]':
        '''List[WormGearMeshSingleMeshWhineAnalysis]: 'WormMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesSingleMeshWhineAnalysis, constructor.new(_5575.WormGearMeshSingleMeshWhineAnalysis))
        return value
