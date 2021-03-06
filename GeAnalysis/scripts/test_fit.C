#include <TROOT.h>
#include "TFile.h"
#include "TROOT.h"
#include "TLegend.h"
#include "TChain.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "THn.h"
#include "TCanvas.h"
#include "TLatex.h"

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

void test_fit(){
   
  TFile* f = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/scripts/psicode/data/his28193.root","read");
  TH3F* h3 = (TH3F*)f->Get("hGermaniumEnergyVsTimeFine");
  
  TFile* fout = new TFile("/Users/chiu.i-huan/Desktop/test.root","recreate");
  fout->cd();

  // === make TH1F ===
  TH1F* hh;
  TH1F* hhnew[100];
  TF1* f1, *f2, *f3;
  for (int idet = 1; idet < 2 ; idet++){
     hh = (TH1F*)h3->ProjectionZ(Form("hh_%d",idet),0,1000,idet,idet);
   
     f1 = new TF1(Form("f1_%d",idet),"gausn",1240,1270);
     f2 = new TF1(Form("f2_%d",idet),"gaus",505,515);
     f3 = new TF1(Form("f3_%d",idet),"gaus",264,267);
     
     hh->Fit(Form("f1_%d",idet),"R");
     hh->Fit(Form("f2_%d",idet),"QR");
     hh->Fit(Form("f3_%d",idet),"QR");
//     std::cout << f1->
   
     gPad->SetLogy(1);
     hh->Draw();
     f1->Draw("same");
     f2->Draw("same");
     f3->Draw("same");
   
     hh->Write();
     f1->Write();
     f2->Write();
     f3->Write();
 
     std::cout << " a : "<< f1->GetParameter(1)  << " b : " << f1->GetParameter(0) << std::endl;
  }

  for(int i = 0;i< 20; i++){
    hhnew[i] = new TH1F(Form("hname_%d",i),Form("hname_%d",i),10,0,10);
    hhnew[i]->Write(); 
  }

//  std::cout << "CON:" << f1->GetParameter(0) << " MEAN : " << f1->GetParameter(1) << " #sigma : " << f1->GetParameter(2) << std::endl;
  int down = hh->GetXaxis()->FindBin(f1->GetParameter(1)-3*f1->GetParameter(2));
  int up = hh->GetXaxis()->FindBin(f1->GetParameter(1)+3*f1->GetParameter(2));
  int sum = hh->Integral(down,up);
//  std::cout << "peak1 : " << sum << std::endl;

//  std::cout << "f1 : " << f1->Integral(f1->GetParameter(1)-3*f1->GetParameter(2), f1->GetParameter(1)+3*f1->GetParameter(2)) << std::endl;
}
