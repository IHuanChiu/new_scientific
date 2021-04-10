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

void mk_Comparison(){

   #ifdef __CINT__
     gROOT->LoadMacro("AtlasLabels.C");
     gROOT->LoadMacro("AtlasUtils.C");
   #endif
   SetAtlasStyle();


  char name[50] = "";
  char name_f1[50] = "";
  char name_f2[50] = "";
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
  TH1F* h0_b;
  TH1F* h0_s;
  TH1F* h1_b;
  TH1F* h1_s;
  TH1F* h2_b;
  TH1F* h2_s;
  TH1F* h3_b;
  TH1F* h3_s;

//Load file : change name and number of matrix
  std::string mainname[4]={"DEW12007","White","Black","DEW12007_bar"};//DEW12007, White, Black
  std::string  mainrun[4]={"203079","203084","203086","203089"};//203079, 203084, ??
  for (int j = 0;  j < 4 ; j++){
     std::string inputname[4]={"Al","Fe","Holder","Ti"};
     std::string   runname[4]={"203081","203082","203068","203080"};
     for (int i = 0;   i < 4 ; i++){
   
   
        TFile *f1=new TFile(Form("../data/JPARC_2021Apri/%s/%s_beam.root",mainname[j].c_str(),mainrun[j].c_str()),"READ");//Sample
        TFile *f2=new TFile(Form("../data/JPARC_2021Apri/%s/%s_beam.root",(inputname[i]).c_str(),(runname[i]).c_str()),"READ");//Other
        sprintf(name_f1, "%s",mainname[j].c_str());
        sprintf(name_f2, "%s",inputname[i].c_str());
        bool do_scale=true;
      
      
        sprintf(name, "/Users/chiu.i-huan/Desktop/Plot_%s_vs_%s.pdf",name_f1,name_f2);
        h0_s = (TH1F*)f1->Get("Energy");
        h0_b = (TH1F*)f2->Get("Energy");
        int nentries1 = h0_s->GetSumOfWeights(); // read the number of entries in the t3
        int nentries2 = h0_b->GetSumOfWeights(); // read the number of entries in the t3
        double f1_scale=1./nentries1;
        double f2_scale=1./nentries2;
      
        cs->cd(1);
        h0_s->SetStats(0);
        if(h0_s->GetMaximum() > h0_s->GetMaximum()){
        h0_s->SetMaximum(h0_s->GetMaximum()*1.3);
        }else{h0_s->SetMaximum(h0_b->GetMaximum()*1.3);}
        h0_s->SetLineWidth(1);
        h0_s->SetLineColorAlpha(2,0.8);
        h0_b->SetStats(0);
        h0_b->SetLineWidth(1);
        h0_b->SetLineColorAlpha(kBlue,0.65);
      
        h0_s->GetXaxis()->SetTitle("Energy [keV]");
        h0_s->GetYaxis()->SetTitle("Counts");
      
        if(do_scale){
          h0_s->Scale(f1_scale);
          h0_b->Scale(f2_scale);
        }
      
      //  h0_s->DrawNormalized("hist",1);
      //  h0_b->DrawNormalized("same hist",1);
        h0_s->Draw("hist");
        h0_b->Draw("same hist");
        h0_s->Draw("same hist");//cover
      
        TLegend* leg = new TLegend(0.8,0.8,0.88,0.9);
        leg->SetFillColor(0);
        leg->SetLineColor(0);
        leg->SetBorderSize( 0);
        leg->SetTextSize(0.038);
        leg->AddEntry(h0_s, name_f1  , "L");
        leg->AddEntry(h0_b, name_f2  , "L");
        leg->Draw("same");
      
        cs->cd(2);
      //  tree1->Draw("energy >> h1_b(700,0,70)","(energy > 0 && energy < 70)","hist");
      //  tree2->Draw("energy >> h1_s(700,0,70)","(energy > 0 && energy < 70)","hist");
      //  h1_b     = (TH1D*)gDirectory->Get("h1_b");
      //  h1_s     = (TH1D*)gDirectory->Get("h1_s");
        h1_s = (TH1F*)f1->Get("el");
        h1_b = (TH1F*)f2->Get("el");
        h1_s->SetStats(0);
        if(h1_s->GetMaximum() > h1_s->GetMaximum()){
        h1_s->SetMaximum(h1_s->GetMaximum()*1.3);
        }else{h1_s->SetMaximum(h1_b->GetMaximum()*1.3);}
        h1_s->SetLineWidth(1);
        h1_s->SetLineColorAlpha(2,0.8);
        h1_b->SetStats(0);
        h1_b->SetLineWidth(1);
        h1_b->SetLineColorAlpha(kBlue,0.65);
        h1_s->GetXaxis()->SetTitle("Energy [keV]");
        h1_s->GetYaxis()->SetTitle("Counts");
        if(do_scale){
          h1_s->Scale(f1_scale);
          h1_b->Scale(f2_scale);
        }
        h1_s->Draw("hist");
        h1_b->Draw("same hist");
        h1_s->Draw("same hist");//cover
        leg->Draw("same");
      
        cs->cd(3);
      //  tree1->Draw("energy >> h2_b(700,70,140)","(energy > 100 && energy < 140)","hist");
      //  tree2->Draw("energy >> h2_s(700,70,140)","(energy > 100 && energy < 140)","hist");
      //  h2_b     = (TH1D*)gDirectory->Get("h2_b");
      //  h2_s     = (TH1D*)gDirectory->Get("h2_s");
        h2_s = (TH1F*)f1->Get("em");
        h2_b = (TH1F*)f2->Get("em");
        h2_s->SetStats(0);
        if(h2_s->GetMaximum() > h2_s->GetMaximum()){
        h2_s->SetMaximum(h2_s->GetMaximum()*1.3);
        }else{h2_s->SetMaximum(h2_b->GetMaximum()*1.3);}
        h2_s->SetLineWidth(1);
        h2_s->SetLineColorAlpha(2,0.8);
        h2_b->SetStats(0);
        h2_b->SetLineWidth(1);
        h2_b->SetLineColorAlpha(kBlue,0.65);
        h2_s->GetXaxis()->SetTitle("Energy [keV]");
        h2_s->GetYaxis()->SetTitle("Counts");
        if(do_scale){
          h2_s->Scale(f1_scale);
          h2_b->Scale(f2_scale);
        }
        h2_s->Draw("hist");
        h2_b->Draw("same hist");
        h2_s->Draw("same hist");//cover
        leg->Draw("same");
      
        cs->cd(4);
      //  tree1->Draw("energy >> h3_b(600,140,200)","(energy > 140 && energy < 200)","hist");
      //  tree2->Draw("energy >> h3_s(600,140,200)","(energy > 140 && energy < 200)","hist");
      //  h3_b     = (TH1D*)gDirectory->Get("h3_b");
      //  h3_s     = (TH1D*)gDirectory->Get("h3_s");
        h3_s = (TH1F*)f1->Get("eh");
        h3_b = (TH1F*)f2->Get("eh");
        h3_s->SetStats(0);
        if(h3_s->GetMaximum() > h3_s->GetMaximum()){
        h3_s->SetMaximum(h3_s->GetMaximum()*1.3);
        }else{h3_s->SetMaximum(h3_b->GetMaximum()*1.3);}
        h3_s->SetLineWidth(1);
        h3_s->SetLineColorAlpha(2,0.8);
        h3_b->SetStats(0);
        h3_b->SetLineWidth(1);
        h3_b->SetLineColorAlpha(kBlue,0.65);
        h3_s->GetXaxis()->SetTitle("Energy [keV]");
        h3_s->GetYaxis()->SetTitle("Counts");
        if(do_scale){
          h3_s->Scale(f1_scale);
          h3_b->Scale(f2_scale);
        }
        h3_s->Draw("hist");
        h3_b->Draw("same hist");
        h3_s->Draw("same hist");//cover
        leg->Draw("same");
      
      
         if(do_scale){
         cs->SaveAs(name);
         }else{
         cs->SaveAs("comparisonplots_4plots.pdf");
         cs->SaveAs("/Users/chiu.i-huan/Desktop/comparisonplots_4plots.pdf");
         }
   
      }// loop files
   }// loop main files
}

