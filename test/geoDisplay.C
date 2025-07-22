//#include "TGLViewer.h"
#include "TGeoManager.h"
//#include "TGLRnrCtx.h"
#include "TVirtualPad.h"
#include "TROOT.h"
#include "TSystem.h"

void geoDisplay(TString filename, Int_t VisLevel)
{

        gSystem->Load("libRGL");
        gSystem->Load("libGeom");
        gSystem->Load("libGeomPainter");


	TGeoManager *geo = TGeoManager::Import(filename);
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();
	geo->SetVisOption(1);
	geo->SetVisLevel(VisLevel);
	geo->GetTopVolume()->Print();
	geo->GetTopVolume()->Draw("ogl");

	gPad->Update();
	
	//TGLViewer * v = (TGLViewer *)gPad->GetViewer3D();
	//v->SetStyle(TGLRnrCtx::kOutline);
	//v->SetSmoothPoints(kTRUE);
	//v->SetLineScale(0.5);
	//	v->UseDarkColorSet();
	//v->UpdateScene();
}


geoDisplay("dunevd_v10.gdml",5);
