# #!/usr/bin/env python
# '''
# World builder for DUNE FD-VD

#                                   |--> FieldCage
# World -> DetEnclosure -> Cryostat |--> TPC -> Wires
#                                   |--> Arapuca
#                                   |--> CathodeGrid
# '''

# import gegede.builder
# from utils import *

# class WorldBuilder(gegede.builder.Builder):
#     def configure(self, **kwds):
#         if not set(kwds).issubset(globals.World): # no unknown keywords
#             msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
#             raise ValueError(msg)

#         # The builder hierarchy takes care of all the configuration parameters
#         globals.World = kwds

#     def construct(self, geom):
#         # get all the relevant stuff here
#         globals.SetDerived()
#         construct_materials(geom)
#         construct_definitions(geom)

#         # create the world box
#         worldBox = geom.shapes.Box(self.name,
#                                    dx=0.5*globals.get("DetEncX")+globals.get("RockThickness"),
#                                    dy=0.5*globals.get("DetEncY")+globals.get("RockThickness"),
#                                    dz=0.5*globals.get("DetEncZ")+globals.get("RockThickness"))## this creates the world "box" whereteh detector will go in

#         # put it in the world volume
#         worldLV = geom.structure.Volume('vol'+self.name, material="DUSEL_Rock", shape=worldBox)## make taht box we created above a avtualy logical volume
#         self.add_volume(worldLV)## add it to the registry

#         # get the detector enclosure sub-builder
#         detenc = self.get_builder("DetEnclosure")## get the detenclose subbuiler, creates an instance of the class
#         detencLV = detenc.get_volume()## gets the colume that was created in DetEnclosure
        
        
#         # Ibeams = self.get_builder("IBeams")
#         # placementsToPut = Ibeams.PlacementList

#         # define where it goes inside the world volume
#         detenc_pos = geom.structure.Position('pos'+detenc.name,
#                                              x = globals.get("OriginXSet"),
#                                              y = globals.get("OriginYSet"),
#                                              z = globals.get("OriginZSet"))## postion of box
#         detenc_place = geom.structure.Placement('place'+detenc.name,
#                                                 volume = detencLV,
#                                                 pos = detenc_pos)## rotation and actual placement of box
        
#         # for i in placementsToPut:
#         #     worldLV.placements.append(i.name)

#         # place it inside the world volume
#         worldLV.placements.append(detenc_place.name) ## this add de detenclosure to the world volume("puts it inside")
#         return worldLV
###################################################################################################################

#!/usr/bin/env python
'''
World builder for DUNE FD-VD

                                  |--> FieldCage
World -> DetEnclosure -> Cryostat |--> TPC -> Wires
                                  |--> Arapuca
                                  |--> CathodeGrid
'''

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
        globals.SetDerived()
        construct_materials(geom)
        construct_definitions(geom)

        
        worldBox = geom.shapes.Box(self.name,
                                   dx=Q('50000cm')/2 ,
                                   dy=Q('50000cm')/2,
                                   dz=Q('75000cm')/2)

       
        worldLV = geom.structure.Volume('vol'+self.name, material="Air", shape=worldBox)
        print("about to print the name")
        print(self.name)
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

        ShieldinWalls = self.get_builder("ShieldingWalls")
        walls = ShieldinWalls.PlacementList
        for i in walls:
            worldLV.placements.append(i.name)

        Cavern = self.get_builder("Cavern")
        CavernPlacement = Cavern.PlacementList
        for i in CavernPlacement:
           worldLV.placements.append(i.name)

        return worldLV
