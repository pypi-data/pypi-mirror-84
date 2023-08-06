'''_2368.py

StraightBevelPlanetGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2131
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3368
from mastapy.system_model.analyses_and_results.system_deflections import _2364
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelPlanetGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearSystemDeflection',)


class StraightBevelPlanetGearSystemDeflection(_2364.StraightBevelDiffGearSystemDeflection):
    '''StraightBevelPlanetGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2131.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3368.StraightBevelPlanetGearPowerFlow':
        '''StraightBevelPlanetGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3368.StraightBevelPlanetGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
