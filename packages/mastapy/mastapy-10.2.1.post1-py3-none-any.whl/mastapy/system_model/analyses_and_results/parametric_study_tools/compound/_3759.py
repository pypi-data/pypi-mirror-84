'''_3759.py

UnbalancedMassCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2061
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3638
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3760
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'UnbalancedMassCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundParametricStudyTool',)


class UnbalancedMassCompoundParametricStudyTool(_3760.VirtualComponentCompoundParametricStudyTool):
    '''UnbalancedMassCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2061.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2061.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3638.UnbalancedMassParametricStudyTool]':
        '''List[UnbalancedMassParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3638.UnbalancedMassParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3638.UnbalancedMassParametricStudyTool]':
        '''List[UnbalancedMassParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3638.UnbalancedMassParametricStudyTool))
        return value
