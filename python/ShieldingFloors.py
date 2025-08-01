import gegede.builder
from gegede import Quantity as Q

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

BlockThickness = Q('0.40m')

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


class ShieldingFloorsBuilder(gegede.builder.Builder):
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
        zbsp = fSpacing
        BlockWidth = fSpacing-fIFlangeWaist-Q('0.001m') - Q('0.050m')
        box_shape = geom.shapes.Box('box_name', dy=(zbsp-Q('0.050m'))/2, dx=(BlockThickness/2.0), dz=(BlockWidth/2))
        boxshapevolume = make_volume(geom,'Water', box_shape, 'boxshapeVol', aux=True)
        #pos2=geom.structure.Position('Test2', x="100cm", y="500cm", z="6000cm")
        #boxshapevolumeplacement = geom.structure.Placement('Test',volume = boxshapevolume, pos=pos2)
        #self.PlacementList.append(boxshapevolumeplacement)

        eps = Q('21.5cm')
        zbsp = fSpacing
        zpl=zbsp/2
        for ii in range(20):
                for jj in range(-5, 6):
                        box_name = f'ShieldingFloor_{jj}_{ii}'

                        #box_lv = geom.structure.Volume(box_name + '_lv', material=geom.get_material("Water"), shape=box_shape)
                        #box_lv.params.append(("color", "blue"))

                        xpos = -fht + eps
                        ypos = (jj) * zbsp
                        zpos = zpl

                        #pos_name = f'ShieldingFloor_pos'
                        #placement_name = f'ShieldingFloor_{jj}_{ii}_placement'

                        placement = geom.structure.Placement(
                                f'ShieldingFloor_{jj}_{ii}',
                                volume = boxshapevolume, 
			        pos = geom.structure.Position(f'ShieldingFloor_{jj}_{ii}_position', x=xpos, y=ypos, z=zpos)
			)
                        self.PlacementList.append(placement)
                zpl+=zbsp

        zpl=-zbsp/2
        for ii in range(0, -20, -1):
                for jj in range(-5, 6): 
                        box_name = f'ShieldingFloor_{jj}_{ii}'

                        #box_lv = geom.structure.Volume(box_name + '_lv', material=geom.get_material("Water"), shape=box_shape)
                        #box_lv.params.append(("color", "blue"))

                        xpos = -fht + eps
                        ypos = (jj) * zbsp
                        zpos = zpl

                        #pos_name = f'ShieldingFloor_pos'
                        #placement_name = f'ShieldingFloor2_{jj}_{ii}_placement'
                               
                        placement = geom.structure.Placement(
                                f'ShieldingFloor2_{jj}_{ii}',
                                volume = boxshapevolume,
                                pos = geom.structure.Position(f'ShieldingFloor2_{jj}_{ii}_position', x=xpos, y=ypos, z=zpos)
                        )
                        self.PlacementList.append(placement)
                zpl-=zbsp

