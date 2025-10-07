import gegede.builder
from gegede import Quantity as Q
from utils import *
from MyNewGlobals import *

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
        
        ###this is the start of Cryostat logical volume ###
        fSolidCryostat = geom.shapes.Box('Cryostat',
					dy = fCryostat_x/2 + Offset,
					dx = fCryostat_y/2 + Offset,
					dz = fCryostat_z/2+Offset)
        ShellOut = geom.shapes.Box('ShellOut',
					dy = fCryostat_x/2+fColdSkinThickness + Offset,
					dx = fCryostat_y/2 +fColdSkinThickness+ Offset,
					dz = fCryostat_z/2+fColdSkinThickness+Offset)
        
        fShell = geom.shapes.Boolean('fShell', type = 'subtraction', 
						first = ShellOut, 
						second = fSolidCryostat,
        )              

        fLogicShell = make_volume(geom, 'fDuneSteel', fShell, "fShellLog", aux=True) 
        



        fPhysShell = geom.structure.Placement('fPhysShell',
                                                                
                                            pos = geom.structure.Position('fPhysShellPlacement',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = fLogicShell
                                                                
                                            )  
    
        self.PlacementList.append(fPhysShell)


        ###box full of liquid argon inside cryostat
        LarBox = geom.shapes.Box('LArBox',
					dy = fCryostat_x/2 - fColdSkinThickness*2 + Offset,
					dx = fCryostat_y/2 - fColdSkinThickness*2 + Offset,
					dz = fCryostat_z/2 - fColdSkinThickness*2 +Offset)
        
        LArBoxLog = make_volume(geom, "G4_lAr", LarBox, "LArBoxLogical", aux=True)

        LArBoxPlacement = geom.structure.Placement('LArBoxPlacement',
                                                                
                                            pos = geom.structure.Position('LArBoxPosition',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = LArBoxLog
                                                                
                                            )  
    
        self.PlacementList.append(LArBoxPlacement)



      
        ###this is the start of foam logical volume###
        sOutShield = geom.shapes.Box('InShield',
					dy = fCryostat_x/2 + fShieldThickness + fColdSkinThickness + Offset,
					dx = fCryostat_y/2 + fShieldThickness + fColdSkinThickness + Offset,
					dz = fCryostat_z/2 + fShieldThickness + fColdSkinThickness + Offset)
        
        sShield = geom.shapes.Boolean('Foam', type = 'subtraction', 
						first = sOutShield, 
						second = ShellOut)
        fLogicShield = make_volume(geom,"Foam",sShield,"FoamLog", aux=True) 
        
        FoamPla = geom.structure.Placement('FoamPlacement',
                                                                
                                            pos = geom.structure.Position('FoamPosition',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = fLogicShield
                                                                
                                            ) 
        
        self.PlacementList.append(FoamPla)
        
        ###this is start of wood logical volume###
        sOutWood = geom.shapes.Box('InWood',
					dy = fCryostat_x/2 + fWoodThickness + fShieldThickness+ fColdSkinThickness + Offset,
					dx = fCryostat_y/2 + fWoodThickness +fShieldThickness+ fColdSkinThickness + Offset,
					dz = fCryostat_z/2 + fWoodThickness +fShieldThickness+ fColdSkinThickness + Offset)
        
        sWood = geom.shapes.Boolean('Wood', type = 'subtraction', 
						first = sOutWood, 
						second = sOutShield)
        
        fLogicWood = make_volume(geom, "Wood", sWood, "WoodLog",aux=True) 

        WoodPla = geom.structure.Placement('WoodPlacement',
                                                                
                                            pos = geom.structure.Position('WoodPosition',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = fLogicWood
                                                                
                                            ) 
        self.PlacementList.append(WoodPla)

        ###this is the start of warmskin Logical volume###
        ShellOutW = geom.shapes.Box('ShellOutW',
					dy = fCryostat_x/2 +fWarmSkinThickness+ fWoodThickness +fShieldThickness+ fColdSkinThickness + Offset,
					dx = fCryostat_y/2 +fWarmSkinThickness+ fWoodThickness +fShieldThickness+ fColdSkinThickness + Offset,
					dz = fCryostat_z/2 +fWarmSkinThickness+ fWoodThickness +fShieldThickness+ fColdSkinThickness + Offset)
        
        fShellW = geom.shapes.Boolean('WarmSkin', type = 'subtraction', 
						first = ShellOutW, 
						second = sOutWood)
        fLogicShellW = make_volume(geom,"fDuneSteel",fShellW, "ShellOutLog", aux=True)

        ShellOutPla = geom.structure.Placement('Warmskin',
                                                                
                                            pos = geom.structure.Position('WarmskinPosition',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = fLogicShellW
                                                                
                                            ) 
        self.PlacementList.append(ShellOutPla)
        

        

       





    
        

        

   



