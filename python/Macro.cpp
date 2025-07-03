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
    TGeoManager::Import("dunevd_v10.gdml");

    TGeoVolume* vol = gGeoManager->FindVolumeFast("fShellLog");
    vol->SetLineColor(kOrange);
    vol->SetFillColor(kOrange);
    vol->SetTransparency(0);

    cout << "fShellVoume is the blue one" << endl;
 
    TGeoVolume* vol2 = gGeoManager->FindVolumeFast("BeltUni");
    vol2->SetLineColor(kBlack);
    vol2->SetFillColor(kBlack);

    cout << "BeltUni volume is the black one" << endl;

    TGeoVolume* vol3 = gGeoManager->FindVolumeFast("BeltHoleUni");
    vol3->SetLineColor(kRed);
    vol3->SetFillColor(kRed);

    cout << "BeltHoleUni volume is the red one" << endl;

    TGeoVolume* vol4 = gGeoManager->FindVolumeFast("IBeamSide");
    vol4->SetLineColor(kGreen);
    vol4->SetFillColor(kGreen);
    TGeoVolume* vol5 = gGeoManager->FindVolumeFast("IBeamTop");
    vol5->SetLineColor(kGreen);
    vol5->SetFillColor(kGreen);
    TGeoVolume* vol6 = gGeoManager->FindVolumeFast("IBeamBot");
    vol6->SetLineColor(kGreen);
    vol6->SetFillColor(kGreen);

    cout << "all of the Ibeams are the green ones" << endl;
    cout << "gets to here" << endl;
    TGeoVolume* vol7 = gGeoManager->FindVolumeFast("FoamLog");
    vol7->SetLineColor(kBlack);
    vol7->SetFillColor(kBlack);

    TGeoVolume* vol8 = gGeoManager->FindVolumeFast("WoodLog");
    vol8->SetLineColor(kViolet);
    vol8->SetFillColor(kViolet);
    

    gGeoManager->GetTopVolume()->Draw("same");

    app.Run();
    return 0;
}



#include <iostream>
#include "TGeoManager.h"
#include "TApplication.h"
#include "TCanvas.h"
#include "TGeoVolume.h"
#include "TColor.h"

using namespace std;


int main(int argc, char **argv)
{


    TApplication app("app", &argc, argv);
    TGeoManager::Import("dunevd_v10.gdml");

    TGeoVolume* vol = gGeoManager->FindVolumeFast("fShellLog");
    vol->SetLineColor(kOrange);
    vol->SetFillColor(kOrange);

    TGeoVolume* vol1 = gGeoManager->FindVolumeFast("volWorld");
    vol1->SetLineColor(kGreen);
    vol1->SetFillColor(kGreen);
    

    // cout << "fShellVoume is the blue one" << endl;
 
    TGeoVolume* vol2 = gGeoManager->FindVolumeFast("BeltUni");
    vol2->SetLineColor(kBlack);
    vol2->SetFillColor(kBlack);

    cout << "BeltUni volume is the black one" << endl;

    TGeoVolume* vol3 = gGeoManager->FindVolumeFast("BeltHoleUni");
    vol3->SetLineColor(kRed);
    vol3->SetFillColor(kRed);

    cout << "BeltHoleUni volume is the red one" << endl;

    TGeoVolume* vol4 = gGeoManager->FindVolumeFast("IBeamSide");
    vol4->SetLineColor(kGreen);
    vol4->SetFillColor(kGreen);
    vol4->SetTransparency(0);
    vol4->Draw("sh");
    TGeoVolume* vol5 = gGeoManager->FindVolumeFast("IBeamTop");
    vol5->SetLineColor(kGreen);
    vol5->SetFillColor(kGreen);
    TGeoVolume* vol6 = gGeoManager->FindVolumeFast("IBeamBot");
    vol6->SetLineColor(kGreen);
    vol6->SetFillColor(kGreen);

    cout << "all of the Ibeams are the green ones" << endl;
    cout << "gets to here" << endl;
    TGeoVolume* vol7 = gGeoManager->FindVolumeFast("FoamLog");
    vol7->SetLineColor(kBlack);
    vol7->SetFillColor(kBlack);

    TGeoVolume* vol8 = gGeoManager->FindVolumeFast("WoodLog");
    vol8->SetLineColor(kViolet);
    vol8->SetFillColor(kViolet);
    

    gGeoManager->GetTopVolume()->Draw("sh");

    app.Run();
    return 0;
}

