'''_5528.py

MeasurementComponentSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2047
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5574
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'MeasurementComponentSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentSingleMeshWhineAnalysis',)


class MeasurementComponentSingleMeshWhineAnalysis(_5574.VirtualComponentSingleMeshWhineAnalysis):
    '''MeasurementComponentSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2047.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2047.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6199.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6199.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
