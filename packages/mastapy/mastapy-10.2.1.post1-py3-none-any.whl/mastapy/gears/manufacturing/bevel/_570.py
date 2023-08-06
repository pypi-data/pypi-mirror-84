'''_570.py

ConicalMeshMicroGeometryConfigBase
'''


from mastapy.gears.manufacturing.bevel import (
    _561, _559, _560, _571,
    _572, _577
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.conical import _892
from mastapy.gears.gear_designs.zerol_bevel import _719
from mastapy.gears.gear_designs.straight_bevel_diff import _728
from mastapy.gears.gear_designs.straight_bevel import _732
from mastapy.gears.gear_designs.spiral_bevel import _736
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _740
from mastapy.gears.gear_designs.klingelnberg_hypoid import _744
from mastapy.gears.gear_designs.klingelnberg_conical import _748
from mastapy.gears.gear_designs.hypoid import _752
from mastapy.gears.gear_designs.bevel import _918
from mastapy.gears.gear_designs.agma_gleason_conical import _931
from mastapy.gears.analysis import _959
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshMicroGeometryConfigBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMicroGeometryConfigBase',)


class ConicalMeshMicroGeometryConfigBase(_959.GearMeshImplementationDetail):
    '''ConicalMeshMicroGeometryConfigBase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshMicroGeometryConfigBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_config(self) -> '_561.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _561.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_manufacturing_config(self) -> '_559.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _559.ConicalGearManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_micro_geometry_config(self) -> '_560.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _560.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_manufacturing_config(self) -> '_571.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _571.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_micro_geometry_config(self) -> '_572.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _572.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_wheel_manufacturing_config(self) -> '_577.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _577.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def mesh(self) -> '_892.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _892.ConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_zerol_bevel_gear_mesh_design(self) -> '_719.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _719.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_728.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_gear_mesh_design(self) -> '_732.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.StraightBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_spiral_bevel_gear_mesh_design(self) -> '_736.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_740.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_744.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_748.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_hypoid_gear_mesh_design(self) -> '_752.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _752.HypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_bevel_gear_mesh_design(self) -> '_918.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _918.BevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_931.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _931.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None
