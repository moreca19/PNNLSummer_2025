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
eps = Q('21.5cm')
ht = fht
st = fst + Q('3.1cm')
fzpl = Q('6473.2cm')
#....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......



## making a volume helper function##
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
##==========================================##

## creating a placement helper fucntion##
def make_placement(geom, position, name,volume,rot):
    Placement = geom.structure.Placement(
        name,
        pos = position,
        volume = volume,
        rot = rot
    )

    if Placement == None:
        print("creation of placement was failed")
        return
    else:
        return Placement
##============================================##

## Creating a position helper function ##
def make_position(geom, name, X,Y,Z):
    
    position = geom.structure.Position(name, x=Y,y=X,z=Z)

    if position == None:
       return print("creation of position was failed")
        
    else:
        
        return position

##============================================##

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

        yTopHole = -((fISideLength / 2) +(fIFlangeHeight / 2) - Q('590.7cm') -(3.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
        yBotHole = -((fISideLength / 2) +(fIFlangeHeight / 2) - Q('590.7cm') -(-1.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
        y1HoleUp = -((fISideLength / 2) +(fIFlangeHeight / 2) - Q('590.7cm') -(1.0 * fIPortSpacing) +(9 * fIPortHoleRad)) / 2
        yTop = (ht-eps)


        BlockWidth = fSpacing - fIFlangeWaist - Q('0.1cm') - Q('5cm')
        BlockHeight = fIPortSpacing - Q('5cm')
        BlockHeightTop = BlockHeight * 0.63
        BlockHeightBottom = BlockHeight * 0.15

        fBlockThickness = Q('23cm')

        
        ShieldBlock = geom.shapes.Box('ShieldBlock',
					dy = (fBlockThickness /2),
					dx = (BlockHeight /2),
					dz = (BlockWidth /2))
        
        ShieldBlockTop = geom.shapes.Box('ShieldBlockTop',
					dy = (fBlockThickness /2),
					dx = (BlockHeightTop /2),
					dz = (BlockWidth /2))
        
        ShieldBlockBot = geom.shapes.Box('ShieldBlockBot',
					dy = (fBlockThickness /2),
					dx = (BlockHeightBottom /2),
					dz = (BlockWidth /2))
        
        fcRotation = geom.structure.Rotation('fcRotation', x= "0deg", y= "0deg",z= "0deg")
        fc2Rotation = geom.structure.Rotation('fc2Rotation',x= "90deg", y= "0deg",z= "0deg")
        fc3Rotation = geom.structure.Rotation('fc3Rotation', x= "0deg", y= "0deg",z= "90deg")

        ShieldBlockLog = make_volume(geom,'Water',ShieldBlock, 'ShieldBlockLog', aux = True  )
        ShieldBlockTopLog = make_volume(geom,'Water',ShieldBlockTop, 'ShieldBlockTopLog', aux = True  )
        ShieldBlockBotLog = make_volume(geom,'Water',ShieldBlockBot, 'ShieldBlockBotLog', aux = True  )

        zbsp = fSpacing
        zpl = zbsp /2
        xpl = Q('0cm')

        for ii in range(20):
            for jj in range(5):
                y = "0cm"
                shield = ShieldBlockLog
                if(jj ==3):
                    y = yTopHole + BlockHeight/2+ BlockHeightTop/2 + Q('5cm')
                    shield = ShieldBlockTopLog
                if(jj==2):
                    y = yBotHole
                if(jj==1):
                    y = y1HoleUp
                if(jj==4):
                    y= (yBotHole)-(BlockHeight/2) - (0.05*BlockHeightBottom)- (Q('5cm'))
                    shield = ShieldBlockBotLog  
                
                if(jj== 0 or jj ==3):
                    continue


                
                shieldLeftPosition = make_position(geom , f'ShieldLeftPosition{ii}{jj}',-st,y,-zpl)
                shieldLeft = make_placement(geom, shieldLeftPosition,f'ShieldLeftPlacement{ii}{jj}', shield, fcRotation)
                self.PlacementList.append(shieldLeft)

                shieldRightPosition = make_position(geom , f'ShieldRightPosition{ii}{jj}',st,y,-zpl)
                shieldRight = make_placement(geom, shieldRightPosition,f'ShielRightPlacement{ii}{jj}',  shield,fcRotation)
                self.PlacementList.append(shieldRight)

                shieldLeftPosition = make_position(geom , f'ShieldLeft2Position{ii}{jj}',-st,y,zpl)
                shieldLeft = make_placement(geom, shieldLeftPosition,f'ShieldLeft2Placement{ii}{jj}',  shield,fcRotation)
                self.PlacementList.append(shieldLeft)

                shieldRightPosition = make_position(geom , f'ShieldRight2Position{ii}{jj}',st,y,zpl)
                shieldRight = make_placement(geom, shieldRightPosition,f'ShielRight2Placement{ii}{jj}',  shield,fcRotation)
                self.PlacementList.append(shieldRight)

            zpl += zbsp

        xpl = zbsp/2
        zpl = fzpl/2
        for ii in range(5):
            for jj in range(5):
                y = "0cm"
                shield = ShieldBlockLog
                if(jj==3):
                    y = yTopHole + BlockHeight/2 + BlockHeightTop/2 + Q('5cm')
                    shield = ShieldBlockTopLog

                if(jj==2):
                    y = yBotHole
                
                if(jj==1):
                    y = y1HoleUp
                if(jj==0):
                    y =yTopHole
                if(jj==4):
                    y = yBotHole -BlockHeight/2 - 0.5*BlockHeightBottom - Q('5cm')
                    shield = ShieldBlockBotLog

                ShieldBackPositon = make_position(geom, f'ShieldBackPosition{ii}{jj}', -xpl, y, -zpl)
                ShielBackPlacement = make_placement(geom,ShieldBackPositon,f'ShieldBackPlacement{ii}{jj}', shield,fc2Rotation)
                self.PlacementList.append(ShielBackPlacement)

                ShieldBackPositon = make_position(geom, f'ShieldBack2Position{ii}{jj}', xpl, y, -zpl)
                ShielBackPlacement = make_placement(geom,ShieldBackPositon,f'ShieldBack2Placement{ii}{jj}', shield,fc2Rotation)
                self.PlacementList.append(ShielBackPlacement)

                ShieldFrontPosition = make_position(geom, f'ShieldFrontposition{ii}{jj}', -xpl,y,zpl)
                ShieldFrontPlacement = make_placement(geom,ShieldFrontPosition,f'ShieldFrontPlacement{ii}{jj}',shield,fc2Rotation)
                self.PlacementList.append(ShieldFrontPlacement)

                ShieldFrontPosition = make_position(geom, f'ShieldFront2position{ii}{jj}', xpl,y,zpl)
                ShieldFrontPlacement = make_placement(geom,ShieldFrontPosition,f'ShieldFront2Placement{ii}{jj}',shield,fc2Rotation)
                self.PlacementList.append(ShieldFrontPlacement)
            xpl+=zbsp

