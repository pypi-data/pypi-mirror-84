﻿'''_4821.py

ModalAnalysisOptions
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4797
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisOptions',)


class ModalAnalysisOptions(_0.APIBase):
    '''ModalAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_modes(self) -> 'int':
        '''int: 'NumberOfModes' is the original name of this property.'''

        return self.wrapped.NumberOfModes

    @number_of_modes.setter
    def number_of_modes(self, value: 'int'):
        self.wrapped.NumberOfModes = int(value) if value else 0

    @property
    def frequency_response_options_for_reports(self) -> '_4797.FrequencyResponseAnalysisOptions':
        '''FrequencyResponseAnalysisOptions: 'FrequencyResponseOptionsForReports' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4797.FrequencyResponseAnalysisOptions)(self.wrapped.FrequencyResponseOptionsForReports) if self.wrapped.FrequencyResponseOptionsForReports else None
