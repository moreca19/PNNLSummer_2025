import gegede.builder
from utils import *
from gegede import Quantity as Q


class WorldBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.World): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.World = kwds

    def construct(self, geom):
        # get all the relevant stuff here
        print("runnning.......")
        globals.SetDerived()
        construct_materials(geom)
        construct_definitions(geom)

        
        worldBox = geom.shapes.Box(self.name,
                                   dx=Q('50000cm')/2 ,
                                   dy=Q('50000cm')/2,
                                   dz=Q('75000cm')/2)

       
        worldLV = geom.structure.Volume('vol'+self.name, material="Air", shape=worldBox)
        self.add_volume(worldLV)## add it to the registry

        Ibeams = self.get_builder("IBeams")
        placementsToPut = Ibeams.PlacementList
        for i in placementsToPut:
            worldLV.placements.append(i.name)

        Belts = self.get_builder("Belts")
        BeltPlacements = Belts.PlacementList
        for i in BeltPlacements:
            worldLV.placements.append(i.name)

        Cryostat = self.get_builder("Cryostat")
        CryostatPlacement = Cryostat.PlacementList
        for i in CryostatPlacement:
            worldLV.placements.append(i.name)

        shieldingFloors = self.get_builder("ShieldingFloors")
        floorPlacements = shieldingFloors.PlacementList
        for i in floorPlacements:
            worldLV.placements.append(i.name)

        ShieldinWalls = self.get_builder("ShieldingWalls")
        walls = ShieldinWalls.PlacementList
        for i in walls:
            worldLV.placements.append(i.name)

        Cavern = self.get_builder("Cavern")
        CavernPlacement = Cavern.PlacementList
        for i in CavernPlacement:
            worldLV.placements.append(i.name)
        
        return worldLV
