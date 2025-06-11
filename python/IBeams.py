import gegede.builder
from gegede import Quantity as Q
from utils import *


#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
#Globals
#---------------------#
fht = Q('841.1cm')
fst = Q('896.4cm')
fSpacing = Q('157.86cm')
fIFlangeWidth = Q('0.42cm')
fIFlangeThick = Q('4cm')
fIFlangeWaist = Q('2.2cm')
fIFlangeHeight = Q('110.8cm')
fIPortSpacing = Q('400cm')

scale_factor =  (fIFlangeHeight / Q('1cm')) /2
fITopLength = Q('1983.2cm') * scale_factor
fISideLength = Q('1473.2cm') * scale_factor
fIPortHoleRad = Q('40cm')	
	
#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......




def make_volume(geom, material, shape, name='', aux=False):
    name_lv = name
    if name == '':
        name_lv = 'vol'+shape.name

    lv = geom.structure.Volume(name_lv,
                               material = material,
                               shape = shape)
    if lv == None:
         return print("logical volume failed to be created")
    else:
         return lv


class IBeamsBuilder(gegede.builder.Builder):
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
        IBeamTopFlange = geom.shapes.Box('IBeamTopFlange',
					dx = (fIFlangeWidth /Q('2')),
					dy = (fIFlangeThick /Q('2')),
					dz = (fITopLength /Q('2')))#creating a IBeamTopFlanfe object
        IBeamTopMid = geom.shapes.Box('IBeamTopMid',
					dx = (fIFlangeWaist /Q('2')),
					dy = (fIFlangeHeight /Q('2')),
					dz = (fITopLength /Q('2')))#creating a IBeamTopMid object
        IBeamSideFlange = geom.shapes.Box('IBeamSideFlange',
					dx = (fIFlangeWidth /Q('2')),
					dy = (fIFlangeThick /Q('2')),
					dz = (fISideLength /Q('2')))#creating a IBeamSideFlange object
        IBeamSideMidtmp0 = geom.shapes.Box('IBeamSideMid',
					dx = (fIFlangeWaist /Q('2')),
					dy = (fIFlangeThick /Q('2')),
					dz = (fISideLength /Q('2')))#creating a IBeamSideMid object
        IBeamPort = geom.shapes.Tubs('IBeamPortTub',
					rmin = Q('0cm'),
					rmax = fIPortHoleRad,
					dz = (fIFlangeThick /Q('2')),
					sphi = Q('0deg'),
					dphi = Q('360deg')) ## created a tube form, still need to talk to eric about this
        fcRotation = geom.structure.Rotation('fc', x= Q('0deg'), y= Q('90deg'),z= Q('0deg'))#90 degrees about the Yaxis, can also use if from utils/definitions.py, same for below jsut diofferent axis
        fc2Rotation = geom.structure.Rotation('fc2', x= Q('0deg'),y= Q('90deg'),z= Q('0deg'))
        fc3Rotation = geom.structure.Rotation('fc3', x= Q('0deg'),y= Q('0deg'),z= Q('90deg'))
        IBeamBotMidtmp = geom.shapes.Boolean('IBeamBottomtmp', type = 'subtraction', 
						first = IBeamTopMid, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam', x=Q('0cm'), y=Q('0cm'), z=(fIPortSpacing )), 
						rot =fcRotation)## these next couple of subtractions are basically cutting out a part of thr first object passed in with the second object, still need to create the global variables
        IBeamBotMid = geom.shapes.Boolean('IBeamBottom', type = 'subtraction', 
						first = IBeamBotMidtmp, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam2', x=Q('0cm'), y=Q('0cm'), z=(-fIPortSpacing/Q('2'))), 
						rot =fcRotation)
        IBeamSideMidtmp1 = geom.shapes.Boolean('IBeamSidetmp', type = 'subtraction', 
						first = IBeamSideMidtmp0, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam3', x=Q('0cm'), y=Q('0cm'), z=(-fIPortSpacing/Q('2'))),## the z dimension will need ot be fixed
						rot =fcRotation)
        IBeamSideMidtmp2 = geom.shapes.Boolean('IBeamSidetmp2', type = 'subtraction', 
						first = IBeamSideMidtmp1, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam4', x=Q('0cm'), y=Q('0cm'), z=(-fIPortSpacing/Q('2'))),## the z dimension will need ot be fixed
						rot =fcRotation)
        IBeamSideMid = geom.shapes.Boolean('IBeamSide', type = 'subtraction', 
						first = IBeamSideMidtmp2, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam5', x=Q('0cm'), y=Q('0cm'), z=(-fIPortSpacing/Q('2'))),## the z dimension will need ot be fixed
						rot =fcRotation)
        IBeamTopPosition = geom.structure.Position('TopPosition', x= Q('0cm'), y=((fIFlangeHeight /Q('2')) + (fIFlangeThick /Q('2'))), z= Q('0cm')) ## still need to implement all globals and actual coordinates, corresponding to tri & tr2 in erics code.
        IBeamBottomPosition = geom.structure.Position('BottomPosition', x= Q('0cm'), y=((-fIFlangeHeight /Q('2')) - (fIFlangeThick /Q('2'))), z= Q('0cm'))
        fBeamTopVol1 = geom.shapes.Boolean('TopBeamUnion', type = 'union', 
						first = IBeamTopMid,
						second = IBeamTopFlange,
						pos = IBeamTopPosition)
        fBeamTopVol2 = geom.shapes.Boolean('TopBeamUnion2.1', type = 'union',
						first = fBeamTopVol1,
						second = IBeamTopFlange,
						pos = IBeamBottomPosition)
        fIBeamTopLog = make_volume(geom, 'AirSteelMixture', fBeamTopVol2, 'IBeamTop', aux = True) #making the logical volume for the beam top
        fBeamBotVol1 = geom.shapes.Boolean('TopBeamUnion1.1', type = 'union', 
						first = IBeamBotMid,
						second = IBeamTopFlange,
						pos = IBeamTopPosition)
        fBeamBotVol2 = geom.shapes.Boolean('TopBeamUnion2.2', type = 'union',
						first = fBeamBotVol1,
						second = IBeamTopFlange,
						pos = IBeamBottomPosition)
        fIBeamBotLog = make_volume(geom, 'AirSteelMixture', fBeamBotVol2, 'IBeamBot', aux = True) 
        fBeamSideVol1 = geom.shapes.Boolean('TopBeamUnion1.3', type = 'union', 
						first = IBeamSideMid,
						second = IBeamSideFlange,
						pos = IBeamTopPosition)
        fBeamSideVol2 = geom.shapes.Boolean('TopBeamUnion2.3', type = 'union',
						first = fBeamSideVol1,
						second = IBeamSideFlange,
						pos = IBeamBottomPosition)
        fIBeamSideLog = make_volume(geom, 'AirSteelMixture', fBeamSideVol2, 'IBeamSide', aux = True) 
        ht = fht
        st = fst
        zbsp = fSpacing
        cpIT = 0
        cpIB = 0
        cpIL = 0
        cpIR = 0
        zpl = Q('0cm')
        mIL  = 0.0
        for i in range(18):
                  IBeamTopPlacement = geom.structure.Placement(f'IBeamTopPLacement{i}',
                                                               rot = fcRotation,
                                                                pos = geom.structure.Position(f'IBeamTopPlacementPos{i}',
                                                                x = Q('0cm'),
                                                                y =  ht,
                                                                z = zpl),
                                                            	volume = fIBeamTopLog)
                  self.PlacementList.append(IBeamTopPlacement)

                  IBeamBotPlacement = geom.structure.Placement(f'IBeamBotPLacement{i}',
                                                               rot = fcRotation,
                                                                pos = geom.structure.Position(f'IBeamBackPlacementPos{i}',
                                                                x = Q('0cm'),
                                                                y =  -ht,
                                                                z = zpl),
                                                            	volume = fIBeamBotLog)
                  self.PlacementList.append(IBeamBotPlacement)

                  IBeamLeftPlacement = geom.structure.Placement(f'IBeamLeftPLacement{i}',
                                                               rot = fc2Rotation,
                                                                pos = geom.structure.Position(f'IBeamLeftPlacementPos{i}',
                                                                x = -(st),
                                                                y =  Q('0cm'),
                                                                z = zpl),
                                                            	volume = fIBeamSideLog)
                  self.PlacementList.append(IBeamLeftPlacement)

                  IBeamRightPlacement = geom.structure.Placement(f'IBeamRightPLacement{i}',
                                                               rot = fc2Rotation,
                                                                pos = geom.structure.Position(f'IBeamRightPlacementPos{i}',
                                                                x = st,
                                                                y =  Q('0cm'),
                                                                z = zpl),
                                                            	volume = fIBeamSideLog)
                  self.PlacementList.append(IBeamRightPlacement)

                  if i == 0:
                       zpl = zbsp
                       continue
                  

                  IBeamTopPlacement = geom.structure.Placement(f'IBeamTopPLacement2{i}',
                                                               rot = fcRotation,
                                                                pos = geom.structure.Position(f'IBeamTopPlacementPos_{i}',
                                                                x = Q('0cm'),
                                                                y =  ht,
                                                                z = -(zpl)),
                                                            	volume = fIBeamTopLog)
                  self.PlacementList.append(IBeamTopPlacement)

                  
                  

                  
	
                    
									
				

		
	
	
	






		
