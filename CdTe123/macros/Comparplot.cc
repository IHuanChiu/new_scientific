#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "THStack.h"
#include "TLegend.h"
//#include "Headers.h"
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

#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"


using namespace std;

void Comparplot(){

   #ifdef __CINT__
     gROOT->LoadMacro("AtlasLabels.C");
     gROOT->LoadMacro("AtlasUtils.C");
   #endif
   SetAtlasStyle();


  char name[50] = "";
  const double mz=91;
  const double rg=13;

  double r1=70;
  double r2=105;
  double scale=0;
  double rightmax=0;

//  TFile * outputTfile = new TFile ("histoutput.root","RECREATE");
  TCanvas *cs = new TCanvas("cs","cs",0,0,3200,3200);
  cs->Divide(2,2);

  TPad *pad1 = new TPad("pad1","pad1",0,0.3,1,1);
  TPad *pad2 = new TPad("pad2","pad2",0,0,1,0.3);
  TH1F* deno[70];
  TH1F* deno2[70];
  TH1 *F1_TL[70];
  TH1 *F2_TL[70];
  TH1D* h0_b;
  TH1D* h0_s;
  TH1D* h1_b;
  TH1D* h1_s;
  TH1D* h2_b;
  TH1D* h2_s;
  TH1D* h3_b;
  TH1D* h3_s;

//Load file
// TFile *f1=new TFile("../data/J-PARC2021Apri/live_data_BGD_27MeV_95ks.root","READ");//recon
// TFile *f2=new TFile("../data/J-PARC2021Apri/live_data0406_STD_27MeV_78ks.mca.root","READ");//recon
// double f1_scale=1/95.;
// double f2_scale=1/78.;
 TFile *f1=new TFile("../data/J-PARC2021Apri/live_data0404_bkg_25MeV_84ks.mca.root","READ");//bkg
 TFile *f2=new TFile("../data/J-PARC2021Apri/live_data0404_STD_25MeV_41ks.mca.root","READ");//signal
 double f1_scale=1/84.;
 double f2_scale=1/41.;
 bool do_scale=true;

  TTree    *tree1 = (TTree*)f1->Get("tree");
  TTree    *tree2 = (TTree*)f2->Get("tree");

  Double_t    energy; //0 is very important !!!
  Int_t    channel; //0 is very important !!!
  Double_t    energy2; //0 is very important !!!
  Int_t    channel2; //0 is very important !!!

  tree1->SetBranchAddress("energy", &energy );
  tree1->SetBranchAddress("channel", &channel );
  
  tree2->SetBranchAddress("energy", &energy2 );
  tree2->SetBranchAddress("channel", &channel2 );


  int nentries1 = tree1->GetEntries(); // read the number of entries in the t3
  cs->cd(1);
  tree1->Draw("energy >> h0_b(700,0,350)","(energy > 0 && energy < 350)","hist");
  tree2->Draw("energy >> h0_s(700,0,350)","(energy > 0 && energy < 350)","hist");
  h0_b     = (TH1D*)gDirectory->Get("h0_b");
  h0_s     = (TH1D*)gDirectory->Get("h0_s");
  h0_s->SetStats(0);
  if(h0_s->GetMaximum() > h0_s->GetMaximum()){
  h0_s->SetMaximum(h0_s->GetMaximum()*1.3);
  }else{h0_s->SetMaximum(h0_b->GetMaximum()*1.3);}
  h0_s->SetLineWidth(1);
  h0_s->SetLineColorAlpha(2,0.75);
  h0_b->SetStats(0);
  h0_b->SetLineWidth(1);
  h0_b->SetLineColorAlpha(kBlue,0.75);

  h0_s->GetXaxis()->SetTitle("Energy [keV]");
  h0_s->GetYaxis()->SetTitle("Counts");

  if(do_scale){
    h0_s->Scale(f2_scale);
    h0_b->Scale(f1_scale);
  }

  h0_s->Draw("hist");
  h0_b->Draw("same hist");

  TLegend* leg = new TLegend(0.8,0.8,0.88,0.9);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize( 0);
  leg->AddEntry(h0_s, "STD"  , "L");
  leg->AddEntry(h0_b, "BGD"  , "L");
  leg->SetTextSize(0.038);
  leg->Draw("same");

  cs->cd(2);
  tree1->Draw("energy >> h1_b(200,0,100)","(energy > 0 && energy < 100)","hist");
  tree2->Draw("energy >> h1_s(200,0,100)","(energy > 0 && energy < 100)","hist");
  h1_b     = (TH1D*)gDirectory->Get("h1_b");
  h1_s     = (TH1D*)gDirectory->Get("h1_s");
  h1_s->SetStats(0);
  if(h1_s->GetMaximum() > h1_s->GetMaximum()){
  h1_s->SetMaximum(h1_s->GetMaximum()*1.3);
  }else{h1_s->SetMaximum(h1_b->GetMaximum()*1.3);}
  h1_s->SetLineWidth(1);
  h1_s->SetLineColorAlpha(2,0.75);
  h1_b->SetStats(0);
  h1_b->SetLineWidth(1);
  h1_b->SetLineColorAlpha(kBlue,0.75);
  h1_s->GetXaxis()->SetTitle("Energy [keV]");
  h1_s->GetYaxis()->SetTitle("Counts");
  if(do_scale){
    h1_s->Scale(f2_scale);
    h1_b->Scale(f1_scale);
  }
  h1_s->Draw("hist");
  h1_b->Draw("same hist");
  leg->Draw("same");

  cs->cd(3);
  tree1->Draw("energy >> h2_b(200,100,200)","(energy > 100 && energy < 200)","hist");
  tree2->Draw("energy >> h2_s(200,100,200)","(energy > 100 && energy < 200)","hist");
  h2_b     = (TH1D*)gDirectory->Get("h2_b");
  h2_s     = (TH1D*)gDirectory->Get("h2_s");
  h2_s->SetStats(0);
  if(h2_s->GetMaximum() > h2_s->GetMaximum()){
  h2_s->SetMaximum(h2_s->GetMaximum()*1.3);
  }else{h2_s->SetMaximum(h2_b->GetMaximum()*1.3);}
  h2_s->SetLineWidth(1);
  h2_s->SetLineColorAlpha(2,0.75);
  h2_b->SetStats(0);
  h2_b->SetLineWidth(1);
  h2_b->SetLineColorAlpha(kBlue,0.75);
  h2_s->GetXaxis()->SetTitle("Energy [keV]");
  h2_s->GetYaxis()->SetTitle("Counts");
  if(do_scale){
    h2_s->Scale(f2_scale);
    h2_b->Scale(f1_scale);
  }
  h2_s->Draw("hist");
  h2_b->Draw("same hist");
  leg->Draw("same");

  cs->cd(4);
  tree1->Draw("energy >> h3_b(300,200,350)","(energy > 200 && energy < 350)","hist");
  tree2->Draw("energy >> h3_s(300,200,350)","(energy > 200 && energy < 350)","hist");
  h3_b     = (TH1D*)gDirectory->Get("h3_b");
  h3_s     = (TH1D*)gDirectory->Get("h3_s");
  h3_s->SetStats(0);
  if(h3_s->GetMaximum() > h3_s->GetMaximum()){
  h3_s->SetMaximum(h3_s->GetMaximum()*1.3);
  }else{h3_s->SetMaximum(h3_b->GetMaximum()*1.3);}
  h3_s->SetLineWidth(1);
  h3_s->SetLineColorAlpha(2,0.75);
  h3_b->SetStats(0);
  h3_b->SetLineWidth(1);
  h3_b->SetLineColorAlpha(kBlue,0.75);
  h3_s->GetXaxis()->SetTitle("Energy [keV]");
  h3_s->GetYaxis()->SetTitle("Counts");
  if(do_scale){
    h3_s->Scale(f2_scale);
    h3_b->Scale(f1_scale);
  }
  h3_s->Draw("hist");
  h3_b->Draw("same hist");
  leg->Draw("same");





//  pad1->SetBottomMargin(0);
//  pad2->SetTopMargin(0.01);
//  pad2->SetBottomMargin(0.4);
//  pad1->Draw();
//  pad2->Draw();
//
//
//  pad1->cd();
//  pad1->SetLogy();
//  h1->Draw();
//  h2->Draw("same");



//  TLatex *text2;
//   text2 = new TLatex(5.570061,23.08044,"^{152}Eu,100s");
//   text2->SetNDC();
//   text2->SetTextAlign(13);
//   text2->SetX(0.384);
//   text2->SetY(0.88);
//   text2->SetTextFont(42);
//   text2->SetTextSizePixels(24);
//   text2->Draw();
//
//
//   pad2->cd();
//
//   pad2->SetLogy();
//  h3 = (TH1D*)h2->Clone("h3");
//
//  h3->Divide(h1);
//  h3->SetStats(0);      // No statistics on lower plot
//  h3->SetLineWidth(2);
//  h3->SetLineColor(1);
//  h3->SetMinimum(0.01);  // Define Y ..
//  h3->SetMaximum(70); // .. range
//  h3->SetTitle("");
//
//   h3->GetYaxis()->SetTitle("Ratio (3CM/5CM)");
//   h3->GetYaxis()->SetNdivisions(505);
//   h3->GetYaxis()->SetTitleSize(25);
//   h3->GetYaxis()->SetTitleFont(43);
//   h3->GetYaxis()->SetTitleOffset(1.55);
//   h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
//   h3->GetYaxis()->SetLabelSize(20);
//
//   h3->GetXaxis()->SetTitle("Ge Detector Channel");
//   h3->GetXaxis()->SetTitleSize(35);
//   h3->GetXaxis()->SetTitleFont(43);
//   h3->GetXaxis()->SetTitleOffset(4.);
//   h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
//   h3->GetXaxis()->SetLabelSize(30);
//
//   h3->Draw("H");
//
//   double low =  h3->GetXaxis()->GetXmin();
//   double high = h3->GetXaxis()->GetXmax();
//   TLine *line = new TLine(low,1,high,1);
//   line->SetLineColorAlpha(kRed, 0.3);
//   line->SetLineWidth(2);
//   line->Draw("same");

   if(do_scale){
   cs->SaveAs("/Users/chiu.i-huan/Desktop/comparisonplots_scale.pdf");
   }else{
   cs->SaveAs("comparisonplots.pdf");
   cs->SaveAs("/Users/chiu.i-huan/Desktop/comparisonplots.pdf");
   }
}

