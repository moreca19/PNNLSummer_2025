import gegede.builder
from gegede import Quantity as Q
import ROOT

from utils import *


#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
#Globals
#--------------------#
fht = Q('841.1cm')
fst = Q('896.4cm')
fSpacing = Q('157.86cm')
fIFlangeWidth = Q('0.42cm')
fIFlangeThick = Q('4cm')
fIFlangeWaist = Q('2.2cm')
fIFlangeHeight = Q('110.8cm')
fIPortSpacing = Q('400cm')


fITopLength = Q('1783.2cm') + fIFlangeHeight
fISideLength = Q('1673.2cm') + fIFlangeHeight
fIPortHoleRad = Q('40cm')	
	
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


class ShieldingWallsBuilder(gegede.builder.Builder):
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


        eps = Q('21.5cm')
        ht = fht
        st = fst + Q('3.1cm')

        yTopHole = -((fISideLength / 2) +(fIFlangeHeight / 2) - 590.0 / 1000.0 - (4.0-1.0) * fIPortSpacing +(9 * fIPortHoleRad)) / 2
        yBotHole = -((fISideLength / 2) +(fIFlangeHeight / 2) - 590.0 / 1000.0 - (0.0-1.0) * fIPortSpacing +(9 * fIPortHoleRad)) / 2
        y1HoleUp = -((fISideLength / 2) +(fIFlangeHeight / 2) - 590.0 / 1000.0 - (2.0-1.0) * fIPortSpacing +(9 * fIPortHoleRad)) / 2

        yTop = (ht-eps)

        BlockWidth = fSpacing-fIFlangeWaist - 0.001 -0.050
        BlockHeight = fIPortSpacing - 0.050
        BlockHeightTop = BlockHeight*0.63
        BlockHeightBot = BlockHeight*0.15

        fBlockThickness = Q('40cm')

        ShieldBlock = geom.shapes.Box('ShieldBlock',
					dx = (fBlockThickness/2),
					dy = (BlockHeight /2),
					dz = (BlockWidth/2))
        
        ShieldBlockTop = geom.shapes.Box('ShieldBlockTop',
					dx = (fBlockThickness/2),
					dy = (BlockHeightTop /2),
					dz = (BlockWidth/2))
        
        ShieldBlockBot = geom.shapes.Box('ShieldBlockBot',
					dx = (fBlockThickness/2),
					dy = (BlockHeightBot /2),
					dz = (BlockWidth/2))
        
        fcRotation = geom.structure.Rotation('fcBelt', x= "0deg", y= "0deg",z= "90deg")
        fc2Rotation = geom.structure.Rotation('fc2Belt',x= "0deg", y= "90deg",z= "0deg")
        fc3Rotation = geom.structure.Rotation('fc3Belt', x= "90deg", y= "0deg",z= "90deg")

        ShieldBlockLog = make_volume(geom, 'AirSteelMixture', ShieldBlock, 'ShieldBlockLog', aux = True) 