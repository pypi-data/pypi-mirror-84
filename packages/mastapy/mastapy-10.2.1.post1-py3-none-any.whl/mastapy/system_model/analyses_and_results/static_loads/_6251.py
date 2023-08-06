'''_6251.py

TorqueConverterPumpLoadCase
'''


from mastapy.system_model.part_model.couplings import _2184
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6136
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterPumpLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpLoadCase',)


class TorqueConverterPumpLoadCase(_6136.CouplingHalfLoadCase):
    '''TorqueConverterPumpLoadCase

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2184.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2184.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
