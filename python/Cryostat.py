import gegede.builder
from gegede import Quantity as Q
from utils import *


#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
#Globals
#--------------------#
fht = Q('841.1cm')
fst = Q('896.4cm')
fzpl = Q('6473.2cm')
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
fShieldThickness = Q('77.6cm')
fWoodThickness = Q('4.8cm')
fWarmSkinThickness = Q('2.4cm')




	
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
        
        LArBoxLog = make_volume(geom, 'LAr', LarBox, "LArBoxLogical", aux=True)

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
        

        ##this is the start of air box logical volume###

        '''worldBox = geom.shapes.Box("WorldBox",
                                   dy=Q('5000cm')/2 ,
                                   dx=Q('5000cm')/2,
                                   dz=Q('7500cm')/2)
        fOuterAir = geom.shapes.Boolean('OuterAir', type = 'subtraction', 
						first = worldBox, 
						second = ShellOutW)
        fLogicOAir = make_volume(geom, "Air",fOuterAir,"OuterAirLog", aux=True)

        OuterAirPla = geom.structure.Placement('OuterAirPla',
                                                                
                                            pos = geom.structure.Position('OuterAirPosition',
                                            x = "0cm",
                                            y =  "0cm",
                                            z = "0cm"),
                                            volume = fLogicOAir
                                                                
                                            ) 
        self.PlacementList.append(OuterAirPla)

        '''

        ##this is the start of the rock floor volume

        # rockThick = Q('1000cm')

        # rockFloor = geom.shapes.Box('RockFloor',
		# 			dy = fst*1.5,
		# 			dx = rockThick/2,
		# 			dz = (fzpl/2)*1.1)
        
        # fLogicRockFloor = make_volume(geom,'DUSEL_Rock',rockFloor, "RockFloorLog", aux=True)


        # fPhysRockFloor = geom.structure.Placement('RockFloorPlacement',
                                                                
        #                                     pos = geom.structure.Position('RockFloorPosition',
        #                                     y = "0cm",
        #                                     x =  -(fht+Q('110cm')+rockThick/2),
        #                                     z = "0cm"),
        #                                     volume = fLogicRockFloor
                                                                
        #                                     ) 
        # self.PlacementList.append(fPhysRockFloor)





    
        

        

   



