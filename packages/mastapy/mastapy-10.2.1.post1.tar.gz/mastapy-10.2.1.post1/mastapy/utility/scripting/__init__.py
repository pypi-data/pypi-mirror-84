'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1282 import ScriptingSetup
    from ._1283 import UserDefinedPropertyKey
    from ._1284 import UserSpecifiedData
