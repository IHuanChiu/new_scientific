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

void Comparplot_bkgvstarget(){

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
  TCanvas *cs = new TCanvas("cs","cs",10,10,1600,800);
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

//Load file
 TFile *f1=new TFile("../data/JPARC_June/sample/merge_target.root","READ");//recon
 TFile *f2=new TFile("../data/JPARC_June/bkg/merge_bkg_bkg.root","READ");//recon

  TTree    *tree1 = (TTree*)f1->Get("tree");
  TTree    *tree2 = (TTree*)f2->Get("tree");

  // 1 : 19.83
  //tree1->Draw("energy >> _h1(397,60,80)","","");
  //tree2->Draw("energy >> _h2(397,60,80)","","");
  //h1 = (TH1D*)gDirectory->Get("_h1");
  //h2 = (TH1D*)gDirectory->Get("_h2");

  h1 = f1->Get("energy");
  h2 = f2->Get("energy");

  double aa = (tree1->GetEntries()+0.0)/tree2->GetEntries();
  h2->Scale(aa);

  outputTfile->Write();

  h1->Rebin(1);
  h2->Rebin(1);

  h1->GetYaxis()->SetTitle("Counts");
  h1->SetMaximum(450);
  h1->SetMinimum(50);

  h1->SetStats(0);
  h1->SetLineWidth(1);
  h1->SetLineColorAlpha(2,0.75);

  h2->SetLineWidth(1);
  h2->SetLineColorAlpha(kBlue,0.6);

  pad1->SetBottomMargin(0);
  pad2->SetTopMargin(0.01);
  pad2->SetBottomMargin(0.4);
  pad1->Draw();
  pad2->Draw();


  pad1->cd();
  pad1->SetLogy(0);
  h1->Draw("hist");
  h2->Draw("hist same");


   TLegend* leg = new TLegend(0.65,0.6,0.88,0.85);
   leg->SetFillColor(0);
   leg->SetLineColor(0);
   leg->SetBorderSize( 0);
   leg->AddEntry(h1, "Target"  , "L");
   leg->AddEntry(h2, "Background"  , "L");
   leg->SetTextSize(0.038);
   leg->Draw("same");

   TLatex *text2;
   text2 = new TLatex(5.570061,23.08044,"Ge-Ch7 2026~2031 vs. 2032~2036");
   text2->SetNDC();
   text2->SetTextAlign(13);
   text2->SetX(0.384);
   text2->SetY(0.88);
   text2->SetTextFont(42);
   text2->SetTextSizePixels(24);
   text2->Draw();


   pad2->cd();

   pad2->SetLogy(0);
  h3 = (TH1D*)h2->Clone("h3");

  h3->Divide(h1);
  h3->SetStats(0);      // No statistics on lower plot
  h3->SetLineWidth(1);
  h3->SetLineColor(1);
  h3->SetMinimum(0.5);  // Define Y ..
  h3->SetMaximum(1.5); // .. range
  h3->SetTitle("");

   h3->GetYaxis()->SetTitle("Ratio (target/bkg.)");
   h3->GetYaxis()->SetNdivisions(505);
   h3->GetYaxis()->SetTitleSize(25);
   h3->GetYaxis()->SetTitleFont(43);
   h3->GetYaxis()->SetTitleOffset(1.55);
   h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
   h3->GetYaxis()->SetLabelSize(20);

   h3->GetXaxis()->SetTitle("Energy [keV]");
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


   cs->SaveAs("comparisonplots_ch7_scale.pdf");
}

