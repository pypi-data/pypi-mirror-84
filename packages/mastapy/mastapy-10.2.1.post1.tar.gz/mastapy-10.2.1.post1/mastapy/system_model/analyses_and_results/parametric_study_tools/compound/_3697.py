'''_3697.py

GearCompoundParametricStudyTool
'''


from mastapy.gears.rating import _158
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _172
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _245
from mastapy.gears.rating.cylindrical import _252
from mastapy.gears.rating.conical import _322
from mastapy.gears.rating.concept import _332
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3717
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundParametricStudyTool',)


class GearCompoundParametricStudyTool(_3717.MountableComponentCompoundParametricStudyTool):
    '''GearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_results(self) -> '_158.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_worm_gear_duty_cycle_rating(self) -> '_172.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _172.WormGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_face_gear_duty_cycle_rating(self) -> '_245.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _245.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_252.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _252.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_conical_gear_duty_cycle_rating(self) -> '_322.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _322.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None

    @property
    def gear_duty_cycle_results_of_type_concept_gear_duty_cycle_rating(self) -> '_332.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _332.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults else None
