'''_4828.py

PartToPartShearCouplingModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2165
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6208
from mastapy.system_model.analyses_and_results.system_deflections import _2340
from mastapy.system_model.analyses_and_results.modal_analyses import _4783
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PartToPartShearCouplingModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingModalAnalysis',)


class PartToPartShearCouplingModalAnalysis(_4783.CouplingModalAnalysis):
    '''PartToPartShearCouplingModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2165.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2165.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6208.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6208.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2340.PartToPartShearCouplingSystemDeflection':
        '''PartToPartShearCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2340.PartToPartShearCouplingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
