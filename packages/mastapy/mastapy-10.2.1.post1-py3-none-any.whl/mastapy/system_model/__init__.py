'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1832 import Design
    from ._1833 import ComponentDampingOption
    from ._1834 import ConceptCouplingSpeedRatioSpecificationMethod
    from ._1835 import DesignEntity
    from ._1836 import DesignEntityId
    from ._1837 import DutyCycleImporter
    from ._1838 import DutyCycleImporterDesignEntityMatch
    from ._1839 import ExternalFullFELoader
    from ._1840 import HypoidWindUpRemovalMethod
    from ._1841 import IncludeDutyCycleOption
    from ._1842 import MemorySummary
    from ._1843 import MeshStiffnessModel
    from ._1844 import PowerLoadDragTorqueSpecificationMethod
    from ._1845 import PowerLoadInputTorqueSpecificationMethod
    from ._1846 import PowerLoadPIDControlSpeedInputType
    from ._1847 import PowerLoadType
    from ._1848 import RelativeComponentAlignment
    from ._1849 import RelativeOffsetOption
    from ._1850 import SystemReporting
    from ._1851 import TransmissionTemperatureSet
