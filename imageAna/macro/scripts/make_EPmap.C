#include <TROOT.h>
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "THStack.h"
#include "TLegend.h"
#include "TChain.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2.h"
#include "TH3.h"
#include "THn.h"
#include "TCanvas.h"
#include "TLatex.h"

#include "TH1F.h"
#include "TDirectory.h"
#include "TDirectoryFile.h"
#include "TArrow.h"
#include "TRef.h"
#include "TApplication.h"
#include "TError.h"
#include "TMath.h"
#include "TAxis.h"
#include "TStyle.h"
#include "TLine.h"
#include "TSpectrum.h"

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <TGraph.h>

#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"

void make_EPmap(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  TCanvas *c0 = new TCanvas("temp canvas","temp canvas",10,10,800,800);
  int nx = 2;// 0 & fitting value
  int ny = 12;// -7 < deltaE < 5
  int index = 0;
  double x,y,z;

  TGraph2D *g = new TGraph2D(nx*ny);
  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_16to30_Osaka2mmCdTe_Co.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_6to8_merge_500n20_Am.root","READ");
  TTree* tree = (TTree*)fa->Get("tree");
  TH1D* h1;
  TSpectrum *s;
  Int_t nfound;
  Double_t *xpeaks;
  Double_t xp;
  Double_t yp;
  Double_t zp;

  c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf[", "pdf");
  index = 0;
  for(int ie = -7 ; ie < 5; ie++){
     tree->Draw("(E_p_lv2+E_n_lv2)/2 >> h1(150,0,150)",Form("(E_p_lv2-E_n_lv2)/2 > %d && (E_p_lv2-E_n_lv2)/2 < %d && nsignalx_lv2 == 1 && nsignaly_lv2 == 1",ie,ie+1),"");
     h1 = (TH1D*)gDirectory->Get("h1");
     s = new TSpectrum(1);
     s->SetResolution(1);
     nfound = s->Search(h1,0.01,"",0.005);
     xpeaks = s->GetPositionX();
     xp = xpeaks[0];//find peak
     std::cout << ie << "< E <" << ie+1 << std::endl;
     std::cout << " Found peak at : " << xp << std::endl;
     h1->Draw("");
     c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf");
     for (int y = 0; y < 3; y++){//energy point 
        if (y==0){ yp = 0; zp= 0;}
        if (y==1){ yp=xp; zp = 122.1;}
        if (y==2){ yp=((xp-0)/(122.1-0))*200; zp = 200;}
        g->SetPoint(index,ie+0.5,yp,zp);
        index++;
     }
  }
  c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf]", "pdf");
  TFile* fout = new TFile("/Users/chiu.i-huan/Desktop/test_map.root","RECREATE");
  fout->cd();
  g->Write();
     
 }

