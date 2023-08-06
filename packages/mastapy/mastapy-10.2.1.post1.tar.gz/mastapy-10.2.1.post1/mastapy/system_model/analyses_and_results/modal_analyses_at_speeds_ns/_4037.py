'''_4037.py

ConceptCouplingHalfModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2160
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6123
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4048
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ConceptCouplingHalfModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfModalAnalysesAtSpeeds',)


class ConceptCouplingHalfModalAnalysesAtSpeeds(_4048.CouplingHalfModalAnalysesAtSpeeds):
    '''ConceptCouplingHalfModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2160.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2160.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6123.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6123.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
