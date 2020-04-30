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
  TH1D *h_all_ps, *h_all_ns, *h_all_nb, *h_all_pb;
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

  file = new TFile("../../run/root/tranadc_dsd_20200307a_00072_001.root","READ");
  mytree = (TTree*)file->Get("tree");
     
//  mytree->SetBranchAddress("energy_p",e_p);
//  mytree->SetBranchAddress("energy_n",e_n);
//  mytree->SetBranchAddress("x",x);
//  mytree->SetBranchAddress("y",y);
//  mytree->SetBranchAddress("trigger",&trigger);
//  mytree->SetBranchAddress("nhitx",&nhitx);
//  mytree->SetBranchAddress("nhity",&nhity);

  TCut cut_energy = Form("energy_p > %f && energy_p < %f", e_min, e_max);
  TCut cut_signal_lv1 = "(Poi_y_lv1 > -5 && Poi_x_lv1 < 8 && Poi_x_lv1 > -7)";
  TCut cut_bkg_lv1 = "(Poi_y_lv1 < -5) || (Poi_y_lv1  > -5 && Poi_x_lv1 < -7) || (Poi_x_lv1 > 8 && Poi_y_lv1  > -5)";
  TCut cut_signal_lv2 = "(Poi_y_lv2 > -5 && Poi_x_lv2 < 8 && Poi_x_lv2 > -7)";
  TCut cut_bkg_lv2 = "(Poi_y_lv2 < -5) || (Poi_y_lv2  > -5 && Poi_x_lv2 < -7) || (Poi_x_lv2 > 8 && Poi_y_lv2  > -5)";
  TCut cut_basic = "((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253))";
  TCut cut_addition = "(nsignalx_lv1 != 0 && nsignaly_lv1 !=0)";
  
  c1->cd(1);
  mytree->Draw("E_p_lv1 >> h_all_ps(300,0,150)",cut_basic+cut_addition+cut_signal_lv1,"");
  mytree->Draw("E_p_lv1 >> h_all_pb(300,0,150)",cut_basic+cut_addition+cut_bkg_lv1,"");

//  gPad->SetLogy(1);
  h_all_ps = (TH1D*)gDirectory->Get("h_all_ps");
  h_all_pb = (TH1D*)gDirectory->Get("h_all_pb"); 
  h_all_ps->SetTitle("Energy Spectrum");
  h_all_ps->GetXaxis()->SetTitle("energy [keV]");
  h_all_ps->GetYaxis()->SetTitle("Normalized");
  h_all_ps->GetYaxis()->SetNdivisions(5,4,5);
  h_all_ps->SetMaximum(800);
  h_all_ps->SetMinimum(80);
  h_all_ps->SetLineColor(kPink+9);
  h_all_ps->SetLineWidth(3);
  h_all_pb->SetLineColor(kAzure-1);
  h_all_pb->SetLineWidth(3);
//  h_all_ps->GetYaxis()->SetLabelOffset(999);
//  h_all_ps->GetYaxis()->SetLabelSize(0);
//  h_all_ps->DrawNormalized("HIST");
//  h_all_pb->DrawNormalized("HIST same");
  h_all_ps->Draw("HIST");
  h_all_pb->Draw("HIST same");

  TLegend* leg = new TLegend(.65,.75,.85,.90);
  leg->AddEntry(h_all_ps,  "P-side signal", "l");
  leg->AddEntry(h_all_pb,   "P-side bkg.",   "l");
  leg->Draw("same");


  c1->cd(2);
  mytree->Draw("E_n_lv1 >> h_all_ns(300,0,150)",cut_basic+cut_addition+cut_signal_lv1,"");
  mytree->Draw("E_n_lv1 >> h_all_nb(300,0,150)",cut_basic+cut_addition+cut_bkg_lv1,"");

//  gPad->SetLogy(1);
  h_all_ns = (TH1D*)gDirectory->Get("h_all_ns");
  h_all_nb = (TH1D*)gDirectory->Get("h_all_nb"); 
  h_all_ns->SetTitle("Energy Spectrum");
  h_all_ns->GetXaxis()->SetTitle("energy [keV]");
  h_all_ns->GetYaxis()->SetTitle("Normalized");
  h_all_ns->GetYaxis()->SetNdivisions(5,4,5);
  h_all_ns->SetMaximum(800);
  h_all_ns->SetMinimum(80);
  h_all_ns->SetLineColor(kPink+9);
  h_all_ns->SetLineWidth(3);
  h_all_nb->SetLineColor(kAzure-1);
  h_all_nb->SetLineWidth(3);
//  h_all_ns->GetYaxis()->SetLabelOffset(999);
//  h_all_ns->GetYaxis()->SetLabelSize(0);
//  h_all_ns->DrawNormalized("HIST");
//  h_all_nb->DrawNormalized("HIST same");
  h_all_ns->Draw("HIST");
  h_all_nb->Draw("HIST same");

  TLegend* leg2 = new TLegend(.65,.75,.85,.90);
  leg2->AddEntry(h_all_ns,  "N-side signal", "l");
  leg2->AddEntry(h_all_nb,   "N-side bkg.",   "l");
  leg2->Draw("same");

//  gPad->SetRightMargin(0.15);
//  gPad->SetLogy(0);
//  gPad->SetLogz(0);
//  mytree->Draw("x:y >> h_image",cut_basic+cut_energy,"colz");
//  h_image = (TH2D*)gDirectory->Get("h_image");
//  h_image->GetXaxis()->SetTitle("N-side signal");
//  h_image->GetYaxis()->SetTitle("N-side bkg.");
//  gStyle->SetPalette(53);
//  h_image->Draw("colz");
  
  sprintf(name, "../../run/figs/hist_comparison_lv1.pdf");
  c1->SaveAs(name);

 }

