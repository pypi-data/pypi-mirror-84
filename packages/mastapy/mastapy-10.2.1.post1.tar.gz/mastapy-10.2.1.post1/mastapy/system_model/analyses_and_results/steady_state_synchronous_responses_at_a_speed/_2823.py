'''_2823.py

HypoidGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2117
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6185
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2824, _2822, _2770
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'HypoidGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetSteadyStateSynchronousResponseAtASpeed',)


class HypoidGearSetSteadyStateSynchronousResponseAtASpeed(_2770.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed):
    '''HypoidGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2117.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6185.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2824.HypoidGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2824.HypoidGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def hypoid_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2822.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]: 'HypoidMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2822.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
