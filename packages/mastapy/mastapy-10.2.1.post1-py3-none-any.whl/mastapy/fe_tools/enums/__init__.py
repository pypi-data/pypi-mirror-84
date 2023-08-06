'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._974 import ElementPropertyClass
    from ._975 import MaterialPropertyClass
