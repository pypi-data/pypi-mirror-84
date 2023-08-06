'''_2244.py

CompoundSingleMeshWhineAnalysisAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _2022, _2023, _2026, _2028,
    _2029, _2030, _2033, _2034,
    _2037, _2038, _2021, _2039,
    _2042, _2046, _2047, _2048,
    _2050, _2052, _2053, _2055,
    _2056, _2058, _2060, _2061,
    _2062
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5581, _5582, _5587, _5598,
    _5599, _5604, _5615, _5626,
    _5627, _5631, _5586, _5635,
    _5639, _5650, _5651, _5652,
    _5653, _5654, _5660, _5661,
    _5662, _5667, _5671, _5694,
    _5695, _5668, _5608, _5610,
    _5628, _5630, _5583, _5585,
    _5590, _5592, _5593, _5594,
    _5595, _5597, _5611, _5613,
    _5622, _5624, _5625, _5632,
    _5634, _5636, _5638, _5641,
    _5643, _5644, _5646, _5647,
    _5649, _5659, _5672, _5674,
    _5678, _5680, _5681, _5683,
    _5684, _5685, _5696, _5698,
    _5699, _5701, _5655, _5657,
    _5589, _5600, _5602, _5605,
    _5607, _5616, _5618, _5620,
    _5621, _5663, _5669, _5665,
    _5664, _5675, _5677, _5686,
    _5687, _5688, _5689, _5690,
    _5692, _5693, _5619, _5588,
    _5603, _5614, _5640, _5658,
    _5666, _5670, _5591, _5609,
    _5629, _5679, _5596, _5612,
    _5584, _5623, _5637, _5642,
    _5645, _5648, _5673, _5682,
    _5697, _5700, _5633, _5656,
    _5601, _5606, _5617, _5676,
    _5691
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2065
from mastapy.system_model.part_model.gears import (
    _2103, _2104, _2110, _2111,
    _2095, _2096, _2097, _2098,
    _2099, _2100, _2101, _2102,
    _2105, _2106, _2107, _2108,
    _2109, _2112, _2114, _2116,
    _2117, _2118, _2119, _2120,
    _2121, _2122, _2123, _2124,
    _2125, _2126, _2127, _2128,
    _2129, _2130, _2131, _2132,
    _2133, _2134, _2135, _2136
)
from mastapy.system_model.part_model.couplings import (
    _2165, _2166, _2154, _2156,
    _2157, _2159, _2160, _2161,
    _2162, _2163, _2164, _2167,
    _2175, _2173, _2174, _2176,
    _2177, _2178, _2180, _2181,
    _2182, _2183, _2184, _2186
)
from mastapy.system_model.connections_and_sockets import (
    _1877, _1872, _1873, _1876,
    _1885, _1888, _1892, _1896
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1902, _1906, _1912, _1926,
    _1904, _1908, _1900, _1910,
    _1916, _1919, _1920, _1921,
    _1924, _1928, _1930, _1932,
    _1914
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1940, _1934, _1936, _1938,
    _1942, _1944
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2195

_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_IMPORTED_FE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ImportedFEComponent')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSingleMeshWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSingleMeshWhineAnalysisAnalysis',)


class CompoundSingleMeshWhineAnalysisAnalysis(_2195.CompoundAnalysis):
    '''CompoundSingleMeshWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSingleMeshWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_abstract_assembly(self, design_entity: '_2022.AbstractAssembly') -> 'Iterable[_5581.AbstractAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5581.AbstractAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2023.AbstractShaftOrHousing') -> 'Iterable[_5582.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None), constructor.new(_5582.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis))

    def results_for_bearing(self, design_entity: '_2026.Bearing') -> 'Iterable[_5587.BearingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BearingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None), constructor.new(_5587.BearingCompoundSingleMeshWhineAnalysis))

    def results_for_bolt(self, design_entity: '_2028.Bolt') -> 'Iterable[_5598.BoltCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None), constructor.new(_5598.BoltCompoundSingleMeshWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_2029.BoltedJoint') -> 'Iterable[_5599.BoltedJointCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltedJointCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None), constructor.new(_5599.BoltedJointCompoundSingleMeshWhineAnalysis))

    def results_for_component(self, design_entity: '_2030.Component') -> 'Iterable[_5604.ComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5604.ComponentCompoundSingleMeshWhineAnalysis))

    def results_for_connector(self, design_entity: '_2033.Connector') -> 'Iterable[_5615.ConnectorCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectorCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None), constructor.new(_5615.ConnectorCompoundSingleMeshWhineAnalysis))

    def results_for_datum(self, design_entity: '_2034.Datum') -> 'Iterable[_5626.DatumCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.DatumCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None), constructor.new(_5626.DatumCompoundSingleMeshWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_2037.ExternalCADModel') -> 'Iterable[_5627.ExternalCADModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ExternalCADModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_5627.ExternalCADModelCompoundSingleMeshWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_2038.FlexiblePinAssembly') -> 'Iterable[_5631.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5631.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_assembly(self, design_entity: '_2021.Assembly') -> 'Iterable[_5586.AssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5586.AssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_2039.GuideDxfModel') -> 'Iterable[_5635.GuideDxfModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GuideDxfModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_5635.GuideDxfModelCompoundSingleMeshWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2042.ImportedFEComponent') -> 'Iterable[_5639.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ImportedFEComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_IMPORTED_FE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5639.ImportedFEComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_2046.MassDisc') -> 'Iterable[_5650.MassDiscCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MassDiscCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None), constructor.new(_5650.MassDiscCompoundSingleMeshWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_2047.MeasurementComponent') -> 'Iterable[_5651.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MeasurementComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5651.MeasurementComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_2048.MountableComponent') -> 'Iterable[_5652.MountableComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MountableComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5652.MountableComponentCompoundSingleMeshWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_2050.OilSeal') -> 'Iterable[_5653.OilSealCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.OilSealCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None), constructor.new(_5653.OilSealCompoundSingleMeshWhineAnalysis))

    def results_for_part(self, design_entity: '_2052.Part') -> 'Iterable[_5654.PartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None), constructor.new(_5654.PartCompoundSingleMeshWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2053.PlanetCarrier') -> 'Iterable[_5660.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetCarrierCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None), constructor.new(_5660.PlanetCarrierCompoundSingleMeshWhineAnalysis))

    def results_for_point_load(self, design_entity: '_2055.PointLoad') -> 'Iterable[_5661.PointLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PointLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_5661.PointLoadCompoundSingleMeshWhineAnalysis))

    def results_for_power_load(self, design_entity: '_2056.PowerLoad') -> 'Iterable[_5662.PowerLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PowerLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_5662.PowerLoadCompoundSingleMeshWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_2058.RootAssembly') -> 'Iterable[_5667.RootAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RootAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5667.RootAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2060.SpecialisedAssembly') -> 'Iterable[_5671.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5671.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2061.UnbalancedMass') -> 'Iterable[_5694.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.UnbalancedMassCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None), constructor.new(_5694.UnbalancedMassCompoundSingleMeshWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_2062.VirtualComponent') -> 'Iterable[_5695.VirtualComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.VirtualComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5695.VirtualComponentCompoundSingleMeshWhineAnalysis))

    def results_for_shaft(self, design_entity: '_2065.Shaft') -> 'Iterable[_5668.ShaftCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_5668.ShaftCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_2103.ConceptGear') -> 'Iterable[_5608.ConceptGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5608.ConceptGearCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2104.ConceptGearSet') -> 'Iterable[_5610.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5610.ConceptGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_2110.FaceGear') -> 'Iterable[_5628.FaceGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5628.FaceGearCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2111.FaceGearSet') -> 'Iterable[_5630.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5630.FaceGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2095.AGMAGleasonConicalGear') -> 'Iterable[_5583.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5583.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2096.AGMAGleasonConicalGearSet') -> 'Iterable[_5585.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5585.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2097.BevelDifferentialGear') -> 'Iterable[_5590.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5590.BevelDifferentialGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2098.BevelDifferentialGearSet') -> 'Iterable[_5592.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5592.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2099.BevelDifferentialPlanetGear') -> 'Iterable[_5593.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5593.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2100.BevelDifferentialSunGear') -> 'Iterable[_5594.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5594.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2101.BevelGear') -> 'Iterable[_5595.BevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5595.BevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2102.BevelGearSet') -> 'Iterable[_5597.BevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5597.BevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_2105.ConicalGear') -> 'Iterable[_5611.ConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5611.ConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2106.ConicalGearSet') -> 'Iterable[_5613.ConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5613.ConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2107.CylindricalGear') -> 'Iterable[_5622.CylindricalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5622.CylindricalGearCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2108.CylindricalGearSet') -> 'Iterable[_5624.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5624.CylindricalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2109.CylindricalPlanetGear') -> 'Iterable[_5625.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5625.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_gear(self, design_entity: '_2112.Gear') -> 'Iterable[_5632.GearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5632.GearCompoundSingleMeshWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_2114.GearSet') -> 'Iterable[_5634.GearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5634.GearSetCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2116.HypoidGear') -> 'Iterable[_5636.HypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5636.HypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2117.HypoidGearSet') -> 'Iterable[_5638.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5638.HypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2118.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5641.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5641.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2119.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5643.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5643.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2120.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5644.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5644.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2121.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5646.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5646.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2122.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5647.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5647.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2123.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5649.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5649.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2124.PlanetaryGearSet') -> 'Iterable[_5659.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5659.PlanetaryGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2125.SpiralBevelGear') -> 'Iterable[_5672.SpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5672.SpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2126.SpiralBevelGearSet') -> 'Iterable[_5674.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5674.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2127.StraightBevelDiffGear') -> 'Iterable[_5678.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5678.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2128.StraightBevelDiffGearSet') -> 'Iterable[_5680.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5680.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2129.StraightBevelGear') -> 'Iterable[_5681.StraightBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5681.StraightBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2130.StraightBevelGearSet') -> 'Iterable[_5683.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5683.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2131.StraightBevelPlanetGear') -> 'Iterable[_5684.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5684.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2132.StraightBevelSunGear') -> 'Iterable[_5685.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5685.StraightBevelSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_2133.WormGear') -> 'Iterable[_5696.WormGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5696.WormGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2134.WormGearSet') -> 'Iterable[_5698.WormGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5698.WormGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2135.ZerolBevelGear') -> 'Iterable[_5699.ZerolBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5699.ZerolBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2136.ZerolBevelGearSet') -> 'Iterable[_5701.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5701.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2165.PartToPartShearCoupling') -> 'Iterable[_5655.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5655.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2166.PartToPartShearCouplingHalf') -> 'Iterable[_5657.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5657.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_2154.BeltDrive') -> 'Iterable[_5589.BeltDriveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltDriveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None), constructor.new(_5589.BeltDriveCompoundSingleMeshWhineAnalysis))

    def results_for_clutch(self, design_entity: '_2156.Clutch') -> 'Iterable[_5600.ClutchCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None), constructor.new(_5600.ClutchCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2157.ClutchHalf') -> 'Iterable[_5602.ClutchHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5602.ClutchHalfCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2159.ConceptCoupling') -> 'Iterable[_5605.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5605.ConceptCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2160.ConceptCouplingHalf') -> 'Iterable[_5607.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5607.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_coupling(self, design_entity: '_2161.Coupling') -> 'Iterable[_5616.CouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5616.CouplingCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_2162.CouplingHalf') -> 'Iterable[_5618.CouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5618.CouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_cvt(self, design_entity: '_2163.CVT') -> 'Iterable[_5620.CVTCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None), constructor.new(_5620.CVTCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2164.CVTPulley') -> 'Iterable[_5621.CVTPulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTPulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_5621.CVTPulleyCompoundSingleMeshWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2167.Pulley') -> 'Iterable[_5663.PulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_5663.PulleyCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2175.ShaftHubConnection') -> 'Iterable[_5669.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5669.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2173.RollingRing') -> 'Iterable[_5665.RollingRingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None), constructor.new(_5665.RollingRingCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2174.RollingRingAssembly') -> 'Iterable[_5664.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5664.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_2176.SpringDamper') -> 'Iterable[_5675.SpringDamperCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None), constructor.new(_5675.SpringDamperCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2177.SpringDamperHalf') -> 'Iterable[_5677.SpringDamperHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5677.SpringDamperHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_2178.Synchroniser') -> 'Iterable[_5686.SynchroniserCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None), constructor.new(_5686.SynchroniserCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2180.SynchroniserHalf') -> 'Iterable[_5687.SynchroniserHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5687.SynchroniserHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2181.SynchroniserPart') -> 'Iterable[_5688.SynchroniserPartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserPartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None), constructor.new(_5688.SynchroniserPartCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2182.SynchroniserSleeve') -> 'Iterable[_5689.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None), constructor.new(_5689.SynchroniserSleeveCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_2183.TorqueConverter') -> 'Iterable[_5690.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None), constructor.new(_5690.TorqueConverterCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2184.TorqueConverterPump') -> 'Iterable[_5692.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None), constructor.new(_5692.TorqueConverterPumpCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2186.TorqueConverterTurbine') -> 'Iterable[_5693.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None), constructor.new(_5693.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1877.CVTBeltConnection') -> 'Iterable[_5619.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5619.CVTBeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1872.BeltConnection') -> 'Iterable[_5588.BeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5588.BeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1873.CoaxialConnection') -> 'Iterable[_5603.CoaxialConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CoaxialConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5603.CoaxialConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_connection(self, design_entity: '_1876.Connection') -> 'Iterable[_5614.ConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5614.ConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1885.InterMountableComponentConnection') -> 'Iterable[_5640.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5640.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1888.PlanetaryConnection') -> 'Iterable[_5658.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5658.PlanetaryConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1892.RollingRingConnection') -> 'Iterable[_5666.RollingRingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5666.RollingRingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1896.ShaftToMountableComponentConnection') -> 'Iterable[_5670.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5670.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1902.BevelDifferentialGearMesh') -> 'Iterable[_5591.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5591.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1906.ConceptGearMesh') -> 'Iterable[_5609.ConceptGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5609.ConceptGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1912.FaceGearMesh') -> 'Iterable[_5629.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5629.FaceGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1926.StraightBevelDiffGearMesh') -> 'Iterable[_5679.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5679.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1904.BevelGearMesh') -> 'Iterable[_5596.BevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5596.BevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1908.ConicalGearMesh') -> 'Iterable[_5612.ConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5612.ConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1900.AGMAGleasonConicalGearMesh') -> 'Iterable[_5584.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5584.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1910.CylindricalGearMesh') -> 'Iterable[_5623.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5623.CylindricalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1916.HypoidGearMesh') -> 'Iterable[_5637.HypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5637.HypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1919.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5642.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5642.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1920.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5645.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5645.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1921.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5648.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5648.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1924.SpiralBevelGearMesh') -> 'Iterable[_5673.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5673.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1928.StraightBevelGearMesh') -> 'Iterable[_5682.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5682.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1930.WormGearMesh') -> 'Iterable[_5697.WormGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5697.WormGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1932.ZerolBevelGearMesh') -> 'Iterable[_5700.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5700.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1914.GearMesh') -> 'Iterable[_5633.GearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5633.GearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1940.PartToPartShearCouplingConnection') -> 'Iterable[_5656.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5656.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1934.ClutchConnection') -> 'Iterable[_5601.ClutchConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5601.ClutchConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1936.ConceptCouplingConnection') -> 'Iterable[_5606.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5606.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1938.CouplingConnection') -> 'Iterable[_5617.CouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5617.CouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1942.SpringDamperConnection') -> 'Iterable[_5676.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5676.SpringDamperConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1944.TorqueConverterConnection') -> 'Iterable[_5691.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5691.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis))
