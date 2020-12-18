
void test_image(){
TTree* tpn;TTree* tp; TTree* tbn;TTree* tb;
TH2D* hp_l; TH2D* hpn_l; TH2D* hb_l; TH2D* hbn_l;
TH2D* hp_h; TH2D* hpn_h; TH2D* hb_h; TH2D* hbn_h;

TFile* _file0_b = new TFile("root/sample_blank_201215_2.root");
TFile* _file1_b = new TFile("root/sample_blank_collimator_201215_2.root");
TFile* _file0_p = new TFile("root/sample_particle_201215_2.root");
TFile* _file1_p = new TFile("root/sample_particle_collimator_201215_2.root");

tbn = (TTree*)_file0_b->Get("tree");
tb = (TTree*)_file1_b->Get("tree");
tpn = (TTree*)_file0_p->Get("tree");
tp = (TTree*)_file1_p->Get("tree");

tbn->Draw("y:x >> hbn_l(128,-16,16,128,-16,16)","energy > 55 && energy < 65","colz");
tbn->Draw("y:x >> hbn_h(128,-16,16,128,-16,16)","energy > 75 && energy < 140","colz");
tb->Draw("y:x >> hb_l(128,-16,16,128,-16,16)","energy > 55 && energy < 65","colz");
tb->Draw("y:x >> hb_h(128,-16,16,128,-16,16)","energy > 75 && energy < 140","colz");
tpn->Draw("y:x >> hpn_l(128,-16,16,128,-16,16)","energy > 55 && energy < 65","colz");
tpn->Draw("y:x >> hpn_h(128,-16,16,128,-16,16)","energy > 75 && energy < 140","colz");
tp->Draw("y:x >> hp_l(128,-16,16,128,-16,16)","energy > 55 && energy < 65","colz");
tp->Draw("y:x >> hp_h(128,-16,16,128,-16,16)","energy > 75 && energy < 140","colz");

hbn_l = (TH2D*)gDirectory->Get("hbn_l");
hbn_h = (TH2D*)gDirectory->Get("hbn_h");
hb_l = (TH2D*)gDirectory->Get("hb_l");
hb_h = (TH2D*)gDirectory->Get("hb_h");
hpn_l = (TH2D*)gDirectory->Get("hpn_l");
hpn_h = (TH2D*)gDirectory->Get("hpn_h");
hp_l = (TH2D*)gDirectory->Get("hp_l");
hp_h = (TH2D*)gDirectory->Get("hp_h");

hbn_l->SetStats(0);
hbn_h->SetStats(0);
hb_l->SetStats(0);
hb_h->SetStats(0);
hpn_l->SetStats(0);
hpn_h->SetStats(0);
hp_l->SetStats(0);
hp_h->SetStats(0);

TCanvas* c1 = new TCanvas("c1","c1",800,1600);
TCanvas* c2 = new TCanvas("c2","c2",800,1600);
c1->Divide(2,2);
c2->Divide(2,2);

hbn_l->SetTitle(" blank, w/o colli. 55 < energy < 65");
hbn_h->SetTitle(" blank, w/o colli. 75 < energy < 140");
hb_l->SetTitle(" blank, with colli. 55 < energy < 65");
hb_h->SetTitle(" blank, with colli. 75 < energy < 140");
hpn_l->SetTitle(" parti., w/o colli. 55 < energy < 65");
hpn_h->SetTitle(" parti., w/o colli. 75 < energy < 140");
hp_l->SetTitle(" parti., with colli. 55 < energy < 65");
hp_h->SetTitle(" parti., with colli. 75 < energy < 140");

hbn_l->GetXaxis()->SetTitle("X[mm]");
hbn_l->GetYaxis()->SetTitle("Y[mm]");
hbn_h->GetXaxis()->SetTitle("X[mm]");
hbn_h->GetYaxis()->SetTitle("Y[mm]");
hb_l->GetXaxis()->SetTitle("X[mm]");
hb_l->GetYaxis()->SetTitle("Y[mm]");
hb_h->GetXaxis()->SetTitle("X[mm]");
hb_h->GetYaxis()->SetTitle("Y[mm]");
hpn_l->GetXaxis()->SetTitle("X[mm]");
hpn_l->GetYaxis()->SetTitle("Y[mm]");
hpn_h->GetXaxis()->SetTitle("X[mm]");
hpn_h->GetYaxis()->SetTitle("Y[mm]");
hp_l->GetXaxis()->SetTitle("X[mm]");
hp_l->GetYaxis()->SetTitle("Y[mm]");
hp_h->GetXaxis()->SetTitle("X[mm]");
hp_h->GetYaxis()->SetTitle("Y[mm]");


c1->cd(1);
gStyle->SetPalette(53);
hbn_l->Draw("colz");
c1->cd(2);
gStyle->SetPalette(53);
hbn_h->Draw("colz");
c1->cd(3);
gStyle->SetPalette(53);
hb_l->Draw("colz");
c1->cd(4);
gStyle->SetPalette(53);
hb_h->Draw("colz");

c2->cd(1);
gStyle->SetPalette(53);
hpn_l->Draw("colz");
c2->cd(2);
gStyle->SetPalette(53);
hpn_h->Draw("colz");
c2->cd(3);
gStyle->SetPalette(53);
hp_l->Draw("colz");
c2->cd(4);
gStyle->SetPalette(53);
hp_h->Draw("colz");

c1->SaveAs("/Users/chiu.i-huan/Desktop/image_blank.pdf");
c2->SaveAs("/Users/chiu.i-huan/Desktop/image_particle.pdf");


}
