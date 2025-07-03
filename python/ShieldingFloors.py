import gegede.builder
from gegede import Quantity as Q
from gegede import geometry as geom

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
'''
for ii in range(19):
    for jj in range(-5, 5):
        box_name = f'ShieldingFloor_{jj}_{ii}'
        box_shape = geom.shapes.Box(box_name, dx, dy, dz)

        box_lv = geom.structure.Volume(box_name + '_lv', material=geom.get_material("Water"), shape=box_shape)
        box_lv.params.append(("color", "blue"))

        xpos = -ht + eps
        ypos = (jj + 0.5) * zbsp
        zpos = zpl

        pos_name = f'{box_name}_pos'
        placement_name = f'{box_name}_placement'

        placement = geom.structure.Placement(
            name=f'ShieldingFloor_placement',
            volume=box_lv,
            pos=geom.structure.Position(f'ShileldingFloor_pos', x=xpos, y=ypos, z=zpos)
        )

        self.PlacementList.append(placement)

def build(self, **kwargs):
    print(" ShieldingFloors.build() called")

    dx, dy, dz = Q("5cm"), Q("5cm"), Q("5cm")
    box = self.shapes.Box("TestBox", dx, dy, dz)
    lv = self.structure.Volume("TestBox_lv", material=self.get_material("Air"), shape=box)
    lv.params.append(("Color", "red"))

    pos = self.structure.Position("TestBox_pos", Q("0cm"), Q("0cm"), Q("0cm"))
    placement = self.structure.Placement("TestBox_placement", volume=lv, pos=pos)

    self.PlacementList.append(placement)
'''
