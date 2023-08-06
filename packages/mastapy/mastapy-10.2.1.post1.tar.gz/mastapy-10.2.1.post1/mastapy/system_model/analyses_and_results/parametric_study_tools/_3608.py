'''_3608.py

RollingRingAssemblyParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2174
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6219
from mastapy.system_model.analyses_and_results.system_deflections import _2346
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3615
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RollingRingAssemblyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyParametricStudyTool',)


class RollingRingAssemblyParametricStudyTool(_3615.SpecialisedAssemblyParametricStudyTool):
    '''RollingRingAssemblyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2174.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6219.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6219.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2346.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2346.RollingRingAssemblySystemDeflection))
        return value
