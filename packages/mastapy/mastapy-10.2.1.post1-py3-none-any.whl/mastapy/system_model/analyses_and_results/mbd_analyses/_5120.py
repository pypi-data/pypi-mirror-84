'''_5120.py

SpiralBevelGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6230
from mastapy.system_model.analyses_and_results.mbd_analyses import _5119, _5118, _5030
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpiralBevelGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetMultiBodyDynamicsAnalysis',)


class SpiralBevelGearSetMultiBodyDynamicsAnalysis(_5030.BevelGearSetMultiBodyDynamicsAnalysis):
    '''SpiralBevelGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2126.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6230.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6230.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5119.SpiralBevelGearMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5119.SpiralBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gears_multi_body_dynamics_analysis(self) -> 'List[_5119.SpiralBevelGearMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultiBodyDynamicsAnalysis]: 'SpiralBevelGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsMultiBodyDynamicsAnalysis, constructor.new(_5119.SpiralBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_multi_body_dynamics_analysis(self) -> 'List[_5118.SpiralBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshMultiBodyDynamicsAnalysis]: 'SpiralBevelMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesMultiBodyDynamicsAnalysis, constructor.new(_5118.SpiralBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
