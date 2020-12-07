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

void make_pnES_base(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",10,10,1100,800);
  TString name;
  TH1D *ha_p,*ha_n, *ha;

//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/data1201a_00006_001_cali_am.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/data1130d_00005_001_cali_ba.root","READ");
  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/data1201a_00026_001_cali_co.root","READ");

//  name.Form("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/EnergySpectrum_combine_battery_all_co.pdf");
  name.Form("/Users/chiu.i-huan/Desktop/EnergySpectrum_temp.pdf");

  TTree* tree_a = (TTree*)fa->Get("tree");     
  tree_a->Draw("energy >> ha(300,0,150)","","");
  tree_a->Draw("energy_p >> ha_p(300,0,150)","","");
  tree_a->Draw("energy_n >> ha_n(300,0,150)","","");
  ha = (TH1D*)gDirectory->Get("ha");
  ha_p = (TH1D*)gDirectory->Get("ha_p");
  ha_n = (TH1D*)gDirectory->Get("ha_n");

  int maxbin = ha_n->GetMaximum();
  if (ha_p->GetMaximum() > maxbin) { maxbin = ha_p->GetMaximum(); }
  if (ha->GetMaximum() > maxbin) { maxbin = ha->GetMaximum(); }
  ha_n->SetMaximum(maxbin*1.1);

  ha_n->GetXaxis()->SetTitle("Energy [keV]");
  ha_n->GetYaxis()->SetTitle("Counts");

  ha->SetLineColor(1);
  ha_n->SetLineColor(kAzure);
  ha_p->SetLineColor(kPink);
//  ha_n->SetLineColor(kSpring-6);

  TLegend* leg = new TLegend(.55,.75,.85,.90);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(ha,  "#gamma (Matching)", "l");
  leg->AddEntry(ha_p,  "Pt side (Cathode)", "l");
  leg->AddEntry(ha_n,   "Al side (Anode)",   "l");

  TLine *line0 = new TLine(14.41,0,14.41,ha_n->GetMaximum());//Co
  TLine *line1 = new TLine(31,0,31,ha_n->GetMaximum());//Ba
  TLine *line2 = new TLine(59.5,0,59.5,ha_n->GetMaximum());//Am
  TLine *line3 = new TLine(81,0,81,ha_n->GetMaximum());//Ba
  TLine *line4 = new TLine(122.06,0,122.06,ha_n->GetMaximum());//Co
  line0->SetLineColorAlpha(1, 0.9);
  line1->SetLineColorAlpha(1, 0.9);
  line2->SetLineColorAlpha(1, 0.9);
  line3->SetLineColorAlpha(1, 0.9);
  line4->SetLineColorAlpha(1, 0.9);

  c1->cd();
  //gPad->SetLeftMargin(0.2);
  ha_n->Draw();
  ha_p->Draw("same");
  ha->Draw("same");

  leg->Draw("same");
  line0->Draw("same");
  line1->Draw("same");
  line2->Draw("same");
  line3->Draw("same");
  line4->Draw("same");

  c1->SaveAs(name.Data());

 }

