void DetectorConstruction::Belts()
{
  // Just two belts, one with a hole, one without.

  const double ht =  fht ; //m
  const double st =  fst ; //m

  G4Box* BeltFlange = new G4Box("BeltFlange", ((0.200)/2.0)*m, (fIFlangeWaist/2.0)*m, (fSpacing/2.-fIFlangeWaist/2.-0.001)*m ); 
  G4Box* BeltMid = new G4Box("BeltMid",(fIFlangeWaist/2.0)*m, (fIFlangeHeight/4.)*m, (fSpacing/2.-fIFlangeWaist/2.-0.001)*m);
  G4Tubs* IBeamPort = new G4Tubs("BeltPortHole",0.,0.25*m,(fIFlangeThick/2.0)*m,0.0,2.0*CLHEP::pi); // 0.6m??
  G4RotationMatrix* fc = new G4RotationMatrix();
  G4RotationMatrix* fc3 = new G4RotationMatrix();
  G4ThreeVector* axisfc = new G4ThreeVector(0.0,0.0,1.0);
  G4RotationMatrix* fc2 = new G4RotationMatrix();
  G4ThreeVector* axisfc2 = new G4ThreeVector(0.0,1.0,0.0);
  G4ThreeVector* axisfc3 = new G4ThreeVector(1.0,0.0,0.0);
  fc->rotate(CLHEP::pi/2.,axisfc);
  fc2->rotate(CLHEP::pi/2.,axisfc2);
  fc3->rotate(CLHEP::pi/2.,axisfc);
  fc3->rotate(CLHEP::pi/2.,axisfc3);
  G4SubtractionSolid* BeltHole = new G4SubtractionSolid("BeltHole", BeltMid, IBeamPort, fc2, G4ThreeVector(0.0,0.0,0.0));

  HepGeom::Transform3D tnull, tr1, tr2;
  tnull = HepGeom::TranslateY3D(0.0);
  tr1 = HepGeom::TranslateY3D( (fIFlangeHeight/4.0)*m);
  tr2 = HepGeom::TranslateY3D(-(fIFlangeHeight/4.0)*m);

  G4MultiUnion* BeltHoleUni = new G4MultiUnion("BeltHoleUni");
  BeltHoleUni->AddNode(BeltHole, tnull);
  BeltHoleUni->AddNode(BeltFlange,tr1);
  BeltHoleUni->AddNode(BeltFlange,tr2);
  BeltHoleUni->Voxelize();
  G4LogicalVolume* BeltHoleUniLog = new G4LogicalVolume(BeltHoleUni, fDUNESteel, "BeltHoleUniLog");
  G4MultiUnion* BeltUni = new G4MultiUnion("BeltUni");
  BeltUni->AddNode(BeltMid, tnull);
  BeltUni->AddNode(BeltFlange,tr1);
  BeltUni->AddNode(BeltFlange,tr2);
  BeltUni->Voxelize();
  G4LogicalVolume* BeltUniLog = new G4LogicalVolume(BeltUni, fDUNESteel, "BeltUniLog");
  G4VisAttributes* simpleBoxAtt= new G4VisAttributes(G4Colour::Cyan());
  G4VisAttributes* simpleBoxHoleAtt= new G4VisAttributes(G4Colour::Brown());
  simpleBoxAtt->SetDaughtersInvisible(true);
  simpleBoxAtt->SetForceSolid(true);
  simpleBoxAtt->SetForceAuxEdgeVisible(true);
  simpleBoxHoleAtt->SetDaughtersInvisible(true);
  simpleBoxHoleAtt->SetForceSolid(true);
  simpleBoxHoleAtt->SetForceAuxEdgeVisible(true);
  BeltUniLog->SetVisAttributes(simpleBoxAtt);
  BeltHoleUniLog->SetVisAttributes(simpleBoxHoleAtt);

  
  const double zbsp = fSpacing; //m
  double zpl(zbsp/2.);
  double xpl(0.);
  double eps(0.215);
  int cpIT(0), cpIB(0), cpIL(0), cpIR(0),cpBlt(0);  
  // Top, bottom

 
  for (size_t ii=0;ii<=19 /*20*/;ii++) 
  {
    // loop on x for top and bottom
    for (int jj=-5;jj<5;jj++) 
	{

      new G4PVPlacement(0,G4ThreeVector((jj+0.5)*zbsp*m,(-ht+eps)*m,(zpl)*m),"BeltBot",
							 BeltHoleUniLog,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpIB++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(0,G4ThreeVector((jj+0.5)*zbsp*m,(-ht+eps)*m,(-zpl)*m),"BeltBot",
							 BeltHoleUniLog,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpIB++, // copyNo
							 true); //check for overlaps
      // belts dodge the flanges on top
      if (std::abs(jj)==1 || std::abs(jj)==2 || std::abs(jj)==4) { 
	new G4PVPlacement(0,G4ThreeVector((jj+0.5)*zbsp*m,(ht-eps)*m,(zpl)*m),"BeltTop",
							 BeltUniLog,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpIT++, // copyNo
							 true); //check for overlaps
	new G4PVPlacement(0,G4ThreeVector((jj+0.5)*zbsp*m,(ht-eps)*m,(-zpl)*m),"BeltTop",
							 BeltUniLog,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpIT++, // copyNo
							 true); //check for overlaps
      }

    }
    // left and right sides. bot 3 y-levels just below the port hole heights, top one at the top
    for (size_t jj=0;jj<4;jj++) {
      double y;
      G4LogicalVolume* belt = BeltHoleUniLog;
     // loop on y bot to top for these  two side walls -- 2 of 3 is nohole
      if (jj==3) { // top 
	y = (ht-eps)*m ;
	belt = BeltUniLog;
	if (ii % 3)  belt = BeltHoleUniLog;
      }
      if (jj==2) { // bot hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.+0.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
      }
      if (jj==1) { // up 1 hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-2.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
	belt = BeltUniLog;
	if ((ii+1) % 3)  belt = BeltHoleUniLog;
      }
      if (jj==0) { // top hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-4.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
	belt = BeltUniLog;
	if ((ii+2) % 3)  belt = BeltHoleUniLog;
      }

      if (ii==20) { // nohole on extreme ends for all four levels
	belt = BeltUniLog;
      }

      new G4PVPlacement(fc,G4ThreeVector(-st*m,y,(-zpl)*m),"BeltLeft",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc,G4ThreeVector( st*m,y,(-zpl)*m),"BeltRight",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc,G4ThreeVector(-st*m,y,(+zpl)*m),"BeltLeft",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBlt++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc,G4ThreeVector( st*m,y,(+zpl)*m),"BeltRight",
							 belt,      //its logical volume   
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
  zpl = fzpl/2.+0.100; //m
  for (size_t ii=0;ii<5;ii++) 
  {
  for (size_t jj=0;jj<4;jj++) 
  {
      double y;
      G4LogicalVolume* belt = BeltHoleUniLog;
     // loop on y bot to top for these  two side walls -- 2 of 3 is nohole
      if (jj==3) { // top 
	y = ht*m;
	belt = BeltUniLog;
	if (ii % 3)  belt = BeltHoleUniLog;
      }
      if (jj==2) { // bot hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.+0.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
      }
      if (jj==1) { // up 1 hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-2.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
	belt = BeltUniLog;
	if ((ii+1) % 3)  belt = BeltHoleUniLog;
      }
      if (jj==0) { // top hole
	y = -(fISideLength/2.+fIFlangeHeight/2.-5907./1000.-4.0*fIPortSpacing + 9*fIPortHoleRad)/2.*m;
	belt = BeltUniLog;
	if ((ii+2) % 3)  belt = BeltHoleUniLog;
      }

      if (ii==20) { // nohole on extreme ends for all four levels
	belt = BeltUniLog;
      }

      new G4PVPlacement(fc3,G4ThreeVector(-xpl*m,y,(-zpl)*m),"BeltBack",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBBk++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc3,G4ThreeVector( xpl*m,y,(-zpl)*m),"BeltBack",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBBk++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc3,G4ThreeVector(-xpl*m,y,(+zpl)*m),"BeltFront",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBF++, // copyNo
							 true); //check for overlaps
      new G4PVPlacement(fc3,G4ThreeVector( xpl*m,y,(+zpl)*m),"BeltFront",
							 belt,      //its logical volume   
							 fPhysOuterAir,           //its mother  volume
							 false,                 //no boolean operation
							 cpBF++, // copyNo
							 true); //check for overlaps
      
    }
    xpl+=zbsp;
  }



}