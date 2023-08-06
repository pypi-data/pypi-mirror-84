﻿'''_2343.py

PointLoadSystemDeflection
'''


from mastapy.system_model.part_model import _2055
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6215
from mastapy.system_model.analyses_and_results.power_flows import _3343
from mastapy.system_model.analyses_and_results.system_deflections import _2384
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PointLoadSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadSystemDeflection',)


class PointLoadSystemDeflection(_2384.VirtualComponentSystemDeflection):
    '''PointLoadSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2055.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2055.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6215.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6215.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3343.PointLoadPowerFlow':
        '''PointLoadPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3343.PointLoadPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
