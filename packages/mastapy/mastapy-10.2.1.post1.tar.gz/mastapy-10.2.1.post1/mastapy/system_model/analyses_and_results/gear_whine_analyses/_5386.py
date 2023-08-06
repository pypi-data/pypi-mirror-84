'''_5386.py

KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2121
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6194
from mastapy.system_model.analyses_and_results.system_deflections import _2324
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5384, _5385, _5383
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis(_5383.KlingelnbergCycloPalloidConicalGearSetGearWhineAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2121.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6194.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6194.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2324.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2324.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5384.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5384.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_gear_whine_analysis(self) -> 'List[_5384.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsGearWhineAnalysis, constructor.new(_5384.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5385.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5385.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_gear_whine_analysis(self) -> 'List[_5385.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesGearWhineAnalysis, constructor.new(_5385.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis))
        return value
