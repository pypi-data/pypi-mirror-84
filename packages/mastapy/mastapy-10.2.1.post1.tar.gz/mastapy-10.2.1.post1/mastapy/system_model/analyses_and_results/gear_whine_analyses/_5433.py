'''_5433.py

TorqueConverterConnectionGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1944
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6249
from mastapy.system_model.analyses_and_results.system_deflections import _2377
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5335
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'TorqueConverterConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionGearWhineAnalysis',)


class TorqueConverterConnectionGearWhineAnalysis(_5335.CouplingConnectionGearWhineAnalysis):
    '''TorqueConverterConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1944.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1944.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6249.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6249.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2377.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2377.TorqueConverterConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
