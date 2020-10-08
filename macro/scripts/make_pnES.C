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

void make_pnES(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  char name[100] = "";

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",10,10,800,800);
  TCanvas *c2 = new TCanvas("c2","",10,10,800,800);

  TH1D *ha_p,*ha_n,*hb_p,*hb_n,*hc_p,*hc_n,*ha,*hb,*hc;

  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdtedsd_2020b_0720a_Amsource_calimerge1008.root","READ");
  TFile* fb = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdtedsd_2020b_0720a_Basource_calimerge1008.root","READ");
  TFile* fc = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdtedsd_2020b_0720a_Cosource_calimerge1008.root","READ");
  TTree* tree_a = (TTree*)fa->Get("tree");
  TTree* tree_b = (TTree*)fb->Get("tree");
  TTree* tree_c = (TTree*)fc->Get("tree");
     
  tree_a->Draw("energy >> ha(600,0,150)","","");
  tree_b->Draw("energy >> hb(600,0,150)","","");
  tree_c->Draw("energy >> hc(600,0,150)","","");
  tree_a->Draw("energy_p >> ha_p(600,0,150)","","");
  tree_b->Draw("energy_p >> hb_p(600,0,150)","","");
  tree_c->Draw("energy_p >> hc_p(600,0,150)","","");
  tree_a->Draw("energy_n >> ha_n(600,0,150)","","");
  tree_b->Draw("energy_n >> hb_n(600,0,150)","","");
  tree_c->Draw("energy_n >> hc_n(600,0,150)","","");
  ha = (TH1D*)gDirectory->Get("ha");
  hb = (TH1D*)gDirectory->Get("hb");
  hc = (TH1D*)gDirectory->Get("hc"); 
  ha_p = (TH1D*)gDirectory->Get("ha_p");
  hb_p = (TH1D*)gDirectory->Get("hb_p");
  hc_p = (TH1D*)gDirectory->Get("hc_p"); 
  ha_n = (TH1D*)gDirectory->Get("ha_n");
  hb_n = (TH1D*)gDirectory->Get("hb_n");
  hc_n = (TH1D*)gDirectory->Get("hc_n"); 

  double n_h = ha->GetMaximum()+hb->GetMaximum()+hc->GetMaximum();
  double n_hpn = ha_p->GetMaximum()+hb_p->GetMaximum()+hc_p->GetMaximum()+ha_n->GetMaximum()+hb_n->GetMaximum()+hc_n->GetMaximum();
  ha->SetMaximum((hb->GetMaximum())*1.1);
  ha_p->SetMaximum((hb->GetMaximum())*1.1);

  ha->SetLineColor(kAzure);
  hb->SetLineColor(kPink);
  hc->SetLineColor(kSpring);

  ha_p->SetLineColor(kAzure-6);
  hb_p->SetLineColor(kPink-6);
  hc_p->SetLineColor(kSpring-6);

  ha_n->SetLineColor(kAzure-9);
  hb_n->SetLineColor(kPink-9);
  hc_n->SetLineColor(kSpring-9);

  TLegend* leg = new TLegend(.65,.75,.85,.90);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(ha,  "Am-241", "l");
  leg->AddEntry(hb,  "Ba-133", "l");
  leg->AddEntry(hc,   "Co-57",   "l");

  TLegend* leg2 = new TLegend(.65,.65,.90,.90);
  leg2->SetFillColor(0);
  leg2->SetLineColor(0);
  leg2->SetBorderSize(0);
  leg2->AddEntry(ha_p,  "p-side, Am-241", "l");
  leg2->AddEntry(ha_n,  "n-side, Am-241", "l");
  leg2->AddEntry(hb_p,  "p-side, Ba-133", "l");
  leg2->AddEntry(hb_n,  "n-side, Ba-133", "l");
  leg2->AddEntry(hc_p,  "p-side, Co-57",   "l");
  leg2->AddEntry(hc_n,  "n-side, Co-57",   "l");

  TLine *line0 = new TLine(14.41,0,14.41,hb->GetMaximum());//Co
  TLine *line1 = new TLine(31,0,31,hb->GetMaximum());//Ba
  TLine *line2 = new TLine(59.5,0,59.5,hb->GetMaximum());//Am
  TLine *line3 = new TLine(81,0,81,hb->GetMaximum());//Ba
  TLine *line4 = new TLine(122.06,0,122.06,hb->GetMaximum());//Co
  line0->SetLineColorAlpha(1, 0.9);
  line1->SetLineColorAlpha(1, 0.9);
  line2->SetLineColorAlpha(1, 0.9);
  line3->SetLineColorAlpha(1, 0.9);
  line4->SetLineColorAlpha(1, 0.9);

  c1->cd();
  ha->Draw();
  hb->Draw("same");
  hc->Draw("same");

  leg->Draw("same");
  line0->Draw("same");
  line1->Draw("same");
  line2->Draw("same");
  line3->Draw("same");
  line4->Draw("same");

  c2->cd();
  ha_p->Draw();
  hb_p->Draw("same");
  hc_p->Draw("same");
  ha_n->Draw("same");
  hb_n->Draw("same");
  hc_n->Draw("same");
  leg2->Draw("same");
  line0->Draw("same");
  line1->Draw("same");
  line2->Draw("same");
  line3->Draw("same");
  line4->Draw("same");

  c1->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/EnergySpectrum_combine_all.pdf");
  c2->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/EnergySpectrum_combine_pn.pdf");

 }

