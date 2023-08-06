'''_2048.py

MountableComponent
'''


from typing import Optional

from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1880, _1878, _1883, _1884,
    _1886, _1887, _1889, _1890,
    _1893, _1894, _1895, _1873
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import _1911
from mastapy.system_model.connections_and_sockets.couplings import (
    _1935, _1937, _1939, _1941,
    _1943, _1945, _1946
)
from mastapy.system_model.part_model.shaft_model import _2065
from mastapy.system_model.part_model import _2031, _2030
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponent',)


class MountableComponent(_2030.Component):
    '''MountableComponent

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotation_about_axis(self) -> 'float':
        '''float: 'RotationAboutAxis' is the original name of this property.'''

        return self.wrapped.RotationAboutAxis

    @rotation_about_axis.setter
    def rotation_about_axis(self, value: 'float'):
        self.wrapped.RotationAboutAxis = float(value) if value else 0.0

    @property
    def inner_socket(self) -> '_1880.CylindricalSocket':
        '''CylindricalSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.CylindricalSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cvt_pulley_socket(self) -> '_1878.CVTPulleySocket':
        '''CVTPulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1878.CVTPulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_inner_shaft_connecting_socket(self) -> '_1883.InnerShaftConnectingSocket':
        '''InnerShaftConnectingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1883.InnerShaftConnectingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftConnectingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_inner_shaft_socket(self) -> '_1884.InnerShaftSocket':
        '''InnerShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1884.InnerShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_outer_shaft_connecting_socket(self) -> '_1886.OuterShaftConnectingSocket':
        '''OuterShaftConnectingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.OuterShaftConnectingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftConnectingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_outer_shaft_socket(self) -> '_1887.OuterShaftSocket':
        '''OuterShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1887.OuterShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_planetary_socket(self) -> '_1889.PlanetarySocket':
        '''PlanetarySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1889.PlanetarySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_pulley_socket(self) -> '_1890.PulleySocket':
        '''PulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1890.PulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_rolling_ring_socket(self) -> '_1893.RollingRingSocket':
        '''RollingRingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1893.RollingRingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_shaft_connecting_socket(self) -> '_1894.ShaftConnectingSocket':
        '''ShaftConnectingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.ShaftConnectingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ShaftConnectingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_shaft_socket(self) -> '_1895.ShaftSocket':
        '''ShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1895.ShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_1911.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1911.CylindricalGearTeethSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_clutch_socket(self) -> '_1935.ClutchSocket':
        '''ClutchSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1935.ClutchSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_concept_coupling_socket(self) -> '_1937.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1937.ConceptCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_coupling_socket(self) -> '_1939.CouplingSocket':
        '''CouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1939.CouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_1941.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1941.PartToPartShearCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_spring_damper_socket(self) -> '_1943.SpringDamperSocket':
        '''SpringDamperSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1943.SpringDamperSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_torque_converter_pump_socket(self) -> '_1945.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.TorqueConverterPumpSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_torque_converter_turbine_socket(self) -> '_1946.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.TorqueConverterTurbineSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_connection(self) -> '_1873.CoaxialConnection':
        '''CoaxialConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1873.CoaxialConnection)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def is_mounted(self) -> 'bool':
        '''bool: 'IsMounted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsMounted

    @property
    def inner_component(self) -> '_2065.Shaft':
        '''Shaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.Shaft)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent else None

    def try_mount_on(self, shaft: '_2065.Shaft', offset: Optional['float'] = float('nan')) -> '_2031.ComponentsConnectedResult':
        ''' 'TryMountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryMountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def mount_on(self, shaft: '_2065.Shaft', offset: Optional['float'] = float('nan')) -> '_1873.CoaxialConnection':
        ''' 'MountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.CoaxialConnection
        '''

        offset = float(offset)
        method_result = self.wrapped.MountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
