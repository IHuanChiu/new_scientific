void tree_test(){
   TFile *f = new TFile("mytest.root","recreate");
   TTree*T = new TTree("T","simple");
   Int_t a;
   Double_t pt;
   Double_t vec[a];
   T->Branch("pt",&pt,"pt/D");
   T->Branch("a",&a,"a/I");
   T->Branch("vec",&vec,"veci[a]/D");
   for (int i = 0; i<10;i++){
    a = i;
    pt = i*10.1;
    vec[i] = i*20;
    T->Fill();
   }
   f->Write();
}
