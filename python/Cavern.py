import gegede.builder
from gegede import Quantity as Q

from utils import *


#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
#Globals
#--------------------#


	
#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......




def make_volume(geom, material, shape, name='', aux=False):
    name_lv = name
    if name == '':
        name_lv = 'vol'+shape.name

    lv = geom.structure.Volume(name_lv,
                               material = material,
                               shape = shape
                               
                               )
    if lv == None:
         return print("logical volume failed to be created")
    else:
         return lv


class CavernBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.World): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.World = kwds

    def construct(self, geom):
        # get all the relevant stuff here
        globals.SetDerived()
        self.PlacementList = []

        detEnclosureBox = geom.shapes.Box('DetEnclosureBox',
					dx = Q('1980cm') /2,
					dy = Q('2315cm')/2,
					dz = Q('15060cm')/2)
        
        radioRockBox = geom.shapes.Box('RadioRockBox',
					dx = Q('2380cm')/2,
					dy = Q('2515cm')/2,
					dz = Q('15460cm')/2)
        
        detEnclosureArch = geom.shapes.Tubs('DetEnclosureArch',
					rmin = Q('0cm'),
					rmax = Q('1284cm'),
					dz = Q('15060cm')/2,
					sphi = Q('40.00000000011459deg'),
					dphi = Q('100deg'))
        
        concreteBox = geom.shapes.Box('ConcreteBox',
					dx = Q('1980cm')/2,
					dy = Q('27.49cm')/2,
					dz = Q('15060cm')/2)
        
        rockArch = geom.shapes.Tubs('RockArch',
					rmin = Q('0cm'),
					rmax = Q('1484cm'),
					dz = Q('15460cm')/2,
					sphi = Q('36.689342620533175deg'),
					dphi = Q('106.6213147592774deg'))
        
        DefaultRotation = geom.structure.Rotation('dr', x= "0deg", y= "0deg",z= "0deg")

        detEnclosureLArBoolAdd = geom.shapes.Boolean('DetEnclosureLArBoolAdd', type = 'union', 
						first = detEnclosureBox,
						second = detEnclosureArch,
						pos = geom.structure.Position('DetEnclosureLAr_ArchPos',
                                   x= Q('0cm'),
                                   y =Q('332.160709162cm'),
                                   z=Q('0cm')))
        
        rockAddition = geom.shapes.Boolean('RockAddition', type = 'union', 
						first = radioRockBox,
						second = rockArch,
						pos = geom.structure.Position('posTube',
                                   x= Q('0cm'),
                                   y =Q('370.84561412cm'),
                                   z=Q('0cm')))
        
        firstSub = geom.shapes.Boolean('FirstSub', type = 'subtraction', 
						first = rockAddition, 
						second = detEnclosureLArBoolAdd,
						pos = geom.structure.Position('posFirstSub', x="0cm", y="100cm", z="0cm"), 
						rot = DefaultRotation)
        
        volRadioRockShell = make_volume(geom, 'DUSEL_Rock', firstSub, 'VolRadioRockShell', aux = True)

        volRadioRockShellPlacement = geom.structure.Placement('RadioRockShellPLacement',
                                                               rot = DefaultRotation,
                                                               volume = volRadioRockShell,
                                                                pos = geom.structure.Position('RadioRockShellPositionInPlacement',
                                                                x = "0cm",
                                                                y =  "0cm",
                                                                z = "0cm"),
                                                            	)
        self.PlacementList.append(volRadioRockShellPlacement)

        VolConcrete = make_volume(geom, 'Concrete', concreteBox, 'volConcrete', aux = True )

        volConcretePlacement = geom.structure.Placement('ConcretePLacement',
                                                               rot = DefaultRotation,
                                                               volume = VolConcrete,
                                                                pos = geom.structure.Position('ConcretePositionInPlacement',
                                                                x = "0cm",
                                                                y =  "-1043.53cm",
                                                                z = "0cm"),
                                                            	)
        self.PlacementList.append(volConcretePlacement)

        



