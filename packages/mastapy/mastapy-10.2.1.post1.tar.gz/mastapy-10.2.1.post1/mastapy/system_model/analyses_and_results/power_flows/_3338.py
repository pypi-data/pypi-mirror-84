'''_3338.py

PartToPartShearCouplingHalfPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2166
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6207
from mastapy.system_model.analyses_and_results.power_flows import _3298
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PartToPartShearCouplingHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfPowerFlow',)


class PartToPartShearCouplingHalfPowerFlow(_3298.CouplingHalfPowerFlow):
    '''PartToPartShearCouplingHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2166.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6207.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6207.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
