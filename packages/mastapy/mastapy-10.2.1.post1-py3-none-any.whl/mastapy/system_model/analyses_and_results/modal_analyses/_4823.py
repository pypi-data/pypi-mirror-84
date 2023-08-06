'''_4823.py

OilSealModalAnalysis
'''


from mastapy.system_model.part_model import _2050
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6203
from mastapy.system_model.analyses_and_results.system_deflections import _2336
from mastapy.system_model.analyses_and_results.modal_analyses import _4779
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'OilSealModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealModalAnalysis',)


class OilSealModalAnalysis(_4779.ConnectorModalAnalysis):
    '''OilSealModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2050.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2050.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6203.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6203.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2336.OilSealSystemDeflection':
        '''OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2336.OilSealSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
