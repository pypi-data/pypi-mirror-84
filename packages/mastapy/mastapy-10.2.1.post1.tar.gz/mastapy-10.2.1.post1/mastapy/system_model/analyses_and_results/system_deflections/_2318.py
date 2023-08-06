'''_2318.py

ImportedFEComponentSystemDeflection
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2042
from mastapy.system_model.analyses_and_results.static_loads import _6186
from mastapy.system_model.analyses_and_results.power_flows import _3321
from mastapy.nodal_analysis.component_mode_synthesis import _1527
from mastapy.nodal_analysis import _1402
from mastapy.math_utility.measured_vectors import _1136, _1132
from mastapy.system_model.analyses_and_results.system_deflections import _2252
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ImportedFEComponentSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentSystemDeflection',)


class ImportedFEComponentSystemDeflection(_2252.AbstractShaftOrHousingSystemDeflection):
    '''ImportedFEComponentSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def export_displacements(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ExportDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportDisplacements

    @property
    def export_forces(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ExportForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportForces

    @property
    def component_design(self) -> '_2042.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2042.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6186.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3321.ImportedFEComponentPowerFlow':
        '''ImportedFEComponentPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3321.ImportedFEComponentPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def full_fe_results(self) -> '_1527.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1527.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults else None

    @property
    def stiffness_in_world_coordinate_system_mn_rad(self) -> '_1402.NodalMatrix':
        '''NodalMatrix: 'StiffnessInWorldCoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1402.NodalMatrix)(self.wrapped.StiffnessInWorldCoordinateSystemMNRad) if self.wrapped.StiffnessInWorldCoordinateSystemMNRad else None

    @property
    def mass_in_world_coordinate_system_mn_rad_s_kg(self) -> '_1402.NodalMatrix':
        '''NodalMatrix: 'MassInWorldCoordinateSystemMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1402.NodalMatrix)(self.wrapped.MassInWorldCoordinateSystemMNRadSKg) if self.wrapped.MassInWorldCoordinateSystemMNRadSKg else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentSystemDeflection))
        return value

    @property
    def applied_internal_forces_in_world_coordinate_system(self) -> 'List[_1136.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'AppliedInternalForcesInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AppliedInternalForcesInWorldCoordinateSystem, constructor.new(_1136.VectorWithLinearAndAngularComponents))
        return value

    @property
    def node_results_in_shaft_coordinate_system(self) -> 'List[_1132.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'NodeResultsInShaftCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsInShaftCoordinateSystem, constructor.new(_1132.ForceAndDisplacementResults))
        return value
