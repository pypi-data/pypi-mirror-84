'''_4589.py

RootAssemblyModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _2058
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4573, _4507
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'RootAssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyModalAnalysisAtASpeed',)


class RootAssemblyModalAnalysisAtASpeed(_4507.AssemblyModalAnalysisAtASpeed):
    '''RootAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2058.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def modal_analysis_at_a_speed_inputs(self) -> '_4573.ModalAnalysisAtASpeed':
        '''ModalAnalysisAtASpeed: 'ModalAnalysisAtASpeedInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4573.ModalAnalysisAtASpeed)(self.wrapped.ModalAnalysisAtASpeedInputs) if self.wrapped.ModalAnalysisAtASpeedInputs else None
