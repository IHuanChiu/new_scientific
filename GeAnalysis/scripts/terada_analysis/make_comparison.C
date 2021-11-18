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

void make_comparison(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  TCanvas *c1 = new TCanvas("c1","Energy Spectum",0,0,1100,800);
  TString name;
  TH1D *h1,*h2;
 /*
  TFile* f1 = new TFile("../data/JPARC_2020Dec/particle_merge.root","READ");//Signal (16168+3693+60219)
  TFile* f2 = new TFile("../data/JPARC_2020Dec/blank_merge.root","READ");//Blank (44879+45721)

  double bin_down=60;
  double bin_up=80;
  int nbin=200;
  name.Form("/Users/chiu.i-huan/Desktop/EnergySpectrum_Ge_comparison_%dto%d.pdf",int(bin_down),int(bin_up));
  TCut cut_basic = "1";
  TTree* tree1 = (TTree*)f1->Get("tree");     
  TTree* tree2 = (TTree*)f2->Get("tree");     
  tree1->Draw(Form("energy >> h1(%d,%f,%f)",nbin,bin_down,bin_up),cut_basic,"");
  tree2->Draw(Form("energy >> h2(%d,%f,%f)",nbin,bin_down,bin_up),cut_basic,"");
  h1 = (TH1D*)gDirectory->Get("h1");
  h2 = (TH1D*)gDirectory->Get("h2");
  int scale_h1=16168+3693+60219;
  int scale_h2=44879+45721;
  h1->Scale(1./scale_h1);
  h2->Scale(1./scale_h2);
  h1->GetXaxis()->SetTitle("Energy [keV]");
  h1->GetYaxis()->SetTitle("Counts/0.2 keV/sec.");
  h2->GetXaxis()->SetTitle("Energy [keV]");
  h2->GetYaxis()->SetTitle("Counts/0.2 keV/sec.");
  h1->GetXaxis()->CenterTitle();
  h1->GetYaxis()->CenterTitle();
  h1->SetLineColor(2);
  h2->SetLineColor(4);
  TLegend* leg = new TLegend(.35,.75,.6,.90);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(h1,  "Particle", "l");
  leg->AddEntry(h2,   "Blank",   "l");
  c1->cd();
  gPad->SetLeftMargin(0.15);
  h2->Draw("hist");
  h1->Draw("hist same");
  leg->Draw("same");// */

// /*
  TFile* f1 = new TFile("/Users/chiu.i-huan/Desktop/202106_self_Ba.root","READ");//Signal
  TFile* f2 = new TFile("/Users/chiu.i-huan/Desktop/ri_ba133_simulation_specfile.root","READ");//Blank 
  name.Form("/Users/chiu.i-huan/Desktop/EnergySpectrum_Ge_comparison_SimvsData.pdf");
  TTree* tree1 = (TTree*)f1->Get("tree");     
  tree1->Draw("energy_ori >> h1(6800, 10,180)","detID == 1 || detID == 5 || detID == 4","");
  h1 = (TH1D*)gDirectory->Get("h1");
  h2=(TH1D*)f2->Get("spec_det_all");
//  h2=(TH1D*)f2->Get("spec_det1");//5
//  h2=(TH1D*)f2->Get("spec_det2");//4
//  h2=(TH1D*)f2->Get("spec_det3");//3
//  h2=(TH1D*)f2->Get("spec_det4");//2
//  h2=(TH1D*)f2->Get("spec_det5");//1
//  h2=(TH1D*)f2->Get("spec_det6");//6

//  double h1_scale=1./h1->GetMaximum();
//  double h2_scale=1./h2->GetMaximum();
//  h1->Scale(h1_scale);
//  h2->Scale(h2_scale);
  h1->Rebin(2);
  h2->Rebin(2);
  h1->GetXaxis()->SetTitle("Energy [keV]");
  h1->GetYaxis()->SetTitle("Normalized");
  h2->GetXaxis()->SetTitle("Energy [keV]");
  h2->GetYaxis()->SetTitle("Normalized");
  h1->SetLineColorAlpha(2,0.7);
  h2->SetLineColorAlpha(4,0.7);
  TLegend* leg = new TLegend(.65,.75,.9,.90);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(h1,  "Exp.", "l");
  leg->AddEntry(h2,  "Sim.",   "l");
  c1->cd();
  gPad->SetLeftMargin(0.15);
  gPad->SetLogy(1);
  h1->DrawNormalized("hist");
  h2->DrawNormalized("hist same");
  leg->Draw("same");// */

  c1->SaveAs(name.Data());

 }

