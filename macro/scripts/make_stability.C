#include <math.h>
#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"

void make_stability(){
   #ifdef __CINT__
     gROOT->LoadMacro("AtlasLabels.C");
     gROOT->LoadMacro("AtlasUtils.C");
   #endif
   SetAtlasStyle();

  double hour, minute, X, temperature, humidity, Dew;
  TFile *file;
  TH1D* hp[20];
  TH1D* hn[20];
  char name[100] = "";

  for (int i = 1; i<10;i++){
  TCanvas *c1 = new TCanvas(Form("c%d",i),Form("c%d",i), 0, 0, 5000, 2500);
  if(i == 1) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_300n20_Am_3h_0915.root","READ");
  if(i == 2) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_300n20_Ba_3h_0915.root","READ");
  if(i == 3) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_300n20_Co_3h_0915.root","READ");
  if(i == 4) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_400n20_Am_3h_0915.root","READ");
  if(i == 5) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_400n20_Ba_3h_0915.root","READ");
  if(i == 6) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_400n20_Co_3h_0915.root","READ");
  if(i == 7) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_500n20_Am_3h_0915.root","READ");
  if(i == 8) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_500n20_Ba_3h_0915.root","READ");
  if(i == 9) file = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/cdte2mmdata_500n20_Co_3h_0915.root","READ");
   
  hp[1] = (TH1D*)file->Get("hpside_0");
  hp[2] = (TH1D*)file->Get("hpside_1");
  hp[3] = (TH1D*)file->Get("hpside_2");
  hp[4] = (TH1D*)file->Get("hpside_3");
  hp[5] = (TH1D*)file->Get("hpside_4");
//  hp[6] = (TH1D*)file->Get("hpside_5");

  hn[1] = (TH1D*)file->Get("hnside_0");
  hn[2] = (TH1D*)file->Get("hnside_1");
  hn[3] = (TH1D*)file->Get("hnside_2");
  hn[4] = (TH1D*)file->Get("hnside_3");
  hn[5] = (TH1D*)file->Get("hnside_4");
//  hn[6] = (TH1D*)file->Get("hnside_5");

  
  for (int j = 1; j < 6; j++){
  hp[j]->SetLineColor(j);
  hn[j]->SetLineColor(j);
  if (j >= 5) {
   hp[j]->SetLineColor(j+1);
  hn[j]->SetLineColor(j+1);
  }
  }

  c1->Divide(2,1);
  c1->cd(1);
  hp[1]->Draw();
  hp[1]->SetStats(0);
  hp[1]->SetMaximum(hp[1]->GetMaximum()*2);
  for (int j = 2; j < 6; j++){
  hp[j]->SetStats(0);
  hp[j]->Draw("same");
  }
  c1->cd(2);
  hn[1]->SetStats(0);
  hn[1]->Draw();
  for (int j = 2; j < 6; j++){
  hn[j]->SetStats(0);
  hn[j]->Draw("same");
  }
  TLegend* leg = new TLegend(.65,.6,.9,.9);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(hn[1], "0~3 hours" , "l");
  leg->AddEntry(hn[2], "3~6 hours" , "l");
  leg->AddEntry(hn[3], "6~9 hours" , "l");
  leg->AddEntry(hn[4], "9~12 hours" , "l");
  leg->AddEntry(hn[5], "12~15 hours" , "l");
//  leg->AddEntry(hn[6], "Time: 15~18 hours" , "l");
  leg->Draw("same");

  sprintf(name, "/Users/chiu.i-huan/Desktop/mycvtest/cv_%d.pdf",i);
  c1->SaveAs(name);

  }  //file loop
}

