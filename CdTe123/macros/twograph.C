
#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"
void twograph(){
  gROOT->Reset();
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
//  SetAtlasStyle();
  bool drawMultiGraphs = false;
  Int_t rangeFunc = 1; // 1 - SetLimits, 2  - SetRange, 3 - SetUserRange
  
  const Int_t N = 6;
  //const double scale = 4719.7328;
  const double scale = 6;
  Double_t x[N], y1[N], y2[N];
  x[0]=14.41;x[1]=31;x[2]=35;x[3]=81;x[4]=122.6;x[5]=136.47;
  y1[0]=0.001979*scale;y1[1]=0.009043*scale;y1[2]=0.008294*scale;y1[3]=0.01032*scale;y1[4]=0.003238*scale;y1[5]=0.002464*scale;
  y2[0]=0.015;y2[1]=0.091;y2[2]=0.089;y2[3]=0.09;y2[4]=0.04;y2[5]=0.036;
 
  TGraph *inputSpec  = new TGraph(N, x, y1);
  TGraph *inputSpec2 = new TGraph(N, x, y2);
  TMultiGraph *mg  = new TMultiGraph();
  TMultiGraph *mg2 = new TMultiGraph();

  TH1F *h1 = inputSpec->GetHistogram();
  h1->Scale(0.1);
  h1->SetTitle("; Energy [keV]; Efficiency (%)");
  h1->GetXaxis()->CenterTitle();h1->GetYaxis()->CenterTitle();

  TCanvas *c1 = new TCanvas("c1", "Comparison",0,  0, 1200, 800);
  TPad *pad1 = new TPad("pad1","",0,0,1,1);
  TPad *pad2 = new TPad("pad2","",0,0,1,1);
  gPad->SetTopMargin(0.15);
  gPad->SetLeftMargin(0.1);
  pad2->SetFillStyle(4000);
  // Makes pad2
  pad2->SetFrameFillStyle(0);
  // transparent.
  pad1->Draw();
  pad1->cd();

  inputSpec->SetMarkerStyle(29);
  inputSpec->SetMarkerColor(kBlack+2);
  inputSpec->SetLineColor(kBlack);
  mg->Add(inputSpec,"LP");
  if (drawMultiGraphs) {
    mg->Draw("ALP");
    //    mg->GetXaxis()->SetLimits(0.,9.);
    switch (rangeFunc) {
    case 1: mg->GetXaxis()->SetLimits(0.,9.); break;
    case 2: mg->GetXaxis()->SetRange(0.,9.); break;
    case 3: mg->GetXaxis()->SetRangeUser(0.,9.); break;
    }
    mg->GetXaxis()->SetRangeUser(0.,9.);
    pad1->Update();
  }
  else {
    //    inputSpec->GetXaxis()->SetLimits(0.,9.);
    switch (rangeFunc) {
    case 1: inputSpec->GetXaxis()->SetLimits(0.,150.); break;
    case 2: inputSpec->GetXaxis()->SetRange(0.,9.); break;
    case 3: inputSpec->GetXaxis()->SetRangeUser(0.,9.); break;
    }
    inputSpec->Draw("ALP");
  }

  TH1F *h2 = inputSpec2->GetHistogram();
//  TAxis *Ay2 = h2->GetYaxis();
//  Ay2->SetRangeUser(0.0, 0.5);

  pad2->Draw();
  pad2->cd();

  inputSpec2->SetMarkerStyle(29);
  inputSpec2->SetMarkerColor(kRed+2);
  inputSpec2->SetLineColor(kRed);
  mg2->Add(inputSpec2,"LPY+");
  if (drawMultiGraphs) {
    mg2->Draw("LPAY+");
    switch (rangeFunc) {
    case 1: mg2->GetXaxis()->SetLimits(0.,150.); break;
    case 2: mg2->GetXaxis()->SetRange(0.,9.); break;
    case 3: mg2->GetXaxis()->SetRangeUser(0.,9.); break;
    }
    mg2->GetXaxis()->SetAxisColor(kRed);
    mg2->GetXaxis()->SetLabelColor(kRed);  
    mg2->GetYaxis()->SetAxisColor(kRed);
    mg2->GetYaxis()->SetLabelColor(kRed);  
    pad2->Update();
  }
  else {
    switch (rangeFunc) {
    case 1: inputSpec2->GetXaxis()->SetLimits(0.,150.); break;
    case 2: inputSpec2->GetXaxis()->SetRange(0.,9.); break;
    case 3: inputSpec2->GetXaxis()->SetRangeUser(0.,9.); break;
    }
    inputSpec2->GetXaxis()->SetAxisColor(kRed);
    inputSpec2->GetXaxis()->SetLabelColor(kRed);  
    inputSpec2->GetYaxis()->SetAxisColor(kRed);
    inputSpec2->GetYaxis()->SetLabelColor(kRed);  
    inputSpec2->Draw("LPAY+");
  }
}

