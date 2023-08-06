'''_5430.py

SynchroniserHalfGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2180
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6243
from mastapy.system_model.analyses_and_results.system_deflections import _2370
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5431
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SynchroniserHalfGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfGearWhineAnalysis',)


class SynchroniserHalfGearWhineAnalysis(_5431.SynchroniserPartGearWhineAnalysis):
    '''SynchroniserHalfGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2180.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6243.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6243.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2370.SynchroniserHalfSystemDeflection':
        '''SynchroniserHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2370.SynchroniserHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
