'''_4872.py

WhineWaterfallSettings
'''


from typing import List

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.math_utility import (
    _1081, _1105, _1069, _1093,
    _1080, _1065, _1079, _1099
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4780, _4869, _4868, _4824,
    _4870
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import (
    _5447, _5450, _5456, _5457
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5363, _5414
from mastapy.utility.units_and_measurements.measurements import (
    _1224, _1177, _1276, _1183,
    _1174, _1179, _1198, _1271,
    _1192, _1242, _1243, _1246
)
from mastapy.utility.property import _1371
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_WHINE_WATERFALL_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WhineWaterfallSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('WhineWaterfallSettings',)


class WhineWaterfallSettings(_0.APIBase):
    '''WhineWaterfallSettings

    This is a mastapy class.
    '''

    TYPE = _WHINE_WATERFALL_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WhineWaterfallSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def response_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType: 'ResponseType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ResponseType, value) if self.wrapped.ResponseType else None

    @response_type.setter
    def response_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ResponseType = value

    @property
    def translation_or_rotation(self) -> '_1105.TranslationRotation':
        '''TranslationRotation: 'TranslationOrRotation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TranslationOrRotation)
        return constructor.new(_1105.TranslationRotation)(value) if value else None

    @translation_or_rotation.setter
    def translation_or_rotation(self, value: '_1105.TranslationRotation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TranslationOrRotation = value

    @property
    def coordinate_system(self) -> '_4780.CoordinateSystemForWhine':
        '''CoordinateSystemForWhine: 'CoordinateSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CoordinateSystem)
        return constructor.new(_4780.CoordinateSystemForWhine)(value) if value else None

    @coordinate_system.setter
    def coordinate_system(self, value: '_4780.CoordinateSystemForWhine'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystem = value

    @property
    def complex_component(self) -> '_1069.ComplexPartDisplayOption':
        '''ComplexPartDisplayOption: 'ComplexComponent' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ComplexComponent)
        return constructor.new(_1069.ComplexPartDisplayOption)(value) if value else None

    @complex_component.setter
    def complex_component(self, value: '_1069.ComplexPartDisplayOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ComplexComponent = value

    @property
    def magnitude_method_for_complex_vectors(self) -> '_1093.ComplexMagnitudeMethod':
        '''ComplexMagnitudeMethod: 'MagnitudeMethodForComplexVectors' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MagnitudeMethodForComplexVectors)
        return constructor.new(_1093.ComplexMagnitudeMethod)(value) if value else None

    @magnitude_method_for_complex_vectors.setter
    def magnitude_method_for_complex_vectors(self, value: '_1093.ComplexMagnitudeMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MagnitudeMethodForComplexVectors = value

    @property
    def max_harmonic(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'MaxHarmonic' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.MaxHarmonic) if self.wrapped.MaxHarmonic else None

    @max_harmonic.setter
    def max_harmonic(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.MaxHarmonic = value

    @property
    def dynamic_scaling(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling: 'DynamicScaling' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.DynamicScaling, value) if self.wrapped.DynamicScaling else None

    @dynamic_scaling.setter
    def dynamic_scaling(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DynamicScaling = value

    @property
    def weighting(self) -> '_1065.AcousticWeighting':
        '''AcousticWeighting: 'Weighting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Weighting)
        return constructor.new(_1065.AcousticWeighting)(value) if value else None

    @weighting.setter
    def weighting(self, value: '_1065.AcousticWeighting'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Weighting = value

    @property
    def show_coupled_modes(self) -> 'bool':
        '''bool: 'ShowCoupledModes' is the original name of this property.'''

        return self.wrapped.ShowCoupledModes

    @show_coupled_modes.setter
    def show_coupled_modes(self, value: 'bool'):
        self.wrapped.ShowCoupledModes = bool(value) if value else False

    @property
    def reduce_number_of_result_points(self) -> 'bool':
        '''bool: 'ReduceNumberOfResultPoints' is the original name of this property.'''

        return self.wrapped.ReduceNumberOfResultPoints

    @reduce_number_of_result_points.setter
    def reduce_number_of_result_points(self, value: 'bool'):
        self.wrapped.ReduceNumberOfResultPoints = bool(value) if value else False

    @property
    def chart_type(self) -> '_1079.DynamicsResponse3DChartType':
        '''DynamicsResponse3DChartType: 'ChartType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ChartType)
        return constructor.new(_1079.DynamicsResponse3DChartType)(value) if value else None

    @chart_type.setter
    def chart_type(self, value: '_1079.DynamicsResponse3DChartType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartType = value

    @property
    def maximum_order(self) -> 'float':
        '''float: 'MaximumOrder' is the original name of this property.'''

        return self.wrapped.MaximumOrder

    @maximum_order.setter
    def maximum_order(self, value: 'float'):
        self.wrapped.MaximumOrder = float(value) if value else 0.0

    @property
    def minimum_order(self) -> 'float':
        '''float: 'MinimumOrder' is the original name of this property.'''

        return self.wrapped.MinimumOrder

    @minimum_order.setter
    def minimum_order(self, value: 'float'):
        self.wrapped.MinimumOrder = float(value) if value else 0.0

    @property
    def connected_component_type(self) -> '_5447.ConnectedComponentType':
        '''ConnectedComponentType: 'ConnectedComponentType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ConnectedComponentType)
        return constructor.new(_5447.ConnectedComponentType)(value) if value else None

    @connected_component_type.setter
    def connected_component_type(self, value: '_5447.ConnectedComponentType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConnectedComponentType = value

    @property
    def whine_waterfall_export_option(self) -> '_4869.WhineWaterfallExportOption':
        '''WhineWaterfallExportOption: 'WhineWaterfallExportOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.WhineWaterfallExportOption)
        return constructor.new(_4869.WhineWaterfallExportOption)(value) if value else None

    @whine_waterfall_export_option.setter
    def whine_waterfall_export_option(self, value: '_4869.WhineWaterfallExportOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WhineWaterfallExportOption = value

    @property
    def number_of_additional_points_either_side_of_order_line(self) -> 'int':
        '''int: 'NumberOfAdditionalPointsEitherSideOfOrderLine' is the original name of this property.'''

        return self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine

    @number_of_additional_points_either_side_of_order_line.setter
    def number_of_additional_points_either_side_of_order_line(self, value: 'int'):
        self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine = int(value) if value else 0

    @property
    def selected_excitations(self) -> '_5450.ExcitationSourceSelectionGroup':
        '''ExcitationSourceSelectionGroup: 'SelectedExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5450.ExcitationSourceSelectionGroup)(self.wrapped.SelectedExcitations) if self.wrapped.SelectedExcitations else None

    @property
    def waterfall_chart_settings(self) -> '_4868.WaterfallChartSettings':
        '''WaterfallChartSettings: 'WaterfallChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4868.WaterfallChartSettings)(self.wrapped.WaterfallChartSettings) if self.wrapped.WaterfallChartSettings else None

    @property
    def order_cuts_chart_settings(self) -> '_4824.OrderCutsChartSettings':
        '''OrderCutsChartSettings: 'OrderCutsChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4824.OrderCutsChartSettings)(self.wrapped.OrderCutsChartSettings) if self.wrapped.OrderCutsChartSettings else None

    @property
    def frequency_options(self) -> '_5363.FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5363.FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def reference_speed_options(self) -> '_5414.SpeedOptionsForGearWhineAnalysisResults':
        '''SpeedOptionsForGearWhineAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5414.SpeedOptionsForGearWhineAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def very_short_length_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1224.LengthVeryShort]':
        '''WhineWaterfallReferenceValues[LengthVeryShort]: 'VeryShortLengthReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1224.LengthVeryShort](self.wrapped.VeryShortLengthReferenceValues) if self.wrapped.VeryShortLengthReferenceValues else None

    @property
    def small_angle_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1177.AngleSmall]':
        '''WhineWaterfallReferenceValues[AngleSmall]: 'SmallAngleReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1177.AngleSmall](self.wrapped.SmallAngleReferenceValues) if self.wrapped.SmallAngleReferenceValues else None

    @property
    def small_velocity_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1276.VelocitySmall]':
        '''WhineWaterfallReferenceValues[VelocitySmall]: 'SmallVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1276.VelocitySmall](self.wrapped.SmallVelocityReferenceValues) if self.wrapped.SmallVelocityReferenceValues else None

    @property
    def angular_velocity_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1183.AngularVelocity]':
        '''WhineWaterfallReferenceValues[AngularVelocity]: 'AngularVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1183.AngularVelocity](self.wrapped.AngularVelocityReferenceValues) if self.wrapped.AngularVelocityReferenceValues else None

    @property
    def acceleration_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1174.Acceleration]':
        '''WhineWaterfallReferenceValues[Acceleration]: 'AccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1174.Acceleration](self.wrapped.AccelerationReferenceValues) if self.wrapped.AccelerationReferenceValues else None

    @property
    def angular_acceleration_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1179.AngularAcceleration]':
        '''WhineWaterfallReferenceValues[AngularAcceleration]: 'AngularAccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1179.AngularAcceleration](self.wrapped.AngularAccelerationReferenceValues) if self.wrapped.AngularAccelerationReferenceValues else None

    @property
    def force_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1198.Force]':
        '''WhineWaterfallReferenceValues[Force]: 'ForceReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1198.Force](self.wrapped.ForceReferenceValues) if self.wrapped.ForceReferenceValues else None

    @property
    def torque_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1271.Torque]':
        '''WhineWaterfallReferenceValues[Torque]: 'TorqueReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1271.Torque](self.wrapped.TorqueReferenceValues) if self.wrapped.TorqueReferenceValues else None

    @property
    def energy_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1192.Energy]':
        '''WhineWaterfallReferenceValues[Energy]: 'EnergyReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1192.Energy](self.wrapped.EnergyReferenceValues) if self.wrapped.EnergyReferenceValues else None

    @property
    def power_small_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1242.PowerSmall]':
        '''WhineWaterfallReferenceValues[PowerSmall]: 'PowerSmallReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1242.PowerSmall](self.wrapped.PowerSmallReferenceValues) if self.wrapped.PowerSmallReferenceValues else None

    @property
    def power_small_per_unit_area_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1243.PowerSmallPerArea]':
        '''WhineWaterfallReferenceValues[PowerSmallPerArea]: 'PowerSmallPerUnitAreaReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1243.PowerSmallPerArea](self.wrapped.PowerSmallPerUnitAreaReferenceValues) if self.wrapped.PowerSmallPerUnitAreaReferenceValues else None

    @property
    def pressure_reference_values(self) -> '_4870.WhineWaterfallReferenceValues[_1246.Pressure]':
        '''WhineWaterfallReferenceValues[Pressure]: 'PressureReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4870.WhineWaterfallReferenceValues)[_1246.Pressure](self.wrapped.PressureReferenceValues) if self.wrapped.PressureReferenceValues else None

    @property
    def result_location_selection_groups(self) -> '_5456.ResultLocationSelectionGroups':
        '''ResultLocationSelectionGroups: 'ResultLocationSelectionGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5456.ResultLocationSelectionGroups)(self.wrapped.ResultLocationSelectionGroups) if self.wrapped.ResultLocationSelectionGroups else None

    @property
    def active_result_locations(self) -> 'List[_5457.ResultNodeSelection]':
        '''List[ResultNodeSelection]: 'ActiveResultLocations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ActiveResultLocations, constructor.new(_5457.ResultNodeSelection))
        return value

    @property
    def degrees_of_freedom(self) -> 'List[_1371.EnumWithBool[_1099.ResultOptionsFor3DVector]]':
        '''List[EnumWithBool[ResultOptionsFor3DVector]]: 'DegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DegreesOfFreedom, constructor.new(_1371.EnumWithBool)[_1099.ResultOptionsFor3DVector])
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
