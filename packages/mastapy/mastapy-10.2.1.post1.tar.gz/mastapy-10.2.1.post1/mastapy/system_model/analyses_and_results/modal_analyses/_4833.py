'''_4833.py

PowerLoadModalAnalysis
'''


from mastapy.system_model.part_model import _2056
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6216
from mastapy.system_model.analyses_and_results.system_deflections import _2344
from mastapy.system_model.analyses_and_results.modal_analyses import _4867
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PowerLoadModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadModalAnalysis',)


class PowerLoadModalAnalysis(_4867.VirtualComponentModalAnalysis):
    '''PowerLoadModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadModalAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6216.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6216.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2344.PowerLoadSystemDeflection':
        '''PowerLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2344.PowerLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
