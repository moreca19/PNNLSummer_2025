import gegede.builder
from gegede import Quantity as Q

from utils import *


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
        
        concreteBox = geom.shapes.Box('ConcreteBox',
					dx = Q('1980cm')/2,
					dy = Q('27.49cm')/2,
					dz = Q('15060cm')/2)
        
        groutBox = geom.shapes.Box('GroutBox',
					dx = Q('1980cm')/2,
					dy = Q('2.54cm')/2,
					dz = Q('15060cm')/2)
        
        detEnclosureArch = geom.shapes.Tubs('DetEnclosureArch',
					rmin = Q('0cm'),
					rmax = Q('1284cm'),
					dz = Q('15060cm')/2,
					sphi = Q('40.00000000011459deg'),
					dphi = Q('100deg'))
        
        
        
        rockArch = geom.shapes.Tubs('RockArch',
					rmin = Q('0cm'),
					rmax = Q('1484cm'),
					dz = Q('15460cm')/2,
					sphi = Q('36.689342620533175deg'),
					dphi = Q('106.6213147592774deg'))
        
        DefaultRotation = geom.structure.Rotation('dr', x= "0deg", y= "0deg",z= "0deg")
        DefaultRotation2 = geom.structure.Rotation('dr2', x= "0deg", y= "0deg",z= "0deg")

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
						rot = DefaultRotation2)
        
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

        ##__ConcreteVolume__##

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

        ##__GorutVolume__##

        VolGrout = make_volume(geom, 'Concrete', groutBox, 'volGrout', aux=True)

        volGroutPlacement = geom.structure.Placement('GroutPLacement',
                                                               rot = DefaultRotation,
                                                               volume = VolGrout,
                                                                pos = geom.structure.Position('GroutPositionInPlacement',
                                                                x = "0cm",
                                                                y =  "-1028.29cm",
                                                                z = "0cm"),
                                                            	)
        self.PlacementList.append(volGroutPlacement)


        ##__ShotBoX, defining all variable down here because, proccess is longer, dont want it to be confusing__##



        concSubBox = geom.shapes.Box('oncSubBox',
					dx = Q('1980cm')/2,
					dy = Q('30.48cm')/2,
					dz = Q('15060cm')/2) ## this box will be used in the last subtraction
        
        shotInnerBox = geom.shapes.Box('ShotInnerBox',
					dx = Q('1959.68cm')/2,
					dy = Q('2315.0cm')/2,
					dz = Q('15039.68cm')/2) ## this box will be used in the first subtraction
        
        shotOuterBox = geom.shapes.Box('ShotOuterBox',
					dx = Q('1980.68cm')/2,
					dy = Q('2315.0cm')/2,
					dz = Q('15060.0cm')/2) #box for union
        
        shotOuterrArch = geom.shapes.Tubs('ShotOuterArch',
					rmin = Q('0cm'),
					rmax = Q('1284cm'),
					dz = Q('15060cm')/2,
					sphi = Q('40.00000000011459deg'),
					dphi = Q('100deg')) #arch for the union
        
        shotInnerArch = geom.shapes.Tubs('ShotInnerArch',
					rmin = Q('0cm'),
					rmax = Q('1273.84cm'),
					dz = Q('15039.68cm')/2,
					sphi = Q('39.71773626968189deg'),
					dphi = Q('100.564527460865deg'))
        
        shotOuterBoolAdd = geom.shapes.Boolean('ShotOuterBoolAdd', type = 'union', 
						first = shotOuterBox,
                        
						second = shotOuterrArch,
						pos = geom.structure.Position('shotOuterArchPos',
                                   x= Q('0cm'),
                                   y =Q('332.160709162cm'),
                                   z=Q('0cm'))) # the union needed for first sub
        
        shotInnerBoxSub = geom.shapes.Boolean('ShotInnerBoxSub', type = 'subtraction', 
						first = shotOuterBoolAdd, 
						second = shotInnerBox,
						pos = geom.structure.Position('posInnerBoxSub', x="0cm", y="0cm", z="0cm"), 
						rot = DefaultRotation2)
        
        shotInnerArchSub = geom.shapes.Boolean('ShotInnerArchSub', type = 'subtraction', 
						first = shotInnerBoxSub, 
						second = shotInnerArch,
						pos = geom.structure.Position('posInnerArchSub', x="0cm", y="338.428648695cm", z="0cm"), 
						rot = DefaultRotation2)
        
        shotOuterMinusBox = geom.shapes.Boolean('ShotOuterMinusBox', type = 'subtraction', 
						first = shotInnerArchSub, 
						second = concSubBox,
						pos = geom.structure.Position('posOuterMinusBoxSub', x="0cm", y="-1142.26cm", z="0cm"), 
						rot = DefaultRotation2)
        
        volShotBox = make_volume(geom, 'Concrete', shotOuterMinusBox, 'VolShotBox', aux = True) ## still need to fix the material its made off.

        volShotBoxPlacement = geom.structure.Placement('ShotBoxPLacement',
                                                               rot = DefaultRotation,
                                                               volume = volShotBox,
                                                                pos = geom.structure.Position('ShotBoxPositionInPlacement',
                                                                x = "0cm",
                                                                y =  "100cm",
                                                                z = "0cm"),
                                                            	)
        self.PlacementList.append(volShotBoxPlacement)

        




        

        

        



