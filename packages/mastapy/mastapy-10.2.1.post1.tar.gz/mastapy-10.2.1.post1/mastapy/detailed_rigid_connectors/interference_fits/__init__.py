'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1032 import AssemblyMethods
    from ._1033 import CalculationMethods
    from ._1034 import InterferenceFitDesign
    from ._1035 import InterferenceFitHalfDesign
    from ._1036 import StressRegions
    from ._1037 import Table4JointInterfaceTypes
