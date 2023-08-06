'''_5927.py

PointLoadDynamicAnalysis
'''


from mastapy.system_model.part_model import _2055
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6215
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5961
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PointLoadDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadDynamicAnalysis',)


class PointLoadDynamicAnalysis(_5961.VirtualComponentDynamicAnalysis):
    '''PointLoadDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2055.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2055.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6215.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6215.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
