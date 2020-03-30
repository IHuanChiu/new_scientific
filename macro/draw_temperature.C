#include <math.h>
#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"

void draw_temperature(){
   #ifdef __CINT__
     gROOT->LoadMacro("AtlasLabels.C");
     gROOT->LoadMacro("AtlasUtils.C");
   #endif
//   SetAtlasStyle();

  ifstream fin("../run/auxfile/temprature.txt");
  if(!fin){
    cerr << "ERROR : ./channelmap.dat is not found. " << endl;
    return -1 ;
  }

  double hour, minute, X, temperature, humidity, Dew;
  TCanvas *c1 = new TCanvas("c1","c1", 0, 0, 2000, 2000);
//  TH2D* h1 = new TH2D("h1","h1",200, 0, 200, 300, -5, 30);
//  TH2D* h2 = new TH2D("h2","h2",200, 0, 200, 100, -5, 30);
//  TH2D* h3 = new TH2D("h3","h3",200, 0, 200, 400, -30, 30);

  TH2D* h1 = new TH2D("h1","h1",970, 1620, 2590, 300, -5, 30);
  TH2D* h2 = new TH2D("h2","h2",970, 1620, 2590, 100, -5, 30);
  TH2D* h3 = new TH2D("h3","h3",970, 1620, 2590, 400, -30, 30);
//
//  TH2D* h1 = new TH2D("h1","h1",300, 3505, 3805, 300, -5, 25);
//  TH2D* h2 = new TH2D("h2","h2",300, 3505, 3805, 100, 20, 30);
//  TH2D* h3 = new TH2D("h3","h3",300, 3505, 3805, 400, -30, 30);

  int bins = 0;
  string line;
  double x0 = 805; 
  while(getline(fin,line)){
    if(line.substr(0, 1)=="#") continue;
    istringstream iss(line) ;
    iss >> hour >> minute >> temperature >> humidity;
    bins++;
//    X = hour*60+minute - x0;
    X = (hour+24)*60+minute - x0;
//    X = (hour+48)*60+minute - x0;
    double denominator = 17.62 - log(humidity/100.) - (17.62*(temperature/100.)/(243.12+temperature/100.));
    double numerator = log(humidity/100.)+(17.62*(temperature/100.)/(243.12+temperature/100.));
    Dew = 243.12*(numerator/denominator);
    std::cout << " X : " << X <<" temp : " << temperature/100. << "  humidity : " << humidity/100.  << "  " << Dew << std::endl;
    h1->Fill(X,temperature/100.);       
    h2->Fill(X,humidity/100.);       
    h3->Fill(X,Dew);       
  }
  h1->SetStats(0);
  h2->SetStats(0);
  h3->SetStats(0);
//  h1->SetTitle("Day 1/28");
  h1->SetTitle("Day 1/29");
//  h1->SetTitle("Day 1/30");
  h1->GetXaxis()->SetTitle("Time [minute]");
  h1->GetYaxis()->SetTitle("temperature[{}^{o}C] or humidity[%]");

  h1->SetMarkerStyle(20);
  h2->SetMarkerStyle(20);
  h3->SetMarkerStyle(20);

  h1->SetMarkerColor(2);
  h2->SetMarkerColor(4);
  h3->SetMarkerColor(3);

  h1->Draw("C L P HIST");
  h2->Draw("C L P HIST same");
  h3->Draw("C L P HIST SAME");

//  TGaxis *axis = new TGaxis(200,-5, 200, 30,-5,30,510,"+L");
  TGaxis *axis = new TGaxis(2590,-5,2590, 30,-5,30,510,"+L");
//  TGaxis *axis = new TGaxis(3805,-5, 3805, 30,-5,30,510,"+L");
  axis->SetLineColor(kBlue);
  axis->SetTextColor(kBlue);
  axis->Draw("same");

  TLegend* leg = new TLegend(.65,.3,.85,.45);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  leg->AddEntry(h1,  "temperature", "p");
  leg->AddEntry(h2,  "humidity",   "p");
  leg->AddEntry(h3,  "dew", "p");
  leg->Draw("same");

//  c1->SaveAs("../run/figs/day1.pdf");
  c1->SaveAs("../run/figs/day2.pdf");
//  c1->SaveAs("../run/figs/day3.pdf");
  
}

