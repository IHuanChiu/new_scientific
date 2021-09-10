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

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",0,0,1100,800);
  TString name;
  TH1D *ha_p,*ha_n, *ha;
  
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/JPARC2020March_Si_sum.root","READ");//Si paper

//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_16to30_Osaka2mmCdTe_Co.root","READ");//Osaka 2mm CdTe
  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_00016_001_500n20_Co_Ecorr_watanabe.root","READ");//Osaka 2mm CdTe

//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/cdtedsd2_0607a_Ba.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/sample_particle_collimator_201215_2.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/sample_particle_201215_2.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/sample_blank_201215_2.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/sample_blank_collimator_201215_2.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/data1130d_00005_001_cali_ba3.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/data1201a_00022_001_cali_co3.root","READ");

  name.Form("/Users/chiu.i-huan/Desktop/EnergySpectrum_PNside.pdf");
//  TCut cut_basic = "((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630))";//Si 
  TCut cut_basic = "1";

  TTree* tree_a = (TTree*)fa->Get("tree");     
  tree_a->Draw("energy >> ha(3000,1,151)",    cut_basic,"");
  tree_a->Draw("energy_p >> ha_p(3000,1,151)",cut_basic,"");
  tree_a->Draw("energy_n >> ha_n(3000,1,151)",cut_basic,"");
  //tree_a->Draw("E_p_lv1 >> ha_p(3000,0,150)",cut_basic,"");
  //tree_a->Draw("E_n_lv1 >> ha_n(3000,0,150)",cut_basic,"");
  ha = (TH1D*)gDirectory->Get("ha");
  ha_p = (TH1D*)gDirectory->Get("ha_p");
  ha_n = (TH1D*)gDirectory->Get("ha_n");

  int maxbin = ha_n->GetMaximum();
  if (ha_p->GetMaximum() > maxbin) { maxbin = ha_p->GetMaximum(); }
  if (ha->GetMaximum() > maxbin) { maxbin = ha->GetMaximum(); }
  ha_n->SetMaximum(maxbin*1.1);

  ha_n->GetXaxis()->SetTitle("Energy [keV]");
  ha_n->GetYaxis()->SetTitle("Counts/0.05 keV");
  ha->GetXaxis()->SetTitle("Energy [keV]");
  ha->GetYaxis()->SetTitle("Counts/0.05 keV");

  ha->SetLineColor(1);
  ha_n->SetLineColor(kAzure);
  ha_p->SetLineColor(kPink);
//  ha_n->SetLineColor(kSpring-6);

  TLegend* leg = new TLegend(.25,.65,.6,.90);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(ha,  "Recon. E", "l");
  leg->AddEntry(ha_p,  "Pt side (Cathode)", "l");
  leg->AddEntry(ha_n,   "Al side (Anode)",   "l");

  TLine *lineCo1 = new TLine(14.41,0,14.41,ha_n->GetMaximum());//Co
  TLine *lineCo2 = new TLine(122.06,0,122.06,ha_n->GetMaximum());//Co
  TLine *lineAm1 = new TLine(13.94,0,13.94,ha_n->GetMaximum());//Am
  TLine *lineAm2 = new TLine(20.8,0,20.8,ha_n->GetMaximum());//Am
  TLine *lineAm3 = new TLine(59.5,0,59.5,ha_n->GetMaximum());//Am
  TLine *lineBa1 = new TLine(31,0,31,ha_n->GetMaximum());//Ba
  TLine *lineBa2 = new TLine(35,0,35,ha_n->GetMaximum());//Ba
  TLine *lineBa3 = new TLine(81,0,81,ha_n->GetMaximum());//Ba
  TLine *line5 = new TLine(75.22,0,75.22,ha_n->GetMaximum());//C 75.22
  TLine *line6 = new TLine(134.35,0,134.35,ha_n->GetMaximum());//O 134.35
  TLine *line7 = new TLine(24.86,0,24.86,ha_n->GetMaximum());//O 24.86

  lineCo1->SetLineColorAlpha(1, 0.9);
  lineCo2->SetLineColorAlpha(1, 0.9);
  lineAm1->SetLineColorAlpha(2, 0.7);
  lineAm2->SetLineColorAlpha(2, 0.7);
  lineAm3->SetLineColorAlpha(2, 0.7);
  lineBa1->SetLineColorAlpha(4, 0.7);
  lineBa2->SetLineColorAlpha(4, 0.7);
  lineBa3->SetLineColorAlpha(4, 0.7);

  line5->SetLineColorAlpha(1, 0.9);
  line6->SetLineColorAlpha(1, 0.9);
  line7->SetLineColorAlpha(1, 0.9);

  c1->cd();
  gPad->SetLeftMargin(0.15);
  ha_n->Draw();
  ha_p->Draw("same");
  ha->Draw("same");

  leg->Draw("same");

//  lineCo1->Draw("same");
//  lineCo2->Draw("same");
//  lineAm1->Draw("same");
//  lineAm2->Draw("same");
//  lineAm3->Draw("same");
//  lineBa1->Draw("same");
//  lineBa2->Draw("same");
//  lineBa3->Draw("same");

//  line5->Draw("same");
//  line6->Draw("same");
//  line7->Draw("same");

  c1->SaveAs(name.Data());

 }

