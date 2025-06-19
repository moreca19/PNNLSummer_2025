import gegede.builder
from gegede import Quantity as Q
import ROOT
from ROOT import kBlue
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


fColdSkinThickness = Q('0.18cm')
Offset = Q('10cm')
fCryostat_x = Q('1480cm')
fCryostat_y = Q('1300cm')
fCryostat_z = Q('6000cm')



	
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

class CryostatBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        
        if not set(kwds).issubset(globals.Cryostat): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.Cryostat = kwds

    def construct(self, geom):
        globals.SetDerived()
        self.PlacementList = []

        fSolidCryostat = geom.shapes.Box('Cryostat',
					dx = fCryostat_x/2 + Offset,
					dy = fCryostat_y/2 + Offset,
					dz = fCryostat_z/2+Offset)
        ShellOut = geom.shapes.Box('ShellOut',
					dx = fCryostat_x/2+fColdSkinThickness + Offset,
					dy = fCryostat_y/2 +fColdSkinThickness+ Offset,
					dz = fCryostat_z/2+fColdSkinThickness+Offset)
        
        fShell = geom.shapes.Boolean('fShell', type = 'subtraction', 
						first = ShellOut, 
						second = fSolidCryostat,
        )              

        fLogicShell = make_volume(geom, 'AirSteelMixture', fShell, "fShellLog", aux=True)        
        


        fPhysShell = geom.structure.Placement('fPhysShell',
                                                                
                                                                pos = geom.structure.Position('fPhysShellPlacement',
                                                                x = "0cm",
                                                                y =  "0cm",
                                                                z = "0cm"),
                                                            	volume = fLogicShell
                                                                
                                                                )  
    
        self.PlacementList.append(fPhysShell)
      





