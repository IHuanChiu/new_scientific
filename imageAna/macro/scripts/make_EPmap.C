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
#include <stdlib.h>
#include <time.h>

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
  int index = 0;
  double x,y,z;
//  TFile* f_hist = new TFile("./Eavg_plots/Eavg_forMap_Co.root","READ");
  TFile* f_hist = new TFile("./Eavg_plots/Eavg_forMap_fullrange0p2keV.root","READ");
  TFile* fb_hist = new TFile("./Eavg_plots/Eavg_forMap_Ba.root","READ");

  double range = 0.2;
  int n_init=-30; int n_end=5;
  int nx = 3;// 0 & fitting value & end point
  int ny;// -7 < deltaE < 5
  ny=(n_end-(n_init))/range;
  TGraph2D *g = new TGraph2D(nx*ny);
  TGraph* gr;
  TH1D* h1;
  TH1D* h2;
  TSpectrum *s;
  Int_t nfound;
  Double_t *xpeaks;
  Double_t xp;
  Double_t yp;
  Double_t zp;
  Double_t ie;
  Double_t x_1d[3], y_1d[3];

  TFile* fout = new TFile("/Users/chiu.i-huan/Desktop/test_map.root","RECREATE");
  fout->cd();
  c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf[", "pdf");
  index = 0;
  for(int i = 0; i < ny; i++){
     ie=n_init+range*i;
     h1 = (TH1D*)f_hist->Get(Form("h%d_nx%d_ny%d",i,1,1));
     h2 = (TH1D*)fb_hist->Get(Form("h%d_nx%d_ny%d",i,1,1));
     s = new TSpectrum(1);
     s->SetResolution(1);
     nfound = s->Search(h1,0.01,"",0.005);
     xpeaks = s->GetPositionX();
     xp = xpeaks[0];//find peak
     std::cout << "index : " << i  << ","<<  ie << "< E <" << ie+range << std::endl;
     std::cout << " Found peak at : " << xp << std::endl;
//     if (xp > 150 || xp < 50) xp=122.1;
     h1->Draw("");
     c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf");
     for (int y = 0; y < 3; y++){//energy point 
//        std::cout  << ((double) rand() / (RAND_MAX + 1.0)) << std::endl;
        if (y==0){ yp = 0; zp= 0; x_1d[0] = 0; y_1d[0]=0;}
        if (y==1){ yp=xp; zp = 122.1 + ((double) rand() / (RAND_MAX + 1.0))*0.1; x_1d[1] = xp; y_1d[1]=122.1;}
        if (y==2){ yp=((xp-0)/(122.1+ ((double) rand() / (RAND_MAX + 1.0))*0.1 -0))*200; zp = 200; x_1d[2] = ((xp-0)/(122.1-0))*200; y_1d[2]=200;}
        g->SetPoint(index,yp,ie+0.5*range,zp);
        index++;
     }
     gr = new TGraph(3,x_1d,y_1d);
     gr->SetName(Form("Graph_map%d",i));
     gr->Write();     
  }
  c0->Print("/Users/chiu.i-huan/Desktop/map_fitting.pdf]", "pdf");
  g->SetName(Form("graph2d_%d_%d",1,1));
  g->SetTitle(";E_{avg.};#DeltaE;E_{exp.}");
  g->Write();
     
 }

