/* """
This module provides the correlation plots
   """
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2021-05-18"
__copyright__ = "Copyright 2021 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"
// */

#include "ATLASStyle/AtlasStyle.C"
#include "ATLASStyle/AtlasLabels.C"
#include "ATLASStyle/AtlasUtils.C"

#define __reference__ 1 

void mk_correlation_fitting(){

  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();
   // si32 : 76keV
   // al43 : 23keV
   // al42 : 89keV
   // fe54 : 43keV
   // fe43 : 92keV

   //fitting method
   double black_si32 = 21796.7;
   double black_al43 = 993.5;
   double black_al42 = 1518.6;
   double black_fe54 = 9446.9;
   double black_fe43 = 18239.3;
   double black_ca43 = 10419.0;
   double black_mg32 = 5802.4;
   double black_si32_error = sqrt(black_si32);
   double black_al43_error = sqrt(black_al43);
   double black_al42_error = sqrt(black_al42);
   double black_fe54_error = sqrt(black_fe54);
   double black_fe43_error = sqrt(black_fe43);
   double black_ca43_error = sqrt(black_ca43);
   double black_mg32_error = sqrt(black_mg32);

   double white_si32 = 12959.0;
   double white_al43 = 2831.7;
   double white_al42 = 1919.4;
   double white_fe54 = 1168.7;
   double white_fe43 = 1587.5;
   double white_ca43 = 9645.5;
   double white_mg32 = 2210.8;
   double white_si32_error = sqrt(white_si32); 
   double white_al43_error = sqrt(white_al43);
   double white_al42_error = sqrt(white_al42);
   double white_fe54_error = sqrt(white_fe54);
   double white_fe43_error = sqrt(white_fe43);
   double white_ca43_error = sqrt(white_ca43);
   double white_mg32_error = sqrt(white_mg32);

   double dew_si32 = 10996.0;
   double dew_al43 = 859.7;
   double dew_al42 = 1120.3;
   double dew_fe54 = 2091.7;
   double dew_fe43 = 4478.6;
   double dew_ca43 = 5498.9;
   double dew_mg32 = 2378.9;
   double dew_si32_error = sqrt(dew_si32); 
   double dew_al43_error = sqrt(dew_al43); 
   double dew_al42_error = sqrt(dew_al42); 
   double dew_fe54_error = sqrt(dew_fe54); 
   double dew_fe43_error = sqrt(dew_fe43); 
   double dew_ca43_error = sqrt(dew_ca43); 
   double dew_mg32_error = sqrt(dew_mg32); 

   double dewbar_si32 = 28941.7; 
   double dewbar_al43 = 2162.2;
   double dewbar_al42 = 2948.0;
   double dewbar_fe54 = 5633.8;
   double dewbar_fe43 = 11903.6;
   double dewbar_ca43 = 14066.6;
   double dewbar_mg32 = 6855.0;
   double dewbar_si32_error = sqrt(dewbar_si32); 
   double dewbar_al43_error = sqrt(dewbar_al43); 
   double dewbar_al42_error = sqrt(dewbar_al42); 
   double dewbar_fe54_error = sqrt(dewbar_fe54); 
   double dewbar_fe43_error = sqrt(dewbar_fe43); 
   double dewbar_ca43_error = sqrt(dewbar_ca43); 
   double dewbar_mg32_error = sqrt(dewbar_mg32); 

   double dewbar35_si32 = 19771.5;
   double dewbar35_al43 = 617.7;
   double dewbar35_al42 = 2094.6;
   double dewbar35_fe54 = 3242.9;
   double dewbar35_fe43 = 8463.4;
   double dewbar35_ca43 = 9110.7;
   double dewbar35_mg32 = 4576.8;
   double dewbar35_si32_error = sqrt(dewbar35_si32); 
   double dewbar35_al43_error = sqrt(dewbar35_al43); 
   double dewbar35_al42_error = sqrt(dewbar35_al42); 
   double dewbar35_fe54_error = sqrt(dewbar35_fe54); 
   double dewbar35_fe43_error = sqrt(dewbar35_fe43); 
   double dewbar35_ca43_error = sqrt(dewbar35_ca43); 
   double dewbar35_mg32_error = sqrt(dewbar35_mg32); 

   //reference
   double black_alsi_ref = 0.225;
   double black_fesi_ref = 0.43;
   double black_casi_ref = 0.26;
   double black_mgsi_ref = 0.28;
   double black_alsi_ref_error = 0.;
   double black_fesi_ref_error = 0.;
   double black_casi_ref_error = 0.;
   double black_mgsi_ref_error = 0.;

   double white_alsi_ref = 0.8;
   double white_fesi_ref = 0.07;
   double white_casi_ref = 0.40;
   double white_mgsi_ref = 0.13;
   double white_alsi_ref_error = 0.;
   double white_fesi_ref_error = 0.;
   double white_casi_ref_error = 0.;
   double white_mgsi_ref_error = 0.;

   double dew_alsi_ref = 0.46;
   double dew_fesi_ref = 0.23;
   double dew_casi_ref = 0.30;
   double dew_mgsi_ref = 0.26;
   double dew_alsi_ref_error = 0.;
   double dew_fesi_ref_error = 0.;
   double dew_casi_ref_error = 0.;
   double dew_mgsi_ref_error = 0.;

   double dewbar_alsi_ref = 0.46;
   double dewbar_fesi_ref = 0.23;
   double dewbar_casi_ref = 0.30;
   double dewbar_mgsi_ref = 0.26;
   double dewbar_alsi_ref_error = 0.;
   double dewbar_fesi_ref_error = 0.;
   double dewbar_casi_ref_error = 0.;
   double dewbar_mgsi_ref_error = 0.;

   double dewbar35_alsi_ref = 0.46;
   double dewbar35_fesi_ref = 0.23;
   double dewbar35_casi_ref = 0.30;
   double dewbar35_mgsi_ref = 0.26;
   double dewbar35_alsi_ref_error = 0.;
   double dewbar35_fesi_ref_error = 0.;
   double dewbar35_casi_ref_error = 0.;
   double dewbar35_mgsi_ref_error = 0.;


   TF1 *fline = new TF1("fline","pol1",0,1);
   fline->FixParameter(0,0);
   fline->SetLineColor(2);
   Double_t x[100],y[100],xe[100],ye[100];
   int np=6;
   x[0]=0;y[0]=0;xe[0]=0;ye[0]=0;
#if defined(__reference__)
   const char *h_addname="_ref";
#else
   const char *h_addname="";
#endif
   
   TCanvas *c1 = new TCanvas("c1","c1",0,0,1000,800);
   x[1]=black_al42/black_si32;
   y[1]=black_al43/black_si32;
   xe[1]=black_al42/black_si32*(sqrt(pow(black_al42_error/black_al42,2)+pow(black_si32_error/black_si32,2)));
   ye[1]=black_al43/black_si32*(sqrt(pow(black_al43_error/black_al43,2)+pow(black_si32_error/black_si32,2)));
   x[2] =dew_al42/dew_si32;
   y[2] =dew_al43/dew_si32;
   xe[2]=dew_al42/dew_si32*(sqrt(pow(dew_al42_error/dew_al42,2)+pow(dew_si32_error/dew_si32,2)));
   ye[2]=dew_al43/dew_si32*(sqrt(pow(dew_al43_error/dew_al43,2)+pow(dew_si32_error/dew_si32,2)));
   x[3] =dewbar_al42/dewbar_si32;
   y[3] =dewbar_al43/dewbar_si32;
   xe[3]=dewbar_al42/dewbar_si32*(sqrt(pow(dewbar_al42_error/dewbar_al42,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[3]=dewbar_al43/dewbar_si32*(sqrt(pow(dewbar_al43_error/dewbar_al43,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   x[4] =dewbar35_al42/dewbar35_si32;
   y[4] =dewbar35_al43/dewbar35_si32;
   xe[4]=dewbar35_al42/dewbar35_si32*(sqrt(pow(dewbar35_al42_error/dewbar35_al42,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[4]=dewbar35_al43/dewbar35_si32*(sqrt(pow(dewbar35_al43_error/dewbar35_al43,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   x[5] =white_al42/white_si32;
   y[5] =white_al43/white_si32;
   xe[5]=white_al42/white_si32*(sqrt(pow(white_al42_error/white_al42,2)+pow(white_si32_error/white_si32,2)));
   ye[5]=white_al43/white_si32*(sqrt(pow(white_al43_error/white_al43,2)+pow(white_si32_error/white_si32,2)));
#if defined(__reference__)
   x[1]=black_alsi_ref;
   x[2]=dew_alsi_ref;
   x[3]=dewbar_alsi_ref;
   x[4]=dewbar35_alsi_ref;
   x[5]=white_alsi_ref;
   xe[1]=black_alsi_ref_error;
   xe[2]=dew_alsi_ref_error;
   xe[3]=dewbar_alsi_ref_error;
   xe[4]=dewbar35_alsi_ref_error;
   xe[5]=white_alsi_ref_error;

   y[1]=black_al42/black_si32;
   ye[1]=black_al42/black_si32*(sqrt(pow(black_al42_error/black_al42,2)+pow(black_si32_error/black_si32,2)));
   y[2] =dew_al42/dew_si32;
   ye[2]=dew_al42/dew_si32*(sqrt(pow(dew_al42_error/dew_al42,2)+pow(dew_si32_error/dew_si32,2)));
   y[3] =dewbar_al42/dewbar_si32;
   ye[3]=dewbar_al42/dewbar_si32*(sqrt(pow(dewbar_al42_error/dewbar_al42,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   y[4] =dewbar35_al42/dewbar35_si32;
   ye[4]=dewbar35_al42/dewbar35_si32*(sqrt(pow(dewbar35_al42_error/dewbar35_al42,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   y[5] =white_al42/white_si32;
   ye[5]=white_al42/white_si32*(sqrt(pow(white_al42_error/white_al42,2)+pow(white_si32_error/white_si32,2)));
#endif
   auto gr = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr->SetMarkerStyle(8);
   gr->SetMarkerSize(1);
   gr->SetMarkerColor(4);
#if not defined(__reference__)
   gr->SetTitle(";Al(4-2)/Si(3-2);Al(4-3)/Si(3-2)");
   gr->GetXaxis()->CenterTitle(); gr->GetYaxis()->CenterTitle();
#else
   gr->SetTitle(";Al/Si ref.;Al(4-2)/Si(3-2)");
   gr->GetXaxis()->CenterTitle(); gr->GetYaxis()->CenterTitle();
#endif
   gr->Draw("AP");
   auto grfit = new TGraph(np,x,y);
   std::cout << " Al fitting " << std::endl;
   grfit->Fit("fline","n");
   fline->Draw("same");
   c1->SaveAs(Form("/Users/chiu.i-huan/Desktop/integ_al%s.pdf",h_addname));

   TCanvas *c2 = new TCanvas("c2","c2",0,0,1000,800);
   x[5]=black_fe43/black_si32;
   y[5]=black_fe54/black_si32;
   xe[5]=black_fe43/black_si32*(sqrt(pow(black_fe43_error/black_fe43,2)+pow(black_si32_error/black_si32,2)));
   ye[5]=black_fe54/black_si32*(sqrt(pow(black_fe54_error/black_fe54,2)+pow(black_si32_error/black_si32,2)));
   x[4] =dew_fe43/dew_si32;
   y[4] =dew_fe54/dew_si32;
   xe[4]=dew_fe43/dew_si32*(sqrt(pow(dew_fe43_error/dew_fe43,2)+pow(dew_si32_error/dew_si32,2)));
   ye[4]=dew_fe54/dew_si32*(sqrt(pow(dew_fe54_error/dew_fe54,2)+pow(dew_si32_error/dew_si32,2)));
   x[3] =dewbar_fe43/dewbar_si32;
   y[3] =dewbar_fe54/dewbar_si32;
   xe[3]=dewbar_fe43/dewbar_si32*(sqrt(pow(dewbar_fe43_error/dewbar_fe43,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[3]=dewbar_fe54/dewbar_si32*(sqrt(pow(dewbar_fe54_error/dewbar_fe54,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   x[2] =dewbar35_fe43/dewbar35_si32;
   y[2] =dewbar35_fe54/dewbar35_si32;
   xe[2]=dewbar35_fe43/dewbar35_si32*(sqrt(pow(dewbar35_fe43_error/dewbar35_fe43,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[2]=dewbar35_fe54/dewbar35_si32*(sqrt(pow(dewbar35_fe54_error/dewbar35_fe54,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   x[1] =white_fe43/white_si32;
   y[1] =white_fe54/white_si32;
   xe[1]=white_fe43/white_si32*(sqrt(pow(white_fe43_error/white_fe43,2)+pow(white_si32_error/white_si32,2)));
   ye[1]=white_fe54/white_si32*(sqrt(pow(white_fe54_error/white_fe54,2)+pow(white_si32_error/white_si32,2)));
#if defined(__reference__)
   x[5]=black_fesi_ref;
   x[4]=dew_fesi_ref;
   x[3]=dewbar_fesi_ref;
   x[2]=dewbar35_fesi_ref;
   x[1]=white_fesi_ref;
   xe[5]=black_fesi_ref_error;
   xe[4]=dew_fesi_ref_error;
   xe[3]=dewbar_fesi_ref_error;
   xe[2]=dewbar35_fesi_ref_error;
   xe[1]=white_fesi_ref_error;
#endif
   auto gr2 = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr2->SetMarkerStyle(8);
   gr2->SetMarkerSize(1);
   gr2->SetMarkerColor(4);
#if not defined(__reference__)
   gr2->SetTitle(";Fe(4-3)/Si(3-2);Fe(5-4)/Si(3-2)");
   gr2->GetXaxis()->CenterTitle("Fe(4-3)/Si(3-2)"); gr2->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#else
   gr2->SetTitle(";Fe/Si ref.;Fe(5-4)/Si(3-2)");
   gr2->GetXaxis()->CenterTitle("Fe/Si ref."); gr2->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#endif
   gr2->Draw("AP");
   auto grfit2 = new TGraph(np,x,y);
   std::cout << " Fe fitting " << std::endl;
   grfit2->Fit("fline","n");
   fline->Draw("same");
   c2->SaveAs(Form("/Users/chiu.i-huan/Desktop/integ_fe%s.pdf",h_addname));

   TCanvas *c3 = new TCanvas("c3","c3",0,0,1000,800);
   y[5]=black_ca43/black_si32;
   y[4]=dew_ca43/dew_si32;
   y[3]=dewbar_ca43/dewbar_si32;
   y[2]=dewbar35_ca43/dewbar35_si32;
   y[1]=white_ca43/white_si32;
   ye[5]=black_ca43/black_si32*(sqrt(pow(black_ca43_error/black_ca43,2)+pow(black_si32_error/black_si32,2)));
   ye[4]=dew_ca43/dew_si32*(sqrt(pow(dew_ca43_error/dew_ca43,2)+pow(dew_si32_error/dew_si32,2)));
   ye[3]=dewbar_ca43/dewbar_si32*(sqrt(pow(dewbar_ca43_error/dewbar_ca43,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[2]=dewbar35_ca43/dewbar35_si32*(sqrt(pow(dewbar35_ca43_error/dewbar35_ca43,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[1]=white_ca43/white_si32*(sqrt(pow(white_ca43_error/white_ca43,2)+pow(white_si32_error/white_si32,2)));
#if defined(__reference__)
   x[5]=black_casi_ref;
   x[4]=dew_casi_ref;
   x[3]=dewbar_casi_ref;
   x[2]=dewbar35_casi_ref;
   x[1]=white_casi_ref;
   xe[5]=black_casi_ref_error;
   xe[4]=dew_casi_ref_error;
   xe[3]=dewbar_casi_ref_error;
   xe[2]=dewbar35_casi_ref_error;
   xe[1]=white_casi_ref_error;
#endif
   auto gr3 = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr3->SetMarkerStyle(8);
   gr3->SetMarkerSize(1);
   gr3->SetMarkerColor(4);
   gr3->SetTitle(";Ca/Si ref.;Ca(4-3)/Si(3-2)");
   gr3->GetXaxis()->CenterTitle("Ca/Si ref."); gr3->GetYaxis()->CenterTitle("Ca(4-3)/Si(3-2)");
   gr3->Draw("AP");
   auto grfit3 = new TGraph(np,x,y);
   std::cout << " Ca fitting " << std::endl;
   grfit3->Fit("fline","n");
   fline->Draw("same");
   c3->SaveAs(Form("/Users/chiu.i-huan/Desktop/integ_ca%s.pdf",h_addname));

   TCanvas *c4 = new TCanvas("c4","c4",0,0,1000,800);
   y[5]=black_mg32/black_si32;
   y[4]=dew_mg32/dew_si32;
   y[3]=dewbar_mg32/dewbar_si32;
   y[2]=dewbar35_mg32/dewbar35_si32;
   y[1]=white_mg32/white_si32;
   ye[5]=black_mg32/black_si32*(sqrt(pow(black_mg32_error/black_mg32,2)+pow(black_si32_error/black_si32,2)));
   ye[4]=dew_mg32/dew_si32*(sqrt(pow(dew_mg32_error/dew_mg32,2)+pow(dew_si32_error/dew_si32,2)));
   ye[3]=dewbar_mg32/dewbar_si32*(sqrt(pow(dewbar_mg32_error/dewbar_mg32,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[2]=dewbar35_mg32/dewbar35_si32*(sqrt(pow(dewbar35_mg32_error/dewbar35_mg32,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[1]=white_mg32/white_si32*(sqrt(pow(white_mg32_error/white_mg32,2)+pow(white_si32_error/white_si32,2)));
#if defined(__reference__)
   x[5]=black_mgsi_ref;
   x[4]=dew_mgsi_ref;
   x[3]=dewbar_mgsi_ref;
   x[2]=dewbar35_mgsi_ref;
   x[1]=white_mgsi_ref;
   xe[5]=black_mgsi_ref_error;
   xe[4]=dew_mgsi_ref_error;
   xe[3]=dewbar_mgsi_ref_error;
   xe[2]=dewbar35_mgsi_ref_error;
   xe[1]=white_mgsi_ref_error;
#endif
   auto gr4 = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr4->SetMarkerStyle(8);
   gr4->SetMarkerSize(1);
   gr4->SetMarkerColor(4);
   gr4->SetTitle(";Mg/Si ref.;Mg(3-2)/Si(3-2)");
   gr4->GetXaxis()->CenterTitle("Mg/Si ref."); gr4->GetYaxis()->CenterTitle("Mg(3-2)/Si(3-2)");
   gr4->Draw("AP");
   auto grfit4 = new TGraph(np,x,y);
   std::cout << " Mg fitting " << std::endl;
   grfit4->Fit("fline","n");
   fline->Draw("same");
   c4->SaveAs(Form("/Users/chiu.i-huan/Desktop/integ_mg%s.pdf",h_addname));


   TCanvas *c5 = new TCanvas("c5","c5",0,0,1000,800);
   x[5]=black_fe54/black_si32;
   y[5]=black_al42/black_si32;
   xe[5]=black_fe54/black_si32*(sqrt(pow(black_fe54_error/black_fe54,2)+pow(black_si32_error/black_si32,2)));
   ye[5]=black_al42/black_si32*(sqrt(pow(black_al42_error/black_al42,2)+pow(black_si32_error/black_si32,2)));
   x[4] =dew_fe54/dew_si32;
   y[4] =dew_al42/dew_si32;
   xe[4]=dew_fe54/dew_si32*(sqrt(pow(dew_fe54_error/dew_fe54,2)+pow(dew_si32_error/dew_si32,2)));
   ye[4]=dew_al42/dew_si32*(sqrt(pow(dew_al42_error/dew_al42,2)+pow(dew_si32_error/dew_si32,2)));
   x[3] =dewbar_fe54/dewbar_si32;
   y[3] =dewbar_al42/dewbar_si32;
   xe[3]=dewbar_fe54/dewbar_si32*(sqrt(pow(dewbar_fe54_error/dewbar_fe54,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[3]=dewbar_al42/dewbar_si32*(sqrt(pow(dewbar_al42_error/dewbar_al42,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   x[2] =dewbar35_fe54/dewbar35_si32;
   y[2] =dewbar35_al42/dewbar35_si32;
   xe[2]=dewbar35_fe54/dewbar35_si32*(sqrt(pow(dewbar35_fe54_error/dewbar35_fe54,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[2]=dewbar35_al42/dewbar35_si32*(sqrt(pow(dewbar35_al42_error/dewbar35_al42,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   x[1] =white_fe54/white_si32;
   y[1] =white_al42/white_si32;
   xe[1]=white_fe54/white_si32*(sqrt(pow(white_fe54_error/white_fe54,2)+pow(white_si32_error/white_si32,2)));
   ye[1]=white_al42/white_si32*(sqrt(pow(white_al42_error/white_al42,2)+pow(white_si32_error/white_si32,2)));   
   auto gr5_iter = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr5_iter->SetTitle(";Fe(5-4)/Si(3-2);Al(4-2)/Si(3-2)");
   gr5_iter->GetXaxis()->CenterTitle("Fe(5-4)/Si(3-2)"); gr5_iter->GetYaxis()->CenterTitle("Al(4-2)/Si(3-2)");
   gr5_iter->SetMarkerStyle(8);
   gr5_iter->SetMarkerSize(1);
   gr5_iter->SetMarkerColor(4);
   gr5_iter->Draw("AP");
   c5->SaveAs("/Users/chiu.i-huan/Desktop/comparison_feal_iter.pdf");

//   TCanvas *c6 = new TCanvas("c6","c6",0,0,1000,800);
//   x[5]=black_fe43_snip/black_si32_snip;
//   y[5]=black_al42_snip/black_si32_snip;
//   xe[5]=black_fe43_snip/black_si32_snip*(sqrt(pow(black_fe43_snip_error/black_fe43_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
//   ye[5]=black_al42_snip/black_si32_snip*(sqrt(pow(black_al42_snip_error/black_al42_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
//   x[4] =dew_fe43_snip/dew_si32_snip;
//   y[4] =dew_al42_snip/dew_si32_snip;
//   xe[4]=dew_fe43_snip/dew_si32_snip*(sqrt(pow(dew_fe43_snip_error/dew_fe43_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
//   ye[4]=dew_al42_snip/dew_si32_snip*(sqrt(pow(dew_al42_snip_error/dew_al42_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
//   x[3] =dewbar_fe43_snip/dewbar_si32_snip;
//   y[3] =dewbar_al42_snip/dewbar_si32_snip;
//   xe[3]=dewbar_fe43_snip/dewbar_si32_snip*(sqrt(pow(dewbar_fe43_snip_error/dewbar_fe43_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
//   ye[3]=dewbar_al42_snip/dewbar_si32_snip*(sqrt(pow(dewbar_al42_snip_error/dewbar_al42_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
//   x[2] =dewbar35_fe43_snip/dewbar35_si32_snip;
//   y[2] =dewbar35_al42_snip/dewbar35_si32_snip;
//   xe[2]=dewbar35_fe43_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_fe43_snip_error/dewbar35_fe43_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
//   ye[2]=dewbar35_al42_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_al42_snip_error/dewbar35_al42_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
//   x[1] =white_fe43_snip/white_si32_snip;
//   y[1] =white_al42_snip/white_si32_snip;
//   xe[1]=white_fe43_snip/white_si32_snip*(sqrt(pow(white_fe43_snip_error/white_fe43_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
//   ye[1]=white_al42_snip/white_si32_snip*(sqrt(pow(white_al42_snip_error/white_al42_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));   
//   auto gr5_snip = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
//   gr5_snip->SetMarkerStyle(8);
//   gr5_snip->SetMarkerSize(1);
//   gr5_snip->SetMarkerColor(2);
//   Double_t x_color,y_color;
//   TMarker *m;
//   /*
//   gr5_snip->GetPoint(4,x_color,y_color);//dewbar
//   m = new TMarker(x_color,y_color,20);
//   m->SetMarkerColor(3);
//   m->Paint();
//   gr5_snip->GetPoint(3,x_color,y_color);//dewbar35
//   m = new TMarker(x_color,y_color,20);
//   m->SetMarkerColor(4);
//   m->Paint();// */
//   gr5_snip->Draw("AP");
//   gr5_snip->SetTitle(";Fe(4-3)/Si(3-2);Al(4-2)/Si(3-2)");
//   gr5_snip->GetXaxis()->CenterTitle(); gr5_snip->GetYaxis()->CenterTitle();
//   c6->SaveAs("/Users/chiu.i-huan/Desktop/comparison_fe43al_snip.pdf");


//   TCanvas *c7 = new TCanvas("c7","c7",0,0,2000,800);
//   c7->Divide(2,1);
//   c7->cd(1);
//   x[1]=black_al42_snip/black_si32_snip;
//   y[1]=black_al42_snip/black_o21_snip;
//   xe[1]=black_al42_snip/black_si32_snip*(sqrt(pow(black_al42_snip_error/black_al42_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
//   ye[1]=black_al42_snip/black_o21_snip*(sqrt(pow(black_al42_snip_error/black_al42_snip,2)+pow(black_o21_snip_error/black_o21_snip,2)));
//   x[3] =dew_al42_snip/dew_si32_snip;
//   y[3] =dew_al42_snip/dew_o21_snip;
//   xe[3]=dew_al42_snip/dew_si32_snip*(sqrt(pow(dew_al42_snip_error/dew_al42_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
//   ye[3]=dew_al42_snip/dew_o21_snip*(sqrt(pow(dew_al42_snip_error/dew_al42_snip,2)+pow(dew_o21_snip_error/dew_o21_snip,2)));
//   x[2] =dewbar_al42_snip/dewbar_si32_snip;
//   y[2] =dewbar_al42_snip/dewbar_o21_snip;
//   xe[2]=dewbar_al42_snip/dewbar_si32_snip*(sqrt(pow(dewbar_al42_snip_error/dewbar_al42_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
//   ye[2]=dewbar_al42_snip/dewbar_o21_snip*(sqrt(pow(dewbar_al42_snip_error/dewbar_al42_snip,2)+pow(dewbar_o21_snip_error/dewbar_o21_snip,2)));
//   x[4] =dewbar35_al42_snip/dewbar35_si32_snip;
//   y[4] =dewbar35_al42_snip/dewbar35_o21_snip;
//   xe[4]=dewbar35_al42_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_al42_snip_error/dewbar35_al42_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
//   ye[4]=dewbar35_al42_snip/dewbar35_o21_snip*(sqrt(pow(dewbar35_al42_snip_error/dewbar35_al42_snip,2)+pow(dewbar35_o21_snip_error/dewbar35_o21_snip,2)));
//   x[5] =white_al42_snip/white_si32_snip;
//   y[5] =white_al42_snip/white_o21_snip;
//   xe[5]=white_al42_snip/white_si32_snip*(sqrt(pow(white_al42_snip_error/white_al42_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
//   ye[5]=white_al42_snip/white_o21_snip*(sqrt(pow(white_al42_snip_error/white_al42_snip,2)+pow(white_o21_snip_error/white_o21_snip,2)));
//   auto gr7_iter = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
//   gr7_iter->SetTitle(";Al(4-2)/Si(3-2);Al(4-2)/O(2-1)");
//   gr7_iter->GetXaxis()->CenterTitle(); gr7_iter->GetYaxis()->CenterTitle();
//   gr7_iter->SetMarkerStyle(8);
//   gr7_iter->SetMarkerSize(1);
//   gr7_iter->SetMarkerColor(4);
//   gr7_iter->Draw("AP");
//   auto grfit7 = new TGraph(np,x,y);
//   grfit7->Fit("fline","n");
//   fline->Draw("same");
//   c7->cd(2);
//   x[5]=black_fe43_snip/black_si32_snip;
//   y[5]=black_fe43_snip/black_o21_snip;
//   xe[5]=black_fe43_snip/black_si32_snip*(sqrt(pow(black_fe43_snip_error/black_fe43_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
//   ye[5]=black_fe43_snip/black_o21_snip*(sqrt(pow(black_fe43_snip_error/black_fe43_snip,2)+pow(black_o21_snip_error/black_o21_snip,2)));
//   x[3] =dew_fe43_snip/dew_si32_snip;
//   y[3] =dew_fe43_snip/dew_o21_snip;
//   xe[3]=dew_fe43_snip/dew_si32_snip*(sqrt(pow(dew_fe43_snip_error/dew_fe43_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
//   ye[3]=dew_fe43_snip/dew_o21_snip*(sqrt(pow(dew_fe43_snip_error/dew_fe43_snip,2)+pow(dew_o21_snip_error/dew_o21_snip,2)));
//   x[4] =dewbar_fe43_snip/dewbar_si32_snip;
//   y[4] =dewbar_fe43_snip/dewbar_o21_snip;
//   xe[4]=dewbar_fe43_snip/dewbar_si32_snip*(sqrt(pow(dewbar_fe43_snip_error/dewbar_fe43_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
//   ye[4]=dewbar_fe43_snip/dewbar_o21_snip*(sqrt(pow(dewbar_fe43_snip_error/dewbar_fe43_snip,2)+pow(dewbar_o21_snip_error/dewbar_o21_snip,2)));
//   x[2] =dewbar35_fe43_snip/dewbar35_si32_snip;
//   y[2] =dewbar35_fe43_snip/dewbar35_o21_snip;
//   xe[2]=dewbar35_fe43_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_fe43_snip_error/dewbar35_fe43_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
//   ye[2]=dewbar35_fe43_snip/dewbar35_o21_snip*(sqrt(pow(dewbar35_fe43_snip_error/dewbar35_fe43_snip,2)+pow(dewbar35_o21_snip_error/dewbar35_o21_snip,2)));
//   x[1] =white_fe43_snip/white_si32_snip;
//   y[1] =white_fe43_snip/white_o21_snip;
//   xe[1]=white_fe43_snip/white_si32_snip*(sqrt(pow(white_fe43_snip_error/white_fe43_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
//   ye[1]=white_fe43_snip/white_o21_snip*(sqrt(pow(white_fe43_snip_error/white_fe43_snip,2)+pow(white_o21_snip_error/white_o21_snip,2)));
//   auto gr8_iter = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
//   gr8_iter->SetTitle(";Fe(4-3)/Si(3-2);Fe(4-3)/O(2-1)");
//   gr8_iter->GetXaxis()->CenterTitle(); gr8_iter->GetYaxis()->CenterTitle();
//   gr8_iter->SetMarkerStyle(8);
//   gr8_iter->SetMarkerSize(1);
//   gr8_iter->SetMarkerColor(4);
//   gr8_iter->Draw("AP");
//   auto grfit8 = new TGraph(np,x,y);
//   grfit8->Fit("fline","n");
//   fline->Draw("same");
//   c7->SaveAs("/Users/chiu.i-huan/Desktop/comparison_siVS.O_snip.pdf");
} 
