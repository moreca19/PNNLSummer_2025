#include <iostream>
#include "TGeoManager.h"
#include "TApplication.h"
#include "TCanvas.h"
#include "TGeoVolume.h"
#include "TColor.h"

//On Ragan Rae's macOS don't forget the parenthesis to compile
//g++ Macro.cpp $(root-config --cflags --libs) -lGdml -lGeom -o runGeo

using namespace std;


int main(int argc, char **argv)
{


    TApplication app("app", &argc, argv);
    TGeoManager::Import("dunevd_New.gdml");

    TGeoVolume* vol4 = gGeoManager->FindVolumeFast("IBeamSide");
    vol4->SetLineColor(kGray+2);
    vol4->SetFillColor(kGray+2);
    TGeoVolume* vol5 = gGeoManager->FindVolumeFast("IBeamTop");
    vol5->SetLineColor(kGray+2);
    vol5->SetFillColor(kGray+2);
    TGeoVolume* vol6 = gGeoManager->FindVolumeFast("IBeamBot");
    vol6->SetLineColor(kGray+2);
    vol6->SetFillColor(kGray+2);

    TGeoVolume* vol2 = gGeoManager->FindVolumeFast("BeltUni");
    vol2->SetLineColor(kRed);
    vol2->SetFillColor(kRed);
    TGeoVolume* vol3 = gGeoManager->FindVolumeFast("BeltHoleUni");
    vol3->SetLineColor(kRed);
    vol3->SetFillColor(kRed);

    TGeoVolume* vol = gGeoManager->FindVolumeFast("fShellLog");
    vol->SetLineColor(kOrange);
    vol->SetFillColor(kOrange);
    vol->SetTransparency(0);
    
    TGeoVolume* vol7 = gGeoManager->FindVolumeFast("FoamLog");
    vol7->SetLineColor(kCyan);
    vol7->SetFillColor(kCyan);

    TGeoVolume* vol8 = gGeoManager->FindVolumeFast("WoodLog");
    vol8->SetLineColor(kViolet);
    vol8->SetFillColor(kViolet);

    TGeoVolume* vol9 = gGeoManager->FindVolumeFast("ShellOutLog");
    vol9->SetLineColor(kPink);
    vol9->SetFillColor(kPink);

    TGeoVolume* vol10 = gGeoManager->FindVolumeFast("LArBoxLogical");
    vol10->SetLineColor(kTeal);
    vol10->SetFillColor(kTeal);
    

    gGeoManager->GetTopVolume()->Draw("same");

    app.Run();
    return 0;
}


