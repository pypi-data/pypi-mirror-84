'''_5896.py

FaceGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5894, _5895, _5900
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'FaceGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetDynamicAnalysis',)


class FaceGearSetDynamicAnalysis(_5900.GearSetDynamicAnalysis):
    '''FaceGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2111.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6165.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_dynamic_analysis(self) -> 'List[_5894.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'FaceGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsDynamicAnalysis, constructor.new(_5894.FaceGearDynamicAnalysis))
        return value

    @property
    def face_meshes_dynamic_analysis(self) -> 'List[_5895.FaceGearMeshDynamicAnalysis]':
        '''List[FaceGearMeshDynamicAnalysis]: 'FaceMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesDynamicAnalysis, constructor.new(_5895.FaceGearMeshDynamicAnalysis))
        return value
