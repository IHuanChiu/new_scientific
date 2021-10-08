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

void make_spectrum_forCdTePaper(){
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  char name[100] = "";

  TCanvas *c1 = new TCanvas("c1","Figure1_1",0,0,1000,800);
  TCanvas *c2 = new TCanvas("c2","Figure1_2",0,0,900,800);
  TCanvas *c3 = new TCanvas("c3","Figure2",0,0,1800,800);
  c3->Divide(4,2);

  TFile *file, *fileplot, *outfile; 
  TTree *mytree;
  TH1D *h_all_b, *h_all_a,*h_all_s, *h_all_minus, *h_all_pa, *h_all_na,*h_all_ps, *h_all_ps_m, *h_all_ns, *h_all_ns_m, *h_all_nb, *h_all_pb;
  TH2D* h_image;
  TH2F* h_image_rot;
  Double_t e_p[2048]; 
  Double_t e_n[2048]; 
  Int_t x[2048]; 
  Int_t y[2048]; 
  Int_t trigger; 
  Int_t nhitx; 
  Int_t nhity; 

  file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/JPARC2020March_CdTe_sum.root","READ");
  fileplot = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_30MeV_paper.root","READ");
  outfile = new TFile("/Users/chiu.i-huan/Desktop/CdTe_merge_paperPlots.root","RECREATE");

  mytree = (TTree*)file->Get("tree");

  TCut cut_energy = "((energy > 72 && energy < 78) || (energy > 12 && energy < 16))";
  TCut cut_signal = "((x < 5 && x > -5) && (y < 11 && y > -7))";
  TCut cut_bkg = "(x < -13.1875 || x > 13.1875)";
  TCut cut_basic = "((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253))";
  TCut UTcut = "((unixtime > 1583663336 && unixtime < 1583663640) || (unixtime > 1583665785 && unixtime < 1583668072) || (unixtime > 1583670126 && unixtime < 1583728926) || (unixtime > 1583797615 && unixtime < 1583807420) || (unixtime > 1583808902 && unixtime < 1583823904) || (unixtime > 1583825103 && unixtime < 1583837643) || (unixtime > 1583838416 && unixtime < 1583846500) || (unixtime > 1583847476 && unixtime < 1583872201))";//30 MeV

  //2D image (all)
  c1->cd();
  mytree->Draw("y:x >> h_image(128,-16,16,128,-16,16)",cut_basic+UTcut,"");
  h_image = (TH2D*)gDirectory->Get("h_image");
  h_image->SetTitle(";X[mm];Y[mm]");
  h_image->GetXaxis()->CenterTitle();
  h_image->GetYaxis()->CenterTitle();
  gStyle->SetPalette(53);
  gPad->SetRightMargin(0.15);
  h_image->Draw("colz");  
  sprintf(name, "/Users/chiu.i-huan/Desktop/hist_cdteImage_paper.pdf");
  c1->SaveAs(name);

  //energy spectrum (all & s vs. b)
  c2->cd();
//  gPad->SetLogy(1);
  mytree->Draw("energy >> h_all_a(300,0,150)",cut_basic+UTcut,"");
  mytree->Draw("energy >> h_all_s(300,0,150)",cut_basic+UTcut+cut_signal,"");
  mytree->Draw("energy >> h_all_b(300,0,150)",cut_basic+UTcut+cut_bkg,"");
  h_all_a = (TH1D*)gDirectory->Get("h_all_a");
  h_all_s = (TH1D*)gDirectory->Get("h_all_s");
  h_all_b = (TH1D*)gDirectory->Get("h_all_b"); 
  h_all_minus = (TH1D*)h_all_s->Clone();
  h_all_minus->Add(h_all_b,-1);
  h_all_a->SetTitle(";Energy[keV];Counts/0.5keV");
  h_all_a->GetXaxis()->CenterTitle();
  h_all_a->GetYaxis()->CenterTitle();
  h_all_a->SetLineColor(1);
  h_all_s->SetLineColor(2);
  h_all_b->SetLineColor(4);
  h_all_minus->SetLineColor(kTeal+9);
  h_all_a->Draw("hist");
  h_all_s->Draw("hist same");
  h_all_b->Draw("hist same");
  h_all_minus->Draw("hist same");
  TLegend* leg = new TLegend(.6,.60,.9,.9);
  leg->AddEntry(h_all_a,  "All", "l");
  leg->AddEntry(h_all_s,  "Signal", "l");
  leg->AddEntry(h_all_b,   "Bkg.",   "l");
  leg->AddEntry(h_all_minus,   "Signal - Bkg.",   "l");
  leg->Draw("same");
  sprintf(name, "/Users/chiu.i-huan/Desktop/hist_cdteES_paper.pdf");
  c2->SaveAs(name);
  
  //2D image (rotation)
  gStyle->SetPalette(53);
  TLatex t;
  t.SetNDC();
  t.SetTextFont( 62 );
  t.SetTextColor( 0 );
  t.SetTextSize( 0.12 );
  t.SetTextAlign( 12 );
  for (int i = 0; i < 8; i++){
     c3->cd(i+1);
     gPad->SetRightMargin(0.15);
     h_image_rot = (TH2F*)fileplot->Get(Form("h%d",i*2+1));
     h_image_rot->Rebin2D(4,4);
     h_image_rot->SetTitle(";X[mm];Y[mm]");
     h_image_rot->GetXaxis()->CenterTitle();
     h_image_rot->GetYaxis()->CenterTitle();
     h_image_rot->Draw("colz");
     t.DrawLatex(0.65,0.25,Form("%d^{o}",i*45));
  }
  sprintf(name, "/Users/chiu.i-huan/Desktop/hist_rot_image.pdf");
  c3->SaveAs(name);

  outfile->cd();
  c1->Write();
  c2->Write();
  c3->Write();
  h_image->Write();
  h_all_a->Write();
  h_all_s->Write();
  h_all_b->Write();
  outfile->Write();

 }

