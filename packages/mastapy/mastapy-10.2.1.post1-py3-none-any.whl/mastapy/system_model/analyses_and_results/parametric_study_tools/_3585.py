'''_3585.py

MeasurementComponentParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2047
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy.system_model.analyses_and_results.system_deflections import _2332
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3639
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'MeasurementComponentParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentParametricStudyTool',)


class MeasurementComponentParametricStudyTool(_3639.VirtualComponentParametricStudyTool):
    '''MeasurementComponentParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2047.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2047.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6199.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6199.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2332.MeasurementComponentSystemDeflection]':
        '''List[MeasurementComponentSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2332.MeasurementComponentSystemDeflection))
        return value
