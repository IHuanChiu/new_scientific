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

void make_spectrum_si(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  char name[100] = "";

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",10,10,1600,800);
  TCanvas *c2 = new TCanvas("c2","Energy Spectum sum",10,10,800,800);
  TCanvas *c3 = new TCanvas("c3","Energy Spectum sub",10,10,800,800);
  c1->Divide(2,1);

  TFile *file; 
  TTree *mytree;
  TH1D *h_all_b, *h_all_a,*h_all_s, *h_all_pa, *h_all_na,*h_all_ps, *h_all_ps_m, *h_all_ns, *h_all_ns_m, *h_all_nb, *h_all_pb;
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

  //file = new TFile("/Users/chiu.i-huan/Desktop/Si_merge_fix.root","READ");
  file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/JPARC2020March_Si_sum.root","READ");
  //file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/JPARC2020March_Si_calibration_5_9_10_Am.root","READ");
  mytree = (TTree*)file->Get("tree");
     
//  mytree->SetBranchAddress("energy_p",e_p);
//  mytree->SetBranchAddress("energy_n",e_n);
//  mytree->SetBranchAddress("x",x);
//  mytree->SetBranchAddress("y",y);
//  mytree->SetBranchAddress("trigger",&trigger);
//  mytree->SetBranchAddress("nhitx",&nhitx);
//  mytree->SetBranchAddress("nhity",&nhity);

  TCut cut_signal = "((x < 8 && x > -5) && (y < 10 && y > -8))";
  TCut cut_bkg = "!((x < 14 && x > -14) && (y < 14 && y > -14))";
//  TCut cut_bkg = "!((x < 8))";
  TCut cut_basic = "((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630))";
  //TCut cut_basic = "1";
  
  c1->cd(1);
  mytree->Draw("energy_p >> h_all_pa(300,0,150)",cut_basic,"");
  mytree->Draw("energy_p >> h_all_ps(300,0,150)",cut_basic+cut_signal,"");
  mytree->Draw("energy_p >> h_all_pb(300,0,150)",cut_basic+cut_bkg,"");
  h_all_pa = (TH1D*)gDirectory->Get("h_all_pa");
  h_all_ps = (TH1D*)gDirectory->Get("h_all_ps");
  h_all_pb = (TH1D*)gDirectory->Get("h_all_pb"); 

  double nbkg = h_all_pb->GetEntries();
  double nsig = h_all_ps->GetEntries();
  double prate = nsig/nbkg;
  h_all_ps_m = (TH1D*)h_all_ps->Clone();
  h_all_ps_m->Scale(prate);
  h_all_ps->Add(h_all_ps_m,-1);
//  gPad->SetLogy(1);
  h_all_pa->SetTitle("Energy Spectrum");
  h_all_pa->GetXaxis()->SetTitle("energy [keV]");
  h_all_pa->GetYaxis()->SetTitle("Counts");
  h_all_pa->GetYaxis()->SetNdivisions(5,4,5);
  h_all_pa->SetMaximum(h_all_pa->GetMaximum()*1.2);
  h_all_pa->SetMinimum(0);
  h_all_pa->SetLineColor(1);
  h_all_pa->SetLineWidth(1);
  h_all_ps->SetLineColor(kPink+9);
  h_all_ps->SetLineWidth(1);
  h_all_pb->SetLineColor(kAzure-1);
  h_all_pb->SetLineWidth(1);
//  h_all_ps->GetYaxis()->SetLabelOffset(999);
//  h_all_ps->GetYaxis()->SetLabelSize(0);
//  h_all_ps->DrawNormalized("HIST");
//  h_all_pb->DrawNormalized("HIST same");
  h_all_pa->Draw("HIST");
  h_all_ps->Draw("HIST same");
  h_all_pb->Draw("HIST same");

  TLegend* leg = new TLegend(.65,.75,.85,.90);
  leg->AddEntry(h_all_pa,  "P-side sum", "l");
  leg->AddEntry(h_all_ps,  "P-side signal", "l");
  leg->AddEntry(h_all_pb,   "P-side bkg.",   "l");
  leg->Draw("same");


  c1->cd(2);
  mytree->Draw("energy_n >> h_all_na(300,0,150)",cut_basic,"");
  mytree->Draw("energy_n >> h_all_ns(300,0,150)",cut_basic+cut_signal,"");
  mytree->Draw("energy_n >> h_all_nb(300,0,150)",cut_basic+cut_bkg,"");
  h_all_na = (TH1D*)gDirectory->Get("h_all_na");
  h_all_ns = (TH1D*)gDirectory->Get("h_all_ns");
  h_all_nb = (TH1D*)gDirectory->Get("h_all_nb"); 

  nbkg = h_all_nb->GetEntries();
  nsig = h_all_ns->GetEntries();
  double nrate = nsig/nbkg;
  h_all_ns_m = (TH1D*)h_all_ns->Clone();
  h_all_ns_m->Scale(nrate);
  h_all_ns->Add(h_all_ns_m,-1);

//  gPad->SetLogy(1);
  h_all_na->SetTitle("Energy Spectrum");
  h_all_na->GetXaxis()->SetTitle("energy [keV]");
  h_all_na->GetYaxis()->SetTitle("Normalized");
  h_all_na->GetYaxis()->SetNdivisions(5,4,5);
  h_all_na->SetMaximum(h_all_na->GetMaximum()*1.2);
  h_all_na->SetMinimum(0);
  h_all_na->SetLineColor(1);
  h_all_na->SetLineWidth(1);
  h_all_ns->SetLineColor(kPink+9);
  h_all_ns->SetLineWidth(1);
  h_all_nb->SetLineColor(kAzure-1);
  h_all_nb->SetLineWidth(1);
//  h_all_ns->GetYaxis()->SetLabelOffset(999);
//  h_all_ns->GetYaxis()->SetLabelSize(0);
//  h_all_ns->DrawNormalized("HIST");
//  h_all_nb->DrawNormalized("HIST same");
  h_all_na->Draw("HIST");
  h_all_ns->Draw("HIST same");
  h_all_nb->Draw("HIST same");

  TLegend* leg2 = new TLegend(.65,.75,.85,.90);
  leg2->AddEntry(h_all_na,  "N-side sum", "l");
  leg2->AddEntry(h_all_ns,  "N-side signal", "l");
  leg2->AddEntry(h_all_nb,   "N-side bkg.",   "l");
  leg2->Draw("same");

  sprintf(name, "../../run/figs/hist_comparison_pn_e_si.pdf");
  c1->SaveAs(name);

  c2->cd();
  mytree->Draw("energy_p >> h_all_a(600,0,150)",cut_basic,"");
  mytree->Draw("energy_p >> h_all_s(600,0,150)",cut_basic+cut_signal,"");
  mytree->Draw("energy_p >> h_all_b(600,0,150)",cut_basic+cut_bkg,"");
  h_all_a = (TH1D*)gDirectory->Get("h_all_a");
  h_all_s = (TH1D*)gDirectory->Get("h_all_s");
  h_all_b = (TH1D*)gDirectory->Get("h_all_b"); 
  h_all_a->SetTitle("Energy Spectrum");
  h_all_a->GetXaxis()->SetTitle("energy [keV]");
  h_all_a->GetYaxis()->SetTitle("Counts/0.25 keV");
  h_all_a->GetXaxis()->CenterTitle();
  h_all_a->GetYaxis()->CenterTitle();
//  gPad->SetLeftMargin(0.2);
  h_all_a->GetYaxis()->SetNdivisions(5,4,5);
  h_all_a->SetMaximum(h_all_a->GetMaximum()*1.2);
  h_all_a->SetMinimum(0);
  h_all_a->SetLineColor(1);
  h_all_a->SetLineWidth(1);
//  h_all_s->SetLineColor(kPink+9);
  h_all_s->SetLineWidth(1);
  h_all_s->SetLineColor(kAzure-1);
  h_all_b->SetLineColor(kSpring-6);
  h_all_b->SetLineWidth(1);
  h_all_a->Draw("HIST");
  h_all_s->Draw("HIST same");
  h_all_b->Draw("HIST same");

  h_all_a->SetLineWidth(3);
  h_all_s->SetLineWidth(3);
  h_all_b->SetLineWidth(3);
  TLegend* legnew = new TLegend(.55,.65,.85,.90);
  legnew->AddEntry(h_all_a,  "Overall data", "l");
  legnew->AddEntry(h_all_s,  "Signal", "l");
  legnew->AddEntry(h_all_b,   "Bkg.",   "l");
  legnew->Draw("same");
  sprintf(name, "/Users/chiu.i-huan/Desktop/hist_comparison_all_si.pdf");
  c2->SaveAs(name);

  c3->cd();
  h_all_s->Add(h_all_b,-1);
  h_all_s->SetLineWidth(3);
  h_all_s->SetLineColor(1);
  h_all_s->SetTitle("Energy Spectrum; energy [keV]; Counts/0.25 keV");
  h_all_s->GetXaxis()->CenterTitle();
  h_all_s->GetYaxis()->CenterTitle();
  h_all_s->Draw("hist");
  sprintf(name, "/Users/chiu.i-huan/Desktop/hist_comparison_sub_si.pdf");
  c3->SaveAs(name);
 }

