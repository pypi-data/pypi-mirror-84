'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2015 import DesignResults
    from ._2016 import ImportedFEResults
    from ._2017 import ImportedFEVersionComparer
    from ._2018 import LoadCaseResults
    from ._2019 import LoadCasesToRun
    from ._2020 import NodeComparisonResult
