'''_2283.py

ConicalGearMeshSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.conical import _887, _892, _897
from mastapy.system_model.connections_and_sockets.gears import (
    _1908, _1900, _1902, _1904,
    _1916, _1919, _1920, _1921,
    _1924, _1926, _1928, _1932
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.conical import _323
from mastapy.gears.rating.zerol_bevel import _169
from mastapy.gears.rating.straight_bevel_diff import _195
from mastapy.gears.rating.straight_bevel import _199
from mastapy.gears.rating.spiral_bevel import _202
from mastapy.gears.rating.klingelnberg_spiral_bevel import _205
from mastapy.gears.rating.klingelnberg_hypoid import _208
from mastapy.gears.rating.klingelnberg_conical import _211
from mastapy.gears.rating.hypoid import _238
from mastapy.gears.rating.bevel import _338
from mastapy.gears.rating.agma_gleason_conical import _349
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
from mastapy.gears.ltca.conical import _642
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2285, _2255, _2262, _2263,
    _2264, _2267, _2317, _2322,
    _2325, _2328, _2358, _2364,
    _2367, _2368, _2369, _2390,
    _2311
)
from mastapy.system_model.analyses_and_results.power_flows import (
    _3292, _3264, _3271, _3276,
    _3318, _3323, _3326, _3329,
    _3356, _3362, _3365, _3384
)
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConicalGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshSystemDeflection',)


class ConicalGearMeshSystemDeflection(_2311.GearMeshSystemDeflection):
    '''ConicalGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delta_xp(self) -> 'float':
        '''float: 'DeltaXP' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeltaXP

    @property
    def delta_xw(self) -> 'float':
        '''float: 'DeltaXW' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeltaXW

    @property
    def delta_e(self) -> 'float':
        '''float: 'DeltaE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeltaE

    @property
    def delta_sigma(self) -> 'float':
        '''float: 'DeltaSigma' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeltaSigma

    @property
    def loaded_flank(self) -> '_887.ActiveConicalFlank':
        '''ActiveConicalFlank: 'LoadedFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.LoadedFlank)
        return constructor.new(_887.ActiveConicalFlank)(value) if value else None

    @property
    def pinion_torque_for_ltca(self) -> 'float':
        '''float: 'PinionTorqueForLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionTorqueForLTCA

    @property
    def load_in_line_of_action_from_ltca(self) -> 'float':
        '''float: 'LoadInLineOfActionFromLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadInLineOfActionFromLTCA

    @property
    def torque_on_gear_a_due_to_force_in_line_of_action_at_mesh_node(self) -> 'float':
        '''float: 'TorqueOnGearADueToForceInLineOfActionAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueOnGearADueToForceInLineOfActionAtMeshNode

    @property
    def torque_on_gear_b_due_to_force_in_line_of_action_at_mesh_node(self) -> 'float':
        '''float: 'TorqueOnGearBDueToForceInLineOfActionAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueOnGearBDueToForceInLineOfActionAtMeshNode

    @property
    def torque_on_gear_a_due_to_moment_at_mesh_node(self) -> 'float':
        '''float: 'TorqueOnGearADueToMomentAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueOnGearADueToMomentAtMeshNode

    @property
    def torque_on_gear_b_due_to_moment_at_mesh_node(self) -> 'float':
        '''float: 'TorqueOnGearBDueToMomentAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueOnGearBDueToMomentAtMeshNode

    @property
    def linear_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'LinearMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinearMisalignmentInSurfaceOfAction

    @property
    def angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'AngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularMisalignmentInSurfaceOfAction

    @property
    def pinion_angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'PinionAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionAngularMisalignmentInSurfaceOfAction

    @property
    def wheel_angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'WheelAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelAngularMisalignmentInSurfaceOfAction

    @property
    def connection_design(self) -> '_1908.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1908.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1900.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1900.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1902.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1904.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1904.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1916.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1916.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1919.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1919.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1920.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1921.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1921.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1924.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1924.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1926.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1928.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1928.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1932.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1932.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def rating(self) -> '_323.ConicalGearMeshRating':
        '''ConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _323.ConicalGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_mesh_rating(self) -> '_169.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _169.ZerolBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_diff_gear_mesh_rating(self) -> '_195.StraightBevelDiffGearMeshRating':
        '''StraightBevelDiffGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _195.StraightBevelDiffGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelDiffGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_mesh_rating(self) -> '_199.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _199.StraightBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_mesh_rating(self) -> '_202.SpiralBevelGearMeshRating':
        '''SpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _202.SpiralBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(self) -> '_205.KlingelnbergCycloPalloidSpiralBevelGearMeshRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _205.KlingelnbergCycloPalloidSpiralBevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(self) -> '_208.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _208.KlingelnbergCycloPalloidHypoidGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_rating(self) -> '_211.KlingelnbergCycloPalloidConicalGearMeshRating':
        '''KlingelnbergCycloPalloidConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _211.KlingelnbergCycloPalloidConicalGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidConicalGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_hypoid_gear_mesh_rating(self) -> '_238.HypoidGearMeshRating':
        '''HypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _238.HypoidGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to HypoidGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_bevel_gear_mesh_rating(self) -> '_338.BevelGearMeshRating':
        '''BevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _338.BevelGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to BevelGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_agma_gleason_conical_gear_mesh_rating(self) -> '_349.AGMAGleasonConicalGearMeshRating':
        '''AGMAGleasonConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _349.AGMAGleasonConicalGearMeshRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AGMAGleasonConicalGearMeshRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def mesh_design(self) -> '_892.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _892.ConicalGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to ConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_719.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _719.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_728.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_732.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.StraightBevelGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_736.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_740.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_744.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_748.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_hypoid_gear_mesh_design(self) -> '_752.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _752.HypoidGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_bevel_gear_mesh_design(self) -> '_918.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _918.BevelGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def mesh_design_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_931.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _931.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.MeshDesign.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.MeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshDesign.__class__)(self.wrapped.MeshDesign) if self.wrapped.MeshDesign else None

    @property
    def misalignments_pinion(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsPinion) if self.wrapped.MisalignmentsPinion else None

    @property
    def misalignments_wheel(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWheel) if self.wrapped.MisalignmentsWheel else None

    @property
    def misalignments_total(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsTotal) if self.wrapped.MisalignmentsTotal else None

    @property
    def mesh_node_misalignments_pinion(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsPinion) if self.wrapped.MeshNodeMisalignmentsPinion else None

    @property
    def mesh_node_misalignments_wheel(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsWheel) if self.wrapped.MeshNodeMisalignmentsWheel else None

    @property
    def mesh_node_misalignments_total(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsTotal) if self.wrapped.MeshNodeMisalignmentsTotal else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_imported_fe_node_total(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeTotal) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeTotal else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_imported_fe_node_pinion(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodePinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodePinion) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodePinion else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_imported_fe_node_wheel(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeWheel) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceImportedFENodeWheel else None

    @property
    def ltca_results(self) -> '_642.ConicalMeshLoadDistributionAnalysis':
        '''ConicalMeshLoadDistributionAnalysis: 'LTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_642.ConicalMeshLoadDistributionAnalysis)(self.wrapped.LTCAResults) if self.wrapped.LTCAResults else None

    @property
    def gear_a(self) -> '_2285.ConicalGearSystemDeflection':
        '''ConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.ConicalGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_agma_gleason_conical_gear_system_deflection(self) -> '_2255.AGMAGleasonConicalGearSystemDeflection':
        '''AGMAGleasonConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.AGMAGleasonConicalGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AGMAGleasonConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_differential_gear_system_deflection(self) -> '_2262.BevelDifferentialGearSystemDeflection':
        '''BevelDifferentialGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelDifferentialGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_differential_planet_gear_system_deflection(self) -> '_2263.BevelDifferentialPlanetGearSystemDeflection':
        '''BevelDifferentialPlanetGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.BevelDifferentialPlanetGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_differential_sun_gear_system_deflection(self) -> '_2264.BevelDifferentialSunGearSystemDeflection':
        '''BevelDifferentialSunGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.BevelDifferentialSunGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_gear_system_deflection(self) -> '_2267.BevelGearSystemDeflection':
        '''BevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2267.BevelGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_hypoid_gear_system_deflection(self) -> '_2317.HypoidGearSystemDeflection':
        '''HypoidGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.HypoidGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to HypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_conical_gear_system_deflection(self) -> '_2322.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.KlingelnbergCycloPalloidConicalGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(self) -> '_2325.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.KlingelnbergCycloPalloidHypoidGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidHypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(self) -> '_2328.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2328.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_spiral_bevel_gear_system_deflection(self) -> '_2358.SpiralBevelGearSystemDeflection':
        '''SpiralBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2358.SpiralBevelGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to SpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_diff_gear_system_deflection(self) -> '_2364.StraightBevelDiffGearSystemDeflection':
        '''StraightBevelDiffGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2364.StraightBevelDiffGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_gear_system_deflection(self) -> '_2367.StraightBevelGearSystemDeflection':
        '''StraightBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2367.StraightBevelGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_planet_gear_system_deflection(self) -> '_2368.StraightBevelPlanetGearSystemDeflection':
        '''StraightBevelPlanetGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2368.StraightBevelPlanetGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_sun_gear_system_deflection(self) -> '_2369.StraightBevelSunGearSystemDeflection':
        '''StraightBevelSunGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2369.StraightBevelSunGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_zerol_bevel_gear_system_deflection(self) -> '_2390.ZerolBevelGearSystemDeflection':
        '''ZerolBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2390.ZerolBevelGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ZerolBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_2285.ConicalGearSystemDeflection':
        '''ConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.ConicalGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_agma_gleason_conical_gear_system_deflection(self) -> '_2255.AGMAGleasonConicalGearSystemDeflection':
        '''AGMAGleasonConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.AGMAGleasonConicalGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AGMAGleasonConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_differential_gear_system_deflection(self) -> '_2262.BevelDifferentialGearSystemDeflection':
        '''BevelDifferentialGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelDifferentialGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_differential_planet_gear_system_deflection(self) -> '_2263.BevelDifferentialPlanetGearSystemDeflection':
        '''BevelDifferentialPlanetGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.BevelDifferentialPlanetGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_differential_sun_gear_system_deflection(self) -> '_2264.BevelDifferentialSunGearSystemDeflection':
        '''BevelDifferentialSunGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.BevelDifferentialSunGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_gear_system_deflection(self) -> '_2267.BevelGearSystemDeflection':
        '''BevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2267.BevelGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_hypoid_gear_system_deflection(self) -> '_2317.HypoidGearSystemDeflection':
        '''HypoidGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.HypoidGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to HypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_conical_gear_system_deflection(self) -> '_2322.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.KlingelnbergCycloPalloidConicalGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(self) -> '_2325.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.KlingelnbergCycloPalloidHypoidGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidHypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(self) -> '_2328.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2328.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_spiral_bevel_gear_system_deflection(self) -> '_2358.SpiralBevelGearSystemDeflection':
        '''SpiralBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2358.SpiralBevelGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to SpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_diff_gear_system_deflection(self) -> '_2364.StraightBevelDiffGearSystemDeflection':
        '''StraightBevelDiffGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2364.StraightBevelDiffGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_gear_system_deflection(self) -> '_2367.StraightBevelGearSystemDeflection':
        '''StraightBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2367.StraightBevelGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_planet_gear_system_deflection(self) -> '_2368.StraightBevelPlanetGearSystemDeflection':
        '''StraightBevelPlanetGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2368.StraightBevelPlanetGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_sun_gear_system_deflection(self) -> '_2369.StraightBevelSunGearSystemDeflection':
        '''StraightBevelSunGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2369.StraightBevelSunGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_zerol_bevel_gear_system_deflection(self) -> '_2390.ZerolBevelGearSystemDeflection':
        '''ZerolBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2390.ZerolBevelGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ZerolBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def planetaries(self) -> 'List[ConicalGearMeshSystemDeflection]':
        '''List[ConicalGearMeshSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshSystemDeflection))
        return value

    @property
    def power_flow_results(self) -> '_3292.ConicalGearMeshPowerFlow':
        '''ConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3292.ConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_agma_gleason_conical_gear_mesh_power_flow(self) -> '_3264.AGMAGleasonConicalGearMeshPowerFlow':
        '''AGMAGleasonConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3264.AGMAGleasonConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to AGMAGleasonConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_bevel_differential_gear_mesh_power_flow(self) -> '_3271.BevelDifferentialGearMeshPowerFlow':
        '''BevelDifferentialGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3271.BevelDifferentialGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelDifferentialGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_bevel_gear_mesh_power_flow(self) -> '_3276.BevelGearMeshPowerFlow':
        '''BevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3276.BevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_hypoid_gear_mesh_power_flow(self) -> '_3318.HypoidGearMeshPowerFlow':
        '''HypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3318.HypoidGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to HypoidGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(self) -> '_3323.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3323.KlingelnbergCycloPalloidConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(self) -> '_3326.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidHypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3326.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidHypoidGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(self) -> '_3329.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3329.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_spiral_bevel_gear_mesh_power_flow(self) -> '_3356.SpiralBevelGearMeshPowerFlow':
        '''SpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3356.SpiralBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to SpiralBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_straight_bevel_diff_gear_mesh_power_flow(self) -> '_3362.StraightBevelDiffGearMeshPowerFlow':
        '''StraightBevelDiffGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3362.StraightBevelDiffGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelDiffGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_straight_bevel_gear_mesh_power_flow(self) -> '_3365.StraightBevelGearMeshPowerFlow':
        '''StraightBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3365.StraightBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_zerol_bevel_gear_mesh_power_flow(self) -> '_3384.ZerolBevelGearMeshPowerFlow':
        '''ZerolBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3384.ZerolBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ZerolBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
