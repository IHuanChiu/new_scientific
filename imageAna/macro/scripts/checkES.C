void checkES(){
TString name;
TString filename;
TString name2;

TString place="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/cali_plots";
TString sourcename="Co";//show Am, Ba, Co lines
TString caliname="merge1008";//merge1008,Am,Ba,Co

// === calibration data ===
//filename.Form("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/2mmCdTe_root/cdtedsd_2020b_0720a_%ssource_cali%s.root",sourcename.Data(),caliname.Data());
//TFile* ff = new TFile(filename.Data(),"read");
//name.Form("%s/canv_%ssource_cali%s_lv1.pdf",place.Data(),sourcename.Data(),caliname.Data());
//name2.Form("%s/canv_%ssource_cali%s_gamma.pdf",place.Data(),sourcename.Data(),caliname.Data());

// === other data ===
TFile* ff = new TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/2mmCdTe_root/cdtedsd_2020b_0917a_battery_Ba.root","read");
name.Form("%s/canv_energyspectrum_lv1_temp.pdf",place.Data());
name2.Form("%s/canv_energyspectrum_gamma_temp.pdf",place.Data());

TTree* t = (TTree*)ff->Get("tree");


// ===== Lv1 hit energy ===
//TCanvas *c1 = new TCanvas(name.Data(), name.Data(), 500, 500);
//c1->Print(name + "[", "pdf");
//for (int i = 0; i < 128; i++){
//  t->Draw("E_p_lv1 >> h1(400,0,200)",Form("Stripid_x_lv1==%d",i));
//  TH1D* h1=(TH1D*)gDirectory->Get("h1");
//  h1->SetTitle(Form("Ch : %d",i));
//  h1->SetStats(0);
//  h1->SetLineColor(1);
//
//  if(sourcename == "Am"){
//    TLine *lineUp = new TLine(59.5,0,59.5,h1->GetMaximum());
//    TLine *lineDown = new TLine(13.94,0,13.94,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }else if (sourcename == "Ba"){
//    TLine *lineUp = new TLine(31,0,31,h1->GetMaximum());
//    TLine *lineDown = new TLine(81,0,81,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }else if (sourcename == "Co"){
//    TLine *lineUp = new TLine(14.41,0,14.41,h1->GetMaximum());
//    TLine *lineDown = new TLine(122.06,0,122.06,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }
//
//  c1->Print(name, "pdf");  
//}
//for (int i = 128; i < 256; i++){
//  t->Draw("E_n_lv1 >> h1(400,0,200)",Form("Stripid_y_lv1==%d",i));
//  TH1D* h1=(TH1D*)gDirectory->Get("h1");
//  h1->SetTitle(Form("Ch : %d",i));
//  h1->SetStats(0);
//
//  if(sourcename == "Am"){
//    TLine *lineUp = new TLine(59.5,0,59.5,h1->GetMaximum());
//    TLine *lineDown = new TLine(13.94,0,13.94,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }else if (sourcename == "Ba"){
//    TLine *lineUp = new TLine(31,0,31,h1->GetMaximum());
//    TLine *lineDown = new TLine(81,0,81,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }else if (sourcename == "Co"){
//    TLine *lineUp = new TLine(14.41,0,14.41,h1->GetMaximum());
//    TLine *lineDown = new TLine(122.06,0,122.06,h1->GetMaximum());
//    lineUp->SetLineColorAlpha(kRed, 0.9);
//    lineDown->SetLineColorAlpha(kRed, 0.9);
//    lineUp->Draw("same");
//    lineDown->Draw("same");
//  }
//
//  c1->Print(name, "pdf");  
//}
//c1->Print(name + "]", "pdf");


TCanvas *c2 = new TCanvas(name2.Data(), name2.Data(), 500, 500);
c2->Print(name2 + "[", "pdf");
for (int i = 0; i < 128; i++){
  t->Draw("energy_p >> h1(400,0,200)",Form("Stripid_x_lv1==%d",i));
  TH1D* h1=(TH1D*)gDirectory->Get("h1");
  h1->SetTitle(Form("Ch : %d",i));
  h1->SetStats(0);
  h1->SetLineColor(1);

  if(sourcename == "Am"){
    TLine *lineUp = new TLine(59.5,0,59.5,h1->GetMaximum());
    TLine *lineDown = new TLine(13.94,0,13.94,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }else if (sourcename == "Ba"){
    TLine *lineUp = new TLine(31,0,31,h1->GetMaximum());
    TLine *lineDown = new TLine(81,0,81,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }else if (sourcename == "Co"){
    TLine *lineUp = new TLine(14.41,0,14.41,h1->GetMaximum());
    TLine *lineDown = new TLine(122.06,0,122.06,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }

  c2->Print(name2, "pdf");  
}
for (int i = 128; i < 256; i++){
  t->Draw("energy_n >> h1(400,0,200)",Form("Stripid_y_lv1==%d",i));
  TH1D* h1=(TH1D*)gDirectory->Get("h1");
  h1->SetTitle(Form("Ch : %d",i));
  h1->SetStats(0);
  h1->SetLineColor(1);

  if(sourcename == "Am"){
    TLine *lineUp = new TLine(59.5,0,59.5,h1->GetMaximum());
    TLine *lineDown = new TLine(13.94,0,13.94,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }else if (sourcename == "Ba"){
    TLine *lineUp = new TLine(31,0,31,h1->GetMaximum());
    TLine *lineDown = new TLine(81,0,81,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }else if (sourcename == "Co"){
    TLine *lineUp = new TLine(14.41,0,14.41,h1->GetMaximum());
    TLine *lineDown = new TLine(122.06,0,122.06,h1->GetMaximum());
    lineUp->SetLineColorAlpha(kRed, 0.9);
    lineDown->SetLineColorAlpha(kRed, 0.9);
    lineUp->Draw("same");
    lineDown->Draw("same");
  }

  c2->Print(name2, "pdf");  
}
c2->Print(name2 + "]", "pdf");


  // 実は、この最後のファイルを閉じる間に、別にのTCanvasオブジェクトを保存することもできる
  // 上の一文の代わりに下記のようにする
  // c2->Print(name, "pdf")
  // c2->Print(name + "]", "pdf")



//TFile* f1 = TFile("../../run/figs/repro_3Dimage.root","read")
//
//Double_t px, py, pz;
//TH3D *hd3 = new TH3D("hd3","hd3",32,0.,1.,32,0,1,32,.0,1.);
//
//for (Int_t i = 0; i < 50000; i++) {
//
//  px = gRandom->Gaus(0.5,0.2);
//  py = gRandom->Gaus(0.5,0.2);
//  pz = (px + py)/2.;
//  hd3->Fill(px, py, pz);
//
//}
//
//hd3->Draw("BOX2 colz");
}
