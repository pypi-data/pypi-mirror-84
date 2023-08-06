'''_1305.py

CustomReportItemContainer
'''


from mastapy.utility.report import _1304
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_ITEM_CONTAINER = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportItemContainer')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportItemContainer',)


class CustomReportItemContainer(_1304.CustomReportItem):
    '''CustomReportItemContainer

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_REPORT_ITEM_CONTAINER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomReportItemContainer.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
