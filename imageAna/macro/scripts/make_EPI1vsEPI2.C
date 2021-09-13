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

void make_EPI1vsEPI2(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  TCanvas *c0 = new TCanvas("temp canvas","temp canvas",10,10,800,800);
  TCanvas *c1 = new TCanvas("c1","Energy Spectum comparison",10,10,1000,800);
  TCanvas *c2 = new TCanvas("c2 test","Energy Spectum",10,10,1000,800);
  TCanvas *c3 = new TCanvas("c3","C3 Energy Spectum",10,10,1000,800);

  TH2D *ha_com;
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_merge_500n20_Co_Emap.root","READ");
  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_16to30_Osaka2mmCdTe_Co.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_9to11_Osaka2mmCdTe_Ba.root","READ");
//  TFile* fa = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210804a_6to8_merge_500n20_Am.root","READ");
  TTree* tree_a = (TTree*)fa->Get("tree");
     
  // make 2d plots
  c0->cd();
  tree_a->Draw("(E_p_lv2-E_n_lv2)/2:(E_p_lv2+E_n_lv2)/2 >> ha_com(600,0,150,200,-40,60)","nsignalx_lv2 == 1 && nsignaly_lv2 == 1","colz");
//  tree_a->Draw("(E_p_lv2-E_n_lv2)/2:energy >> ha_com(600,0,150,200,-40,60)","nsignalx_lv2 == 1 && nsignaly_lv2 == 1","colz");
  ha_com = (TH2D*)gDirectory->Get("ha_com"); 
  ha_com->SetTitle(";(E_{Pt}+E_{Al})/2 [keV];(E_{Pt}-E_{Al})/2 [keV]");
  c1->cd();
  gPad->SetRightMargin(0.15);
  gPad->SetLogz(1);
  gStyle->SetPalette(62);//or 107
  ha_com->Draw("colz");
  c1->SaveAs("/Users/chiu.i-huan/Desktop/PN_2dplot.pdf");


  // make energy spectrum
  TH1D *h1, *h2, *h3;
  tree_a->Draw("(E_p_lv2+E_n_lv2)/2 >> h1(3000,0,150)","(E_p_lv2-E_n_lv2)/2 > -1 && (E_p_lv2-E_n_lv2)/2 < 1 && nsignalx_lv2 == 1 && nsignaly_lv2 == 1","colz");
  tree_a->Draw("(E_p_lv2+E_n_lv2)/2 >> h2(3000,0,150)","(E_p_lv2-E_n_lv2)/2 > -4 && (E_p_lv2-E_n_lv2)/2 < -3 && nsignalx_lv2 == 1 && nsignaly_lv2 == 1","colz");
  tree_a->Draw("(E_p_lv2+E_n_lv2)/2 >> h3(3000,0,150)","(E_p_lv2-E_n_lv2)/2 > -6 && (E_p_lv2-E_n_lv2)/2 < -5 && nsignalx_lv2 == 1 && nsignaly_lv2 == 1","colz");
  h1 = (TH1D*)gDirectory->Get("h1");
  h2 = (TH1D*)gDirectory->Get("h2");
  h3 = (TH1D*)gDirectory->Get("h3");
  h1->SetLineColor(3);
  h2->SetLineColor(2);
  h3->SetLineColor(4);
  h1->SetTitle(";E_{avg};Count/0.05 keV");
  TLegend* leg = new TLegend(.2,.6,.7,.9);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(h1, "#DeltaE = 0" , "l");
  leg->AddEntry(h2, "#DeltaE = -3.5" , "l");
  leg->AddEntry(h3, "#DeltaE = -5.5" , "l");
  c2->cd();
  h1->Draw("hist");
  h2->Draw("hist same");
  h3->Draw("hist same");
  leg->Draw("same");
  c2->SaveAs("/Users/chiu.i-huan/Desktop/map_plot.pdf");

  // make energy spectrum for mao

  TFile *fout = new TFile("/Users/chiu.i-huan/Desktop/Eavg_forMap_fullrange1keV.root","RECREATE");
  fout->cd();
  TH1D* hmap;
  int h_index;
  double ori_E;
  double range = 1;
  c3->Print("/Users/chiu.i-huan/Desktop/map_plot_all.pdf[", "pdf");
  c3->cd();
  for(int nx = 1; nx < 2;nx++){
     for(int ny = 1; ny < 2;ny++){
       ori_E=-30;//from -20 keV
       h_index = 0;
       for(int i = 0 ; i < 1000; i++){
        if(ori_E > 5) continue;  
        std::cout <<  "Index : " << h_index <<"  "  << ori_E<<"<E<" << ori_E+range << std::endl;
        tree_a->Draw("(E_p_lv2+E_n_lv2)/2 >> hmap(600,0,150)",Form("(E_p_lv2-E_n_lv2)/2 > %f && (E_p_lv2-E_n_lv2)/2 < %f && nsignalx_lv2 == %d && nsignaly_lv2 == %d",ori_E,ori_E+range,nx,ny),"");
        hmap = (TH1D*)gDirectory->Get("hmap");
        hmap->SetName(Form("h%d_nx%d_ny%d",h_index,nx,ny));
//        hmap->SetTitle(";E_{avg};Counts/0.25keV");
        hmap->Write();
        ori_E=ori_E+range;
        h_index++;  
        hmap->Draw("hist");
        c3->Print("/Users/chiu.i-huan/Desktop/map_plot_all.pdf");
       }
     }
  }
  c3->Print("/Users/chiu.i-huan/Desktop/map_plot_all.pdf]", "pdf");
  std::cout << "/Users/chiu.i-huan/Desktop/Eavg_forMap_fullrange1keV.root" << std::endl;


 }

