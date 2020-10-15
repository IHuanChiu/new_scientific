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
  TString voltagename="300n20";

  TCanvas *c0 = new TCanvas("temp canvas","temp canvas",10,10,800,800);
  TCanvas *c1 = new TCanvas("c1","Energy Spectum",10,10,800,800);
  TCanvas *c2 = new TCanvas("c2","Energy Spectum comparison",10,10,800,800);
  TCanvas *c3_a = new TCanvas("c3_a","Energy comparison Am",0,0,1600,800);
  TCanvas *c3_b = new TCanvas("c3_b","Energy comparison Ba",0,0,1600,800);
  TCanvas *c3_c = new TCanvas("c3_c","Energy comparison Co",0,0,1600,800);
  c3_a->Divide(2,1);
  c3_b->Divide(2,1);
  c3_c->Divide(2,1);

  TH1D *ha_p,*ha_n,*hb_p,*hb_n,*hc_p,*hc_n,*ha,*hb,*hc;
  TH2D *ha_com, *ha_com2, *hb_com, *hb_com2, *hc_com, *hc_com2;

  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/2mmCdTe_root/cdtedsd_2020b_combined_"+voltagename+"_Amsource_cali_merge_1008.root","READ");
  TFile* fb = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/2mmCdTe_root/cdtedsd_2020b_combined_"+voltagename+"_Basource_cali_merge_1008.root","READ");
  TFile* fc = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/2mmCdTe_root/cdtedsd_2020b_combined_"+voltagename+"_Cosource_cali_merge_1008.root","READ");
  TTree* tree_a = (TTree*)fa->Get("tree");
  TTree* tree_b = (TTree*)fb->Get("tree");
  TTree* tree_c = (TTree*)fc->Get("tree");
     
  c0->cd();
  tree_a->Draw("energy >> ha(600,0,150)","","");
  tree_b->Draw("energy >> hb(600,0,150)","","");
  tree_c->Draw("energy >> hc(600,0,150)","","");
  tree_a->Draw("energy_p >> ha_p(600,0,150)","","");
  tree_b->Draw("energy_p >> hb_p(600,0,150)","","");
  tree_c->Draw("energy_p >> hc_p(600,0,150)","","");
  tree_a->Draw("energy_n >> ha_n(600,0,150)","","");
  tree_b->Draw("energy_n >> hb_n(600,0,150)","","");
  tree_c->Draw("energy_n >> hc_n(600,0,150)","","");
  tree_a->Draw("energy_n:energy_p >> ha_com(600,0,150,600,0,150)","","colz");
  tree_a->Draw("(energy_p-energy_n):(energy_p+energy_n)/2 >> ha_com2(600,0,150,400,-60,40)","","colz");
  tree_b->Draw("energy_n:energy_p >> hb_com(600,0,150,600,0,150)","","");
  tree_b->Draw("(energy_p-energy_n):(energy_p+energy_n)/2 >> hb_com2(600,0,150,400,-60,40)","","colz");
  tree_c->Draw("energy_n:energy_p >> hc_com(600,0,150,600,0,150)","","colz");
  tree_c->Draw("(energy_p-energy_n):(energy_p+energy_n)/2 >> hc_com2(600,0,150,400,-60,40)","","colz");
  ha = (TH1D*)gDirectory->Get("ha");
  hb = (TH1D*)gDirectory->Get("hb");
  hc = (TH1D*)gDirectory->Get("hc"); 
  ha_p = (TH1D*)gDirectory->Get("ha_p");
  hb_p = (TH1D*)gDirectory->Get("hb_p");
  hc_p = (TH1D*)gDirectory->Get("hc_p"); 
  ha_n = (TH1D*)gDirectory->Get("ha_n");
  hb_n = (TH1D*)gDirectory->Get("hb_n");
  hc_n = (TH1D*)gDirectory->Get("hc_n"); 
  ha_com = (TH2D*)gDirectory->Get("ha_com"); 
  ha_com2 = (TH2D*)gDirectory->Get("ha_com2"); 
  hb_com = (TH2D*)gDirectory->Get("hb_com"); 
  hb_com2 = (TH2D*)gDirectory->Get("hb_com2"); 
  hc_com = (TH2D*)gDirectory->Get("hc_com"); 
  hc_com2 = (TH2D*)gDirectory->Get("hc_com2"); 

  double n_h = ha->GetMaximum()+hb->GetMaximum()+hc->GetMaximum();
  double n_hpn = ha_p->GetMaximum()+hb_p->GetMaximum()+hc_p->GetMaximum()+ha_n->GetMaximum()+hb_n->GetMaximum()+hc_n->GetMaximum();
  ha->SetMaximum((hb->GetMaximum())*1.1);
  ha_p->SetMaximum((hb->GetMaximum())*1.1);

  ha->GetXaxis()->SetTitle("Energy [keV]");
  ha->GetYaxis()->SetTitle("Counts");
  ha_p->GetXaxis()->SetTitle("Energy [keV]");
  ha_p->GetYaxis()->SetTitle("Counts");
  ha_com->GetXaxis()->SetTitle("E_{Pt} [keV]");
  ha_com->GetYaxis()->SetTitle("E_{Al} [keV]");
  ha_com2->GetXaxis()->SetTitle("(E_{Pt}+E_{Al})/2 [keV]");
  ha_com2->GetYaxis()->SetTitle("(E_{Pt}-E_{Al})/2 [keV]");
  hb_com->GetXaxis()->SetTitle("E_{Pt} [keV]");
  hb_com->GetYaxis()->SetTitle("E_{Al} [keV]");
  hb_com2->GetXaxis()->SetTitle("(E_{Pt}+E_{Al})/2 [keV]");
  hb_com2->GetYaxis()->SetTitle("(E_{Pt}-E_{Al})/2 [keV]");
  hc_com->GetXaxis()->SetTitle("E_{Pt} [keV]");
  hc_com->GetYaxis()->SetTitle("E_{Al} [keV]");
  hc_com2->GetXaxis()->SetTitle("(E_{Pt}+E_{Al})/2 [keV]");
  hc_com2->GetYaxis()->SetTitle("(E_{Pt}-E_{Al})/2 [keV]");

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

  c3_a->cd(1); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  ha_com->Draw("colz");
  c3_a->cd(2); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  ha_com2->Draw("colz");

  c3_b->cd(1); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  hb_com->Draw("colz");
  c3_b->cd(2); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  hb_com2->Draw("colz");

  c3_c->cd(1); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  hc_com->Draw("colz");
  c3_c->cd(2); 
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  hc_com2->Draw("colz");

  c1->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_combine_all.pdf");
  c2->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_combine_pn.pdf");

  c3_a->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Am.pdf");
  c3_b->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Ba.pdf");
  c3_c->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Co.pdf");
  c3_a->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Am.png");
  c3_b->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Ba.png");
  c3_c->SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+voltagename+"/EnergySpectrum_correlation_Co.png");

 }

