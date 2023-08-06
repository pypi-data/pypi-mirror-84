'''_5345.py

DatumGearWhineAnalysis
'''


from mastapy.system_model.part_model import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6149
from mastapy.system_model.analyses_and_results.system_deflections import _2304
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5323
from mastapy._internal.python_net import python_net_import

_DATUM_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'DatumGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumGearWhineAnalysis',)


class DatumGearWhineAnalysis(_5323.ComponentGearWhineAnalysis):
    '''DatumGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2034.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6149.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6149.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2304.DatumSystemDeflection':
        '''DatumSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2304.DatumSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
