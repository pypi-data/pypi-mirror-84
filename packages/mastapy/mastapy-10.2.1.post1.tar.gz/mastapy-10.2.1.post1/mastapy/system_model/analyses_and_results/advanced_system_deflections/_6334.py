'''_6334.py

FaceGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2110
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6163
from mastapy.gears.rating.face import _248
from mastapy.system_model.analyses_and_results.system_deflections import _2309
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6338
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearAdvancedSystemDeflection',)


class FaceGearAdvancedSystemDeflection(_6338.GearAdvancedSystemDeflection):
    '''FaceGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2110.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6163.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6163.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_248.FaceGearRating':
        '''FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_248.FaceGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2309.FaceGearSystemDeflection]':
        '''List[FaceGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2309.FaceGearSystemDeflection))
        return value
