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

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <TGraph.h>

#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"

int usage(void)
{
    std::string message = "Usage: ./make_plots <input root file>";
    std::cerr << message << std::endl;
    return 0;
}

void make_scpectum(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  char name[100] = "";

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",10,10,1600,800);
  c1->Divide(2,1);

  TFile *file; 
  TTree *mytree;
  TH1D *h_all_p, *h_all_n;
  TH2D* h_image;
  Double_t e_p[2048]; 
  Double_t e_n[2048]; 
  Int_t x[2048]; 
  Int_t y[2048]; 
  Int_t trigger; 
  Int_t nhitx; 
  Int_t nhity; 
  double e_max = 15;
  double e_min = 10;

//  h_all_p = new TH1D("energy_spectrum pside", "energy spectrum pside",100,0,100);
//  h_all_n = new TH1D("energy_spectrum nside", "energy spectrum nside",100,0,100);
//  h_image = new TH2D("image", "image",130,0,130,130,0,130);

  file = new TFile("../run/root/tranadc_dsd.root","READ");
  mytree = (TTree*)file->Get("tree");
     
//  mytree->SetBranchAddress("energy_p",e_p);
//  mytree->SetBranchAddress("energy_n",e_n);
//  mytree->SetBranchAddress("x",x);
//  mytree->SetBranchAddress("y",y);
//  mytree->SetBranchAddress("trigger",&trigger);
//  mytree->SetBranchAddress("nhitx",&nhitx);
//  mytree->SetBranchAddress("nhity",&nhity);

  TCut cut_energy = Form("energy_p > %f && energy_p < %f", e_min, e_max);
  TCut cut_basic = "(trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630)";
  
  c1->cd(1);
  mytree->Draw("energy_p >> h_all_p",cut_basic,"");
  mytree->Draw("energy_n >> h_all_n",cut_basic,"");
  gPad->SetLogy(1);
  h_all_p = (TH1D*)gDirectory->Get("h_all_p");
  h_all_n = (TH1D*)gDirectory->Get("h_all_n"); 
  h_all_p->SetTitle("Energy Spectrum");
  h_all_p->GetXaxis()->SetTitle("energy [keV]");
  h_all_p->GetYaxis()->SetTitle("Counts / 0.1 keV");
  h_all_p->SetMaximum(h_all_p->GetMaximum()*50);
  h_all_p->GetYaxis()->SetNdivisions(5,4,5);
  h_all_p->SetLineColor(kPink+9);
  h_all_p->SetLineWidth(3);
  h_all_p->Draw("H");
  h_all_n->SetLineColor(kAzure-1);
  h_all_n->SetLineWidth(3);
  h_all_n->Draw("H same");

  TLegend* leg = new TLegend(.65,.75,.85,.90);
  leg->AddEntry(h_all_p,  "P-side", "l");
  leg->AddEntry(h_all_n,   "N-side",   "l");
  leg->Draw("same");


  c1->cd(2);
  gPad->SetRightMargin(0.15);
  gPad->SetLogy(0);
  gPad->SetLogz(0);
  mytree->Draw("x:y >> h_image",cut_basic+cut_energy,"colz");
  h_image = (TH2D*)gDirectory->Get("h_image");
  h_image->GetXaxis()->SetTitle("p-side [ch]");
  h_image->GetYaxis()->SetTitle("n-side [ch]");
  gStyle->SetPalette(53);
  h_image->Draw("colz");
  
  sprintf(name, "../run/figs/hist_image_e.pdf");
  c1->SaveAs(name);

 }

