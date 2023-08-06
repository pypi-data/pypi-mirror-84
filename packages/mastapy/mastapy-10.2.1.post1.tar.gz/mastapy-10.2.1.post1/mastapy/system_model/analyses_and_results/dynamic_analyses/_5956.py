'''_5956.py

TorqueConverterConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1944
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6249
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5880
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'TorqueConverterConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionDynamicAnalysis',)


class TorqueConverterConnectionDynamicAnalysis(_5880.CouplingConnectionDynamicAnalysis):
    '''TorqueConverterConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionDynamicAnalysis.TYPE'):
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
