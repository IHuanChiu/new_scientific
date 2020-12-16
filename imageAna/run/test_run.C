
void test_run(){
TTree* t1;
TTree* t2;
TH1D* h1;
TH1D* h2;

TFile* _file0_b = new TFile("root/sample_blank_201215_2.root");
TFile* _file1_b = new TFile("root/sample_blank_collimator_201215_2.root");
TFile* _file0_p = new TFile("root/sample_particle_201215_2.root");
TFile* _file1_p = new TFile("root/sample_particle_collimator_201215_2.root");

TCanvas* c1 = new TCanvas("c1","c1",1200,1000);
t1=(TTree*)_file0_b->Get("tree"); 
t2=(TTree*)_file1_b->Get("tree"); 
t1->Draw("energy_p >> h1(500,0,200)","1/30600.*(unixtime>1607360510)","hist"); 
t2->Draw("energy_p >> h2(500,0,200)","1/76500.","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew = new TLegend(.65,.75,.85,.90); legnew->AddEntry(h1,  "w/o colli.", "l"); legnew->AddEntry(h2,  "with colli.", "l"); legnew->Draw("same");
c1->SaveAs("/Users/chiu.i-huan/Desktop/blank_ep.pdf");

TCanvas* c2 = new TCanvas("c2","c2",1200,1000);
t1=(TTree*)_file0_b->Get("tree"); 
t2=(TTree*)_file1_b->Get("tree"); 
t1->Draw("energy_n >> h1(500,0,200)","1/30600.*(unixtime>1607360510)","hist"); 
t2->Draw("energy_n >> h2(500,0,200)","1/76500.","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew2 = new TLegend(.65,.75,.85,.90); legnew2->AddEntry(h1,  "w/o colli.", "l"); legnew2->AddEntry(h2,  "with colli.", "l"); legnew2->Draw("same");
c2->SaveAs("/Users/chiu.i-huan/Desktop/blank_en.pdf");

TCanvas* c3 = new TCanvas("c3","c3",1200,1000);
t1=(TTree*)_file0_b->Get("tree"); 
t2=(TTree*)_file1_b->Get("tree"); 
t1->Draw("energy >> h1(500,0,200)","1/30600.*(unixtime>1607360510)","hist"); 
t2->Draw("energy >> h2(500,0,200)","1/76500.","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew3 = new TLegend(.65,.75,.85,.90); legnew3->AddEntry(h1,  "w/o colli.", "l"); legnew3->AddEntry(h2,  "with colli.", "l"); legnew3->Draw("same");
c3->SaveAs("/Users/chiu.i-huan/Desktop/blank_e.pdf");

TCanvas* c4 = new TCanvas("c4","c4",1200,1000);
t1=(TTree*)_file0_p->Get("tree"); 
t2=(TTree*)_file1_p->Get("tree"); 
t1->Draw("energy_p >> h1(500,0,150)","1/88740.","hist"); 
t2->Draw("energy_p >> h2(500,0,150)","1/57120.*(unixtime < 1607650460)","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew4 = new TLegend(.65,.75,.85,.90); legnew4->AddEntry(h1,  "w/o colli.", "l"); legnew4->AddEntry(h2,  "with colli.", "l"); legnew4->Draw("same");
c4->SaveAs("/Users/chiu.i-huan/Desktop/par_ep.pdf");

TCanvas* c5 = new TCanvas("c5","c5",1200,1000);
t1=(TTree*)_file0_p->Get("tree"); 
t2=(TTree*)_file1_p->Get("tree"); 
t1->Draw("energy_n >> h1(500,0,150)","1/88740.","hist"); 
t2->Draw("energy_n >> h2(500,0,150)","1/57120.*(unixtime < 1607650460)","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew5 = new TLegend(.65,.75,.85,.90); legnew5->AddEntry(h1,  "w/o colli.", "l"); legnew5->AddEntry(h2,  "with colli.", "l"); legnew5->Draw("same");
c5->SaveAs("/Users/chiu.i-huan/Desktop/par_en.pdf");

TCanvas* c6 = new TCanvas("c6","c6",1200,1000);
t1=(TTree*)_file0_p->Get("tree"); 
t2=(TTree*)_file1_p->Get("tree"); 
t1->Draw("energy >> h1(500,0,150)","1/88740.","hist"); 
t2->Draw("energy >> h2(500,0,150)","1/57120.*(unixtime < 1607650460)","hist"); 
h1 = (TH1D*)gDirectory->Get("h1");
h2 = (TH1D*)gDirectory->Get("h2");
h1->GetXaxis()->SetTitle("Energy [keV]"); 
h1->GetYaxis()->SetTitle("Counts/sec."); 
h1->SetTitle(""); h1->SetLineColor(2); 
h2->SetLineColor(4);h1->SetStats(0); 
h1->SetMaximum(h1->GetMaximum()*1.3);
h1->Draw("hist"); h2->Draw("same hist"); gPad->SetLeftMargin(0.15); TLegend* legnew6 = new TLegend(.65,.75,.85,.90); legnew6->AddEntry(h1,  "w/o colli.", "l"); legnew6->AddEntry(h2,  "with colli.", "l"); legnew6->Draw("same");
c6->SaveAs("/Users/chiu.i-huan/Desktop/par_e.pdf");


}
