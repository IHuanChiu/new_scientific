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

//#include "ATLASStyle/AtlasStyle.C"
//#include "ATLASStyle/AtlasLabels.C"
//#include "ATLASStyle/AtlasUtils.C"


using namespace std;

void Comparplot(){

//   #ifdef __CINT__
//     gROOT->LoadMacro("AtlasLabels.C");
//     gROOT->LoadMacro("AtlasUtils.C");
//   #endif
//   SetAtlasStyle();


  char name[50] = "";
  const double mz=91;
  const double rg=13;

  double r1=70;
  double r2=105;
  double scale=0;
  double rightmax=0;

  TFile * outputTfile = new TFile ("histoutput.root","RECREATE");
//  gErrorIgnoreLevel=1001;
//  TCanvas *c1 = new TCanvas("c1","gg comapare 12g Higgs",10,10,600,650);
  TCanvas *cs = new TCanvas("cs","cs",10,10,800,800);
//  cs->SetLogy();
//  gStyle->SetOptStat(kFALSE);
  TPad *pad1 = new TPad("pad1","pad1",0,0.3,1,1);
  TPad *pad2 = new TPad("pad2","pad2",0,0,1,0.3);
  TH1F* deno[70];
  TH1F* deno2[70];
  TH1 *F1_TL[70];
  TH1 *F2_TL[70];
  TH1D* h1;
  TH1D* h2;
  TH1D* h3;
//  TH1 *hsqrt;

//  const Int_t NBINS = 12;
//  Double_t edges[NBINS + 1] = {0.0, 100, 200, 300, 400, 500,
//                                700, 900, 
//                              1100, 1500, 1700,
//                               2000,  2500};
  h1     = new TH1D("h1",   "Var",  3000,  0, 3000);
  h2     = new TH1D("h2",   "Var",  3000, 0, 3000);
//  h3     = new TH1D("h3",   "Var",  NBINS,  edges);

//Load file
 TFile *f1=new TFile("outputTfile5cm.root","READ");//recon
 TFile *f2=new TFile("outputTfile3cm.root","READ");//recon

  TTree    *tree1 = (TTree*)f1->Get("EventTree");
  TTree    *tree2 = (TTree*)f2->Get("EventTree");

  Double_t    count; //0 is very important !!!
  Double_t    channel; //0 is very important !!!
  Double_t    count2; //0 is very important !!!
  Double_t    channel2; //0 is very important !!!

  tree1->SetBranchAddress("Count", &count );
  tree1->SetBranchAddress("Channel", &channel );
  
  tree2->SetBranchAddress("Count", &count2 );
  tree2->SetBranchAddress("Channel", &channel2 );


  int nentries1 = tree1->GetEntries(); // read the number of entries in the t3
  for (int i=0; i< nentries1 ; i++){
   tree1->GetEntry(i);//            <-----     !!!!!!!!!!!!!
   for(int c = 0; c < count; c++){
   h1->Fill(channel);
   }
   }

  int nentries2 = tree2->GetEntries(); // read the number of entries in the t3
  for (int i=0; i< nentries2 ; i++){
   tree2->GetEntry(i);//            <-----     !!!!!!!!!!!!!  
   for(int c = 0; c < count2; c++){
   h2->Fill(channel2);
   }
   }

   outputTfile->Write();

  h1->Rebin(10);
  h2->Rebin(10);

//  h1->GetXaxis()->SetTitle("Channel");
  h1->GetYaxis()->SetTitle("Counts");
  h1->SetMaximum(30000);
  h1->SetMinimum(0.1);
//  h1->GetXaxis()->SetNdivisions(7, 4, 0);

  h1->SetStats(0);
  h1->SetLineWidth(3);
  h1->SetLineColorAlpha(2,0.75);

  h2->SetLineWidth(3);
  h2->SetLineColorAlpha(kBlue,0.6);

  pad1->SetBottomMargin(0);
  pad2->SetTopMargin(0.01);
  pad2->SetBottomMargin(0.4);
  pad1->Draw();
  pad2->Draw();


  pad1->cd();
  pad1->SetLogy();
  h1->Draw();
  h2->Draw("same");


   TLegend* leg = new TLegend(0.65,0.6,0.88,0.9);
   leg->SetFillColor(0);
   leg->SetLineColor(0);
   leg->SetBorderSize( 0);
   leg->AddEntry(h1, "5CM"  , "L");
   leg->AddEntry(h2, "3CM"  , "L");
   leg->SetTextSize(0.038);
   leg->Draw("same");

   TLatex *text2;
   text2 = new TLatex(5.570061,23.08044,"^{152}Eu,100s");
   text2->SetNDC();
   text2->SetTextAlign(13);
   text2->SetX(0.384);
   text2->SetY(0.88);
   text2->SetTextFont(42);
   text2->SetTextSizePixels(24);
   text2->Draw();


   pad2->cd();

   pad2->SetLogy();
  h3 = (TH1D*)h2->Clone("h3");

  h3->Divide(h1);
  h3->SetStats(0);      // No statistics on lower plot
  h3->SetLineWidth(2);
  h3->SetLineColor(1);
  h3->SetMinimum(0.01);  // Define Y ..
  h3->SetMaximum(70); // .. range
  h3->SetTitle("");

   h3->GetYaxis()->SetTitle("Ratio (3CM/5CM)");
   h3->GetYaxis()->SetNdivisions(505);
   h3->GetYaxis()->SetTitleSize(25);
   h3->GetYaxis()->SetTitleFont(43);
   h3->GetYaxis()->SetTitleOffset(1.55);
   h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
   h3->GetYaxis()->SetLabelSize(20);

   h3->GetXaxis()->SetTitle("Ge Detector Channel");
   h3->GetXaxis()->SetTitleSize(35);
   h3->GetXaxis()->SetTitleFont(43);
   h3->GetXaxis()->SetTitleOffset(4.);
   h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
   h3->GetXaxis()->SetLabelSize(30);

   h3->Draw("H");

   double low =  h3->GetXaxis()->GetXmin();
   double high = h3->GetXaxis()->GetXmax();
   TLine *line = new TLine(low,1,high,1);
   line->SetLineColorAlpha(kRed, 0.3);
   line->SetLineWidth(2);
   line->Draw("same");


   cs->SaveAs("comparisonplots.pdf");
   cs->SaveAs("/Users/chiu.i-huan/Desktop/comparisonplots.pdf");
}

