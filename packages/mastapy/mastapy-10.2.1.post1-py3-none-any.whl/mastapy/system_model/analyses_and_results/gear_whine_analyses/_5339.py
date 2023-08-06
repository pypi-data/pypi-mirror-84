'''_5339.py

CVTGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2163
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2293
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5307
from mastapy._internal.python_net import python_net_import

_CVT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CVTGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTGearWhineAnalysis',)


class CVTGearWhineAnalysis(_5307.BeltDriveGearWhineAnalysis):
    '''CVTGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2163.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def system_deflection_results(self) -> '_2293.CVTSystemDeflection':
        '''CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2293.CVTSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
