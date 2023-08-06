'''_3304.py

CylindricalGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1910
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.gears.rating.cylindrical import _255
from mastapy.system_model.analyses_and_results.power_flows import _3314
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CylindricalGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshPowerFlow',)


class CylindricalGearMeshPowerFlow(_3314.GearMeshPowerFlow):
    '''CylindricalGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1910.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6143.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6143.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_255.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_255.CylindricalGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_255.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_255.CylindricalGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
