'''_2308.py

FaceGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.power_flows import _3312
from mastapy.gears.rating.face import _250
from mastapy.system_model.analyses_and_results.system_deflections import _2309, _2307, _2312
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FaceGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetSystemDeflection',)


class FaceGearSetSystemDeflection(_2312.GearSetSystemDeflection):
    '''FaceGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2111.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6165.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3312.FaceGearSetPowerFlow':
        '''FaceGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3312.FaceGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_250.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_250.FaceGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_250.FaceGearSetRating':
        '''FaceGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_250.FaceGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def face_gears_system_deflection(self) -> 'List[_2309.FaceGearSystemDeflection]':
        '''List[FaceGearSystemDeflection]: 'FaceGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsSystemDeflection, constructor.new(_2309.FaceGearSystemDeflection))
        return value

    @property
    def face_meshes_system_deflection(self) -> 'List[_2307.FaceGearMeshSystemDeflection]':
        '''List[FaceGearMeshSystemDeflection]: 'FaceMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesSystemDeflection, constructor.new(_2307.FaceGearMeshSystemDeflection))
        return value
