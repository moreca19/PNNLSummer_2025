 
  double eps(0.215);
  const double ht =  fht ; //m
  const double st =  fst + 0.031 ; //m have to be out from the belts left, right

  // These are the y-locations of centers of shield panels, not the actual holes.
  const double yTopHole = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-(4.0-1.)*fIPortSpacing + 9*fIPortHoleRad)/2.;
  const double yBotHole = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-(0.0-1.)*fIPortSpacing + 9*fIPortHoleRad)/2.;
  const double y1HoleUp = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-(2.0-1.)*fIPortSpacing + 9*fIPortHoleRad)/2.;;
  const double yTop = (ht-eps);
  
  const double BlockWidth = fSpacing-fIFlangeWaist-0.001 - 0.050;
  const double BlockHeight = fIPortSpacing - 0.050;
  const double BlockHeightTop =  BlockHeight*0.63 ;
  std::cout << "BlockHeight,Top are " << BlockHeight << ", " << BlockHeightTop << std::endl;
  const double BlockHeightBot = BlockHeight*0.15;

 
 const double zbsp = fSpacing; //m
  double zpl(zbsp/2.);
  double xpl(0.);

  int cpIT(0), cpIB(0), cpIL(0), cpIR(0),cpBlt(0);  

  for (size_t ii=0;ii<=19;ii++) {

    // left and right sides. bot 3 y-levels just below the port hole heights, top one at the top
       for (size_t jj=0;jj<5;jj++) {
      double y;
      G4LogicalVolume* shield = ShieldBlockLog ;
     // loop on y bot to top for these  two side walls -- 2 of 3 is nohole
      if (jj==3) { // top 
	y = yTopHole + BlockHeight/2. + BlockHeightTop/2. + 0.050;
	shield = ShieldBlockTopLog;

      }
      if (jj==2) { // bot hole
	y = yBotHole;

      }
      if (jj==1) { // up 1 hole
	y = y1HoleUp;
      }
      if (jj==0) { // top hole
	y = yTopHole;
      }
      if (jj==4) { // bottom 
	y = yBotHole - BlockHeight/2. - 0.5*BlockHeightBot - 0.050 ;
	shield = ShieldBlockBotLog;

      }

      // This next line is doing a lot of work!! 
      if (jj==0 || jj == 3) continue; // EC, 2-May-2025, drop upper shields.
      
      new G4PVPlacement(0,G4ThreeVector(-st*m,y*m,(-zpl)*m),"ShieldLeft",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(0,G4ThreeVector( st*m,y*m,(-zpl)*m),"ShieldRight",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(0,G4ThreeVector(-st*m,y*m,(+zpl)*m),"ShieldLeft",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(0,G4ThreeVector( st*m,y*m,(+zpl)*m),"ShieldRight",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      
    }
    zpl+=zbsp;
  }


  // Front face, back face
  int cpBF(0), cpBBk(0);
  xpl = zbsp/2.; //m
  zpl = fzpl/2.; //m
  for (size_t ii=0;ii<5;ii++) {

       for (size_t jj=0;jj<5;jj++) {
      double y;
      G4LogicalVolume* shield = ShieldBlockLog ;
     // loop on y bot to top for these  two side walls -- 2 of 3 is nohole
      if (jj==3) { // top 
	y = yTopHole + BlockHeight/2. + BlockHeightTop/2. + 0.050;
	shield = ShieldBlockTopLog;

      }
      if (jj==2) { // bot hole
	y = yBotHole;

      }
      if (jj==1) { // up 1 hole
	y = y1HoleUp;
      }
      if (jj==0) { // top hole
	y = yTopHole;
      }
      if (jj==4) { // bottom 
	y = yBotHole - BlockHeight/2. - 0.5*BlockHeightBot - 0.050 ;
	shield = ShieldBlockBotLog;
      }

      new G4PVPlacement(fc2,G4ThreeVector(-xpl*m,y*m,(-zpl)*m),"ShieldBack",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBBk++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc2,G4ThreeVector( xpl*m,y*m,(-zpl)*m),"ShieldBack",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBBk++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc2,G4ThreeVector(-xpl*m,y*m,(+zpl)*m),"ShieldFront",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBF++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc2,G4ThreeVector( xpl*m,y*m,(+zpl)*m),"ShieldFront",
							 shield,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBF++, // copyNo
							 true); //check for overlaps
      
    }
    
    xpl+=zbsp;
  }
  
