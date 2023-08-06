'''_5515.py

HypoidGearSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2116
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6183
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5462
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'HypoidGearSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSingleMeshWhineAnalysis',)


class HypoidGearSingleMeshWhineAnalysis(_5462.AGMAGleasonConicalGearSingleMeshWhineAnalysis):
    '''HypoidGearSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2116.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6183.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6183.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
