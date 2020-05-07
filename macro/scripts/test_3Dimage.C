void test_3Dimage(){
Double_t px, py, pz;
TH3D *hd3 = new TH3D("hd3","hd3",32,0.,1.,32,0,1,32,.0,1.);

for (Int_t i = 0; i < 50000; i++) {

  px = gRandom->Gaus(0.5,0.2);
  py = gRandom->Gaus(0.5,0.2);
  pz = (px + py)/2.;
  hd3->Fill(px, py, pz);

}

hd3->Draw("BOX2 colz");
}
