'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1934 import ClutchConnection
    from ._1935 import ClutchSocket
    from ._1936 import ConceptCouplingConnection
    from ._1937 import ConceptCouplingSocket
    from ._1938 import CouplingConnection
    from ._1939 import CouplingSocket
    from ._1940 import PartToPartShearCouplingConnection
    from ._1941 import PartToPartShearCouplingSocket
    from ._1942 import SpringDamperConnection
    from ._1943 import SpringDamperSocket
    from ._1944 import TorqueConverterConnection
    from ._1945 import TorqueConverterPumpSocket
    from ._1946 import TorqueConverterTurbineSocket
