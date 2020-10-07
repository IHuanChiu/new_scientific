void test_3Dimage(){

TString name;
name.Form("canv.pdf");
TCanvas *c1 = new TCanvas(name.Data(), name.Data(), 1000, 500);
c1->Print(name + "[", "pdf");    // ここで"canv.pdf"を開く感じ
int Nhists = 10;
TH1D* hist[10];

for (Int_t ihist = 0; ihist < Nhists; ihist++) {
    hist[ihist] = new TH1D("AA","AA",10,0,10);
    hist[ihist]->Draw();
    c1->Print(name, "pdf");       // ここで、キャンバスを保存する
}
 
c1->Print(name + "]", "pdf");    // ここで"canv.pdf"を閉じる感じ
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
