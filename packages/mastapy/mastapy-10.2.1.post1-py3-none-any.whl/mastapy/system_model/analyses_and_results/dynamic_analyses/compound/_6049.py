﻿'''_6049.py

PowerLoadCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2056
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5928
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6082
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PowerLoadCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundDynamicAnalysis',)


class PowerLoadCompoundDynamicAnalysis(_6082.VirtualComponentCompoundDynamicAnalysis):
    '''PowerLoadCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2056.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5928.PowerLoadDynamicAnalysis]':
        '''List[PowerLoadDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5928.PowerLoadDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5928.PowerLoadDynamicAnalysis]':
        '''List[PowerLoadDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5928.PowerLoadDynamicAnalysis))
        return value
