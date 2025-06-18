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


class BeltsBuilder(gegede.builder.Builder):
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

        ht = fht
        st = fst

        BeltFlange = geom.shapes.Box('BeltFlange',
					dx = Q('10cm'),
					dy = (fIFlangeWaist /2),
					dz = ((fSpacing /2) - (fIFlangeWaist/2) - Q('0.001cm')))
        
        BeltMid = geom.shapes.Box('BeltMid',
					dx = (fIFlangeWaist/2),
					dy = (fIFlangeHeight /4),
					dz = ((fSpacing /2) - (fIFlangeWaist/2) - Q('0.001cm')))
        
        IBeamPort = geom.shapes.Tubs('BeltPortHole',
					rmin = Q('0cm'),
					rmax = Q('25cm'),
					dz = (fIFlangeThick /2),
					sphi = Q('0deg'),
					dphi = Q('360deg')) 
        
        fcRotation = geom.structure.Rotation('fcBelt', x= "0deg", y= "0deg",z= "90deg")
        fc2Rotation = geom.structure.Rotation('fc2Belt',x= "0deg", y= "90deg",z= "0deg")
        fc3Rotation = geom.structure.Rotation('fc3Belt', x= "90deg", y= "0deg",z= "90deg")
        

        BeltHole = geom.shapes.Boolean('BeltHole', type = 'subtraction', 
						first = BeltMid, 
						second = IBeamPort,
						pos = geom.structure.Position('BeltHoleSub', x="0cm", y="0cm", z="0cm"), 
						rot = fc2Rotation)
        

        tr1 = geom.structure.Position('tr1', x= Q('0cm'), y=(fIFlangeHeight/4), z= Q('0cm')) 
        tr2 = geom.structure.Position('tr2', x= Q('0cm'), y=(-fIFlangeHeight /4), z= Q('0cm'))

        Union1 = geom.shapes.Boolean('Union1', type = 'union', 
						first = BeltHole,
						second = BeltFlange,
						pos = tr1)
        BeltHoleUni = geom.shapes.Boolean('BeltHoleUnion', type = 'union',
						first = Union1,
						second = BeltFlange,
						pos = tr2)
        
        
        BeltHoleUniLog = make_volume(geom, 'AirSteelMixture', BeltHoleUni, 'BeltHoleUni', aux = True) 
        

        Union2 = geom.shapes.Boolean('Union2', type = 'union', 
						first = BeltMid,
						second = BeltFlange,
						pos = tr1)
        BeltUni = geom.shapes.Boolean('BeltUnion', type = 'union',
						first = Union2,
						second = BeltFlange,
						pos = tr2)
        
        
        

        BeltUniLog = make_volume(geom, 'AirSteelMixture', BeltUni, 'BeltUni', aux = True)
	

        zbsp = fSpacing
        zpl = (zbsp/2)
        xpl = Q('0cm')
        eps = Q('21.5cm')
        cpIT = Q('0cm')
        cpIB = Q('0cm')
        cpIL = Q('0cm')
        cpIR = Q('0cm')
        fzpl = Q('6473.2cm')

        for ii in range (19):
            for jj in range(-5,5):
                BeltBot = geom.structure.Placement(f'BeltBottom_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltBottomPlacement_{jj}_{ii}',
                                                                x = ((jj + 0.5) * zbsp),
                                                                y =  (-ht + eps),
                                                                z = (zpl)),
                                                            	volume = BeltHoleUniLog)
                self.PlacementList.append(BeltBot)

                BeltBot = geom.structure.Placement(f'BeltBottom2_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltBottomPlacement2_{jj}_{ii}',
                                                                x = ((jj + 0.5) * zbsp),
                                                                y =  (-ht + eps),
                                                                z = (-zpl)),
                                                            	volume = BeltHoleUniLog)
                self.PlacementList.append(BeltBot)

                if abs(jj) in (1, 2, 4):

                    BeltTop = geom.structure.Placement(f'BeltTop_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltTopPlacement_{jj}_{ii}',
                                                                x = ((jj + 0.5) * zbsp),
                                                                y =  (ht - eps),
                                                                z = (zpl)),
                                                            	volume = BeltUniLog)
                    self.PlacementList.append(BeltTop)

                    BeltTop = geom.structure.Placement(f'BeltTop2_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltTopPlacement2_{jj}_{ii}',
                                                                x = ((jj + 0.5) * zbsp),
                                                                y =  (ht - eps),
                                                                z = (-zpl)),
                                                            	volume = BeltUniLog)
                    self.PlacementList.append(BeltTop)
            
            
            for kk in range(4):
                yvar = None
                belt = BeltHoleUniLog

                if kk == 3:
                    yvar = ht-eps
                    belt = BeltUniLog
                    if ii % 3:
                        belt = BeltHoleUniLog
                if kk == 2:
                    yvar = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(0.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2

                if kk ==1:
                    yvar = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(2.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
                    belt = BeltUniLog
                    if (ii+1) % 3:
                        belt =BeltHoleUniLog

                if kk == 0:
                    yvar  = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(4.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
                    belt = BeltUniLog
                    if ((ii+2) %3):
                        belt = BeltHoleUniLog

                if ii ==20:
                    belt = BeltUniLog

                BeltLeft = geom.structure.Placement(f'BeltLeft{kk}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltLeftPlacement{kk}_{ii}',
                                                                x = -st,
                                                                y = yvar ,
                                                                z = (-zpl)),
                                                            	volume = belt,
                                                                rot= fcRotation)
                self.PlacementList.append(BeltLeft)

                BeltRight = geom.structure.Placement(f'BeltRight{kk}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltRigthPlacement{kk}_{ii}',
                                                                x = st,
                                                                y = yvar ,
                                                                z = (-zpl)),
                                                            	volume = belt,
                                                                rot= fcRotation)
                self.PlacementList.append(BeltRight)

                BeltLeft = geom.structure.Placement(f'BeltLeft_{kk}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltLeftPlacement_{kk}_{ii}',
                                                                x = -st,
                                                                y = yvar ,
                                                                z = (zpl)),
                                                            	volume = belt,
                                                                rot= fcRotation)
                self.PlacementList.append(BeltLeft)

                BeltRight = geom.structure.Placement(f'BeltRight_{kk}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltRigthPlacement_{kk}_{ii}',
                                                                x = st,
                                                                y = yvar ,
                                                                z = (zpl)),
                                                            	volume = belt,
                                                                rot= fcRotation)
                self.PlacementList.append(BeltRight)
            zpl+=zbsp

        cpBF =0
        cpBBK =0
        xpl = zbsp/2
        zpl = fzpl / 2 + Q('0.100cm')
        for ii in range(5):
            for jj in range (4):
                y = None
                belt = BeltHoleUniLog

                if jj == 3:
                    y = ht
                    belt = BeltUniLog
                    if ii % 3:
                        belt = BeltHoleUniLog
                if jj == 2:
                    y = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(0.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
                if jj ==1:
                    y = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(0.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
                    belt = BeltUniLog
                    if ((ii +1) % 3):
                        belt = BeltHoleUniLog
                if jj == 0:
                    y = -((fISideLength / 2) +(fIFlangeHeight / 2) -Q('590.7cm') +(0.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
                    belt = BeltUniLog
                    if ((ii +2) %3 ):
                        belt = BeltHoleUniLog


                if ii == 20:
                    belt = BeltUniLog

                
                BeltBack = geom.structure.Placement(f'BeltBack_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltBackPlacement_{jj}{ii}',
                                                                x = -xpl,
                                                                y = y ,
                                                                z = -zpl),
                                                            	volume = belt,
                                                                rot= fc3Rotation)
                self.PlacementList.append(BeltBack)

                BeltBack = geom.structure.Placement(f'BeltBack2_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltBackPlacement2_{jj}{ii}',
                                                                x = xpl,
                                                                y = y ,
                                                                z = -zpl),
                                                            	volume = belt,
                                                                rot= fc3Rotation)
                self.PlacementList.append(BeltBack)

                BeltFront = geom.structure.Placement(f'BeltFront_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltFrontPlacement_{jj}{ii}',
                                                                x = -xpl,
                                                                y = y ,
                                                                z = zpl),
                                                            	volume = belt,
                                                                rot= fc3Rotation)
                self.PlacementList.append(BeltFront)

                BeltFront = geom.structure.Placement(f'BeltFront2_{jj}_{ii}',
                                                                
                                                                pos = geom.structure.Position(f'BeltFrontPlacement2_{jj}{ii}',
                                                                x = xpl,
                                                                y = y ,
                                                                z = zpl),
                                                            	volume = belt,
                                                                rot= fc3Rotation)
                self.PlacementList.append(BeltFront)
            xpl =+zbsp

                
                





 
