import gegede.builder
from gegede import Quantity as Q
from utils import *
#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
#Globals
#--------------------#
fht = Q('841.1cm')
fst = Q('896.4cm')
fSpacing = Q('157.86cm')
fIFlangeWidth = Q('40.2cm')
fIFlangeThick = Q('4cm')
fIFlangeWaist = Q('2.2cm')
fIFlangeHeight = Q('110.8cm')
fIPortSpacing = Q('400cm')
fITopLength = Q('1783.2cm') + fIFlangeHeight
fISideLength = Q('1473.2cm') + fIFlangeHeight
fIPortHoleRad = Q('40cm')	
#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

def make_volume(geom, material, shape, name='', aux=False):
    name_lv = name
    if name == '':
        name_lv = 'vol'+shape.name

    lv = geom.structure.Volume(name_lv,
                               material = material,
                               shape = shape,
                               )
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
					dy = (fIFlangeWidth /2),
					dx = (fIFlangeThick /2),
					dz = (fITopLength /2))#creating a IBeamTopFlanfe object
        IBeamTopMid = geom.shapes.Box('IBeamTopMid',
					dy = (fIFlangeWaist /2),
					dx = (fIFlangeHeight /2),
					dz = (fITopLength /2))#creating a IBeamTopMid object
        IBeamSideFlange = geom.shapes.Box('IBeamSideFlange',
					dy = (fIFlangeWidth /2),
					dx = (fIFlangeThick /2),
					dz = (fISideLength /2))#creating a IBeamSideFlange object
        IBeamSideMidtmp0 = geom.shapes.Box('IBeamSideMid',
					dy = (fIFlangeWaist /2),
					dx = (fIFlangeHeight /2),
					dz = (fISideLength /2))#creating a IBeamSideMid object
        IBeamPort = geom.shapes.Tubs('IBeamPortTub',
					rmin = Q('0cm'),
					rmax = fIPortHoleRad,
					dz = (fIFlangeThick /2),
					sphi = Q('0deg'),
					dphi = Q('360deg')) 
        
        fcRotation = geom.structure.Rotation('fc', x= "90deg", y= "0deg",z= "0deg")
        fc2Rotation = geom.structure.Rotation('fc2',x= "0deg", y= "90deg",z= "90deg")
        fc3Rotation = geom.structure.Rotation('fc3', x= "0deg", y= "90deg",z= "0deg")
        
        IBeamBotMidtmp = geom.shapes.Boolean('IBeamBottomtmp', type = 'subtraction', 
						first = IBeamTopMid, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam', x="0cm", y="0cm", z=fIPortSpacing/2), 
						rot = fcRotation)
        IBeamBotMid = geom.shapes.Boolean('IBeamBottom', type = 'subtraction', 
						first = IBeamBotMidtmp, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam2', x="0cm", y="0cm", z=-fIPortSpacing/2), 
						rot = fcRotation)
        IBeamSideMidtmp1 = geom.shapes.Boolean('IBeamSidetmp', type = 'subtraction', 
						first = IBeamSideMidtmp0, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam3', x="0cm", y="0cm", z=((fISideLength/2) + (fIFlangeHeight/2) - Q('590.7cm'))),
						rot =fcRotation)
        IBeamSideMidtmp2 = geom.shapes.Boolean('IBeamSidetmp2', type = 'subtraction', 
						first = IBeamSideMidtmp1, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam4', x="0cm", y="0cm", z=((fISideLength/2) + (fIFlangeHeight/2) - Q('590.7cm') - fIPortSpacing)),
						rot =fcRotation)
        IBeamSideMid = geom.shapes.Boolean('IBeamSide', type = 'subtraction', 
						first = IBeamSideMidtmp2, 
						second = IBeamPort,
						pos = geom.structure.Position('PosOfIBeam5', x="0cm", y="0cm", z=((fISideLength/2) + (fIFlangeHeight/2) - Q('590.7cm') - (2*fIPortSpacing))),
						rot =fcRotation)
        
        IBeamTopPosition = geom.structure.Position('TopPosition', y= Q('0cm'), x=((fIFlangeHeight /2) + (fIFlangeThick /2)), z= Q('0cm')) 
        IBeamBottomPosition = geom.structure.Position('BottomPosition', y= Q('0cm'), x=((-fIFlangeHeight /2) - (fIFlangeThick /2)), z= Q('0cm'))


        fBeamTopVol1 = geom.shapes.Boolean('TopBeamUnion', type = 'union', 
						first = IBeamTopMid,
						second = IBeamTopFlange,
						pos = IBeamTopPosition)
        fBeamTopVol2 = geom.shapes.Boolean('TopBeamUnion2.1', type = 'union',
						first = fBeamTopVol1,
						second = IBeamTopFlange,
						pos = IBeamBottomPosition)
        fIBeamTopLog = make_volume(geom, 'fDuneSteel', fBeamTopVol2, 'IBeamTop', aux = True)
        
        fBeamBotVol1 = geom.shapes.Boolean('TopBeamUnion1.1', type = 'union', 
						first = IBeamBotMid,
						second = IBeamTopFlange,
						pos = IBeamTopPosition)
        fBeamBotVol2 = geom.shapes.Boolean('TopBeamUnion2.2', type = 'union',
						first = fBeamBotVol1,
						second = IBeamTopFlange,
						pos = IBeamBottomPosition)
        fIBeamBotLog = make_volume(geom, 'fDuneSteel', fBeamBotVol2, 'IBeamBot', aux = True) 
        
        fBeamSideVol1 = geom.shapes.Boolean('TopBeamUnion1.3', type = 'union', 
						first = IBeamSideMid,
						second = IBeamSideFlange,
						pos = IBeamTopPosition)
        fBeamSideVol2 = geom.shapes.Boolean('TopBeamUnion2.3', type = 'union',
						first = fBeamSideVol1,
						second = IBeamSideFlange,
						pos = IBeamBottomPosition)
        fIBeamSideLog = make_volume(geom, 'fDuneSteel', fBeamSideVol2, 'IBeamSide', aux = True) 
        #big box for ibeams volume
        
        ht = fht
        st = fst
        zbsp = fSpacing
        cpIT = Q('0')
        cpIB = Q('0')
        cpIL = Q('0')
        cpIR = Q('0')
        zpl = Q('0cm')
        mIL  = Q('0')
        cpIF = Q('0')
        cpIBk = Q('0')
        xpl = Q('0cm')
        fzpl = Q('6473.2cm')

        for i in range(20):
                  IBeamTopPlacement = geom.structure.Placement(f'IBeamTopPLacement{i}',
                                                               rot = fcRotation,
                                                               volume = fIBeamTopLog,
                                                                pos = geom.structure.Position(f'IBeamTopPlacementPos{i}',
                                                                y = "0cm",
                                                                x =  ht,
                                                                z = zpl),
                                                            	)
                  self.PlacementList.append(IBeamTopPlacement)

                  IBeamBotPlacement = geom.structure.Placement(f'IBeamBotPLacement{i}',
                                                               rot = fcRotation,
                                                               volume = fIBeamBotLog,
                                                                pos = geom.structure.Position(f'IBeamBackPlacementPos{i}',
                                                                y = "0cm",
                                                                x =  - ht,
                                                                z = zpl) 
                                                            	)
                  self.PlacementList.append(IBeamBotPlacement)

                  IBeamLeftPlacement = geom.structure.Placement(f'IBeamLeftPLacement{i}',
                                                               rot = fc2Rotation,
                                                               volume = fIBeamSideLog,
                                                                pos = geom.structure.Position(f'IBeamLeftPlacementPos{i}',
                                                                y = - st,
                                                                x =  "0cm",
                                                                z = zpl)
                                                            	)
                  self.PlacementList.append(IBeamLeftPlacement)

                  IBeamRightPlacement = geom.structure.Placement(f'IBeamRightPLacement{i}',
                                                                rot = fc2Rotation,
                                                                pos = geom.structure.Position(f'IBeamRightPlacementPos{i}',
                                                                y = st,
                                                                x =  "0cm",
                                                                z = zpl),
                                                            	volume = fIBeamSideLog)
                  self.PlacementList.append(IBeamRightPlacement)

                  if i == 0:
                       zpl += zbsp
                       continue
                  

                  IBeamTopPlacement = geom.structure.Placement(f'IBeamTopPLacement2{i}',
                                                                 rot = fcRotation,
                                                                pos = geom.structure.Position(f'IBeamTopPlacementPos2{i}',
                                                                y = "0cm",
                                                                x =  ht,
                                                                z = -(zpl)),
                                                            	volume = fIBeamTopLog)
                  self.PlacementList.append(IBeamTopPlacement)

                  IBeamBotPlacement = geom.structure.Placement(f'IBeamBotPLacement2{i}',
                                                                 rot = fcRotation,
                                                                pos = geom.structure.Position(f'IBeamBotPlacementPos2{i}',
                                                                y = "0cm",
                                                                x =  -(ht),
                                                                z = -(zpl)),
                                                            	volume = fIBeamBotLog)
                  self.PlacementList.append(IBeamBotPlacement)

                  IBeamLeftPlacement = geom.structure.Placement(f'IBeamLeftPLacement2{i}',
                                                                rot = fc2Rotation,
                                                                pos = geom.structure.Position(f'IBeamLeftPlacementPos2{i}',
                                                                y = -(st),
                                                                x =  "0cm",
                                                                z = -(zpl)),
                                                            	volume = fIBeamSideLog)
                  self.PlacementList.append(IBeamLeftPlacement)

                  IBeamRightPlacement = geom.structure.Placement(f'IBeamRightPLacement2{i}',
                                                                 rot = fc2Rotation,
                                                                pos = geom.structure.Position(f'IBeamRightPlacementPos2{i}',
                                                                y = st,
                                                                x =  "0cm",
                                                                z = -(zpl)),
                                                            	volume = fIBeamSideLog)
                  self.PlacementList.append(IBeamRightPlacement)

                  zpl += zbsp
        
        
        xpl = Q('0cm')
        zpl = (fzpl /2)
        for i in range(5):
            IBeamFrontPlacement = geom.structure.Placement(f'IBeamFrontPLacement{i}',
                                                                rot = fc3Rotation,
                                                                pos = geom.structure.Position(f'IBeamFrontPlacementPos{i}',
                                                                y = xpl,
                                                                x =  "0cm",
                                                                z = zpl),
                                                            	volume = fIBeamSideLog)
            self.PlacementList.append(IBeamFrontPlacement)
            
            IBeamBackPlacement = geom.structure.Placement(f'IBeamBackPlacement{i}',
                                                                rot = fc3Rotation,
                                                                pos = geom.structure.Position(f'IBeamBackPlacementPos2ndLoop{i}',
                                                                y = xpl,
                                                                x =  "0cm",
                                                                z = -zpl),
                                                            	volume = fIBeamSideLog)
            self.PlacementList.append(IBeamBackPlacement)

            if i == 0:
                xpl +=zbsp
                continue
            
            IBeamFrontPlacement = geom.structure.Placement(f'IBeamFrontPLacement2{i}',
                                                                rot = fc3Rotation,
                                                                pos = geom.structure.Position(f'IBeamFrontPlacementPos2{i}',
                                                                y = -xpl,
                                                                x =  "0cm",
                                                                z = zpl),
                                                            	volume = fIBeamSideLog)
            self.PlacementList.append(IBeamFrontPlacement)

            IBeamBackPlacement = geom.structure.Placement(f'IBeamBackPlacement2{i}',
                                                                rot = fc3Rotation,
                                                                pos = geom.structure.Position(f'IBeamBackPlacementPos2{i}',
                                                                y = -xpl,
                                                                x =  "0cm",
                                                                z = -zpl),
                                                            	volume = fIBeamSideLog)
            self.PlacementList.append(IBeamBackPlacement)
          

            xpl += zbsp
        
             

             
             




                
                  

                  
	
                    
									
				

		
	
	
	






		
