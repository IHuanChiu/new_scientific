/* """
This module provides the correlation plots
   """
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2021-05-18"
__copyright__ = "Copyright 2021 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"
// */

#define __reference__ 1 

void mk_correlation(){

   // si32 : 76keV
   // al43 : 23keV
   // al42 : 89keV
   // fe54 : 43keV
   // fe43 : 92keV

   //numerical integration
   double black_si32 = 21651;
   double black_al43 = 1147;
   double black_al42 = 1251;
   double black_fe54 = 9090;
   double black_fe43 = 16898;
   double black_si32_error = 188;
   double black_al43_error = 113;
   double black_al42_error = 125;
   double black_fe54_error = 130;
   double black_fe43_error = 199;

   double white_si32 = 12491;
   double white_al43 = 2890;
   double white_al42 = 1714;
   double white_fe54 = 937;
   double white_fe43 = 897;
   double white_si32_error = 157;
   double white_al43_error = 124;
   double white_al42_error = 119;
   double white_fe54_error = 92;
   double white_fe43_error = 120;

   double dew_si32 = 10893;
   double dew_al43 = 882;
   double dew_al42 = 1069;
   double dew_fe54 = 2082;
   double dew_fe43 = 3667;
   double dew_si32_error = 135;
   double dew_al43_error = 81;
   double dew_al42_error = 95;
   double dew_fe54_error = 77;
   double dew_fe43_error = 111;

   double dewbar_si32 = 28830;
   double dewbar_al43 = 2201;
   double dewbar_al42 = 2842;
   double dewbar_fe54 = 5462;
   double dewbar_fe43 = 9562;
   double dewbar_si32_error = 218;
   double dewbar_al43_error = 133;
   double dewbar_al42_error = 154;
   double dewbar_fe54_error = 126;
   double dewbar_fe43_error = 183;

   double dewbar35_si32 = 19830;
   double dewbar35_al43 = 597;
   double dewbar35_al42 = 2032;
   double dewbar35_fe54 = 3033;
   double dewbar35_fe43 = 6917;
   double dewbar35_si32_error = 180;
   double dewbar35_al43_error = 102;
   double dewbar35_al42_error = 129;
   double dewbar35_fe54_error = 101;
   double dewbar35_fe43_error = 152;

   //SNIP
   double black_si32_snip = 22124.6;
   double black_al43_snip = 1488.9;
   double black_al42_snip = 1957.7;
   double black_fe54_snip = 9523.4;
   double black_fe43_snip = 18106.9;
   double black_si32_snip_error = 181;
   double black_al43_snip_error = 110.2;
   double black_al42_snip_error = 131.3;
   double black_fe54_snip_error = 129.3;
   double black_fe43_snip_error = 176.4;

   double white_si32_snip = 13154.4;
   double white_al43_snip = 3177.2;
   double white_al42_snip = 2188.3;
   double white_fe54_snip = 1306.8;
   double white_fe43_snip = 1895.1;
   double white_si32_snip_error = 149.0;
   double white_al43_snip_error = 106.0;
   double white_al42_snip_error = 117.7;
   double white_fe54_snip_error = 82.7;
   double white_fe43_snip_error = 120.0;

   double dew_si32_snip = 11191.6;
   double dew_al43_snip = 1012.4;
   double dew_al42_snip = 1436.9;
   double dew_fe54_snip = 2249.3;
   double dew_fe43_snip = 4626.2;
   double dew_si32_snip_error = 130.2;
   double dew_al43_snip_error = 70.0;
   double dew_al42_snip_error = 96.8;
   double dew_fe54_snip_error = 75.0;
   double dew_fe43_snip_error = 110.5;

   double dewbar_si32_snip = 29332.6;
   double dewbar_al43_snip = 2509.8;
   double dewbar_al42_snip = 3571.8;
   double dewbar_fe54_snip = 5960.3;
   double dewbar_fe43_snip = 12039.2;
   double dewbar_si32_snip_error = 210.5;
   double dewbar_al43_snip_error = 114.3;
   double dewbar_al42_snip_error = 168.2;
   double dewbar_fe54_snip_error = 122.8;
   double dewbar_fe43_snip_error = 178.4;

   double dewbar35_si32_snip = 20070.3;
   double dewbar35_al43_snip = 744.7;
   double dewbar35_al42_snip = 2850.6;
   double dewbar35_fe54_snip = 3407.3;
   double dewbar35_fe43_snip = 8599.1;
   double dewbar35_si32_snip_error = 173.8;
   double dewbar35_al43_snip_error = 83.7;
   double dewbar35_al42_snip_error = 144.1;
   double dewbar35_fe54_snip_error = 97.8;
   double dewbar35_fe43_snip_error = 149.9;

   //reference
   double black_alsi_ref = 0.225;
   double black_fesi_ref = 0.43;
   double black_alsi_ref_error = 0.;
   double black_fesi_ref_error = 0.;

   double white_alsi_ref = 0.8;
   double white_fesi_ref = 0.07;
   double white_alsi_ref_error = 0.;
   double white_fesi_ref_error = 0.;

   double dew_alsi_ref = 0.46;
   double dew_fesi_ref = 0.23;
   double dew_alsi_ref_error = 0.;
   double dew_fesi_ref_error = 0.;

   double dewbar_alsi_ref = 0.46;
   double dewbar_fesi_ref = 0.23;
   double dewbar_alsi_ref_error = 0.;
   double dewbar_fesi_ref_error = 0.;

   double dewbar35_alsi_ref = 0.46;
   double dewbar35_fesi_ref = 0.23;
   double dewbar35_alsi_ref_error = 0.;
   double dewbar35_fesi_ref_error = 0.;


   Double_t x[100],y[100],xe[100],ye[100];
   int np=6;
   x[0]=0;y[0]=0;xe[0]=0;ye[0]=0;
   
   TCanvas *c1 = new TCanvas("c1","c1",0,0,3200,3200);
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
   y[1]=black_alsi_ref;
   y[2]=dew_alsi_ref;
   y[3]=dewbar_alsi_ref;
   y[4]=dewbar35_alsi_ref;
   y[5]=white_alsi_ref;
#endif
   TGraph* gr = new TGraph(np,x,y);
   gr->SetMarkerStyle(8);
   gr->SetMarkerSize(2);
   gr->SetMarkerColor(4);
#if not defined(__reference__)
   gr->SetTitle(";Al(4-2)/Si(3-2);Al(4-3)/Si(3-2)");
   gr->GetXaxis()->CenterTitle("Al(4-2)/Si(3-2)"); gr->GetYaxis()->CenterTitle("Al(4-3)/Si(3-2)");
#else
   gr->SetTitle(";Al(4-2)/Si(3-2);Al/Si ref.");
   gr->GetXaxis()->CenterTitle("Al(4-2)/Si(3-2)"); gr->GetYaxis()->CenterTitle("Al/Si ref.");
#endif
   gr->Draw("");
   c1->SaveAs("/Users/chiu.i-huan/Desktop/integ_al.pdf");

   TCanvas *c2 = new TCanvas("c2","c2",0,0,3200,3200);
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
#endif
   TGraph* gr2 = new TGraph(np,x,y);
   gr2->SetMarkerStyle(8);
   gr2->SetMarkerSize(2);
   gr2->SetMarkerColor(4);
#if not defined(__reference__)
   gr2->SetTitle(";Fe(4-3)/Si(3-2);Fe(5-4)/Si(3-2)");
   gr2->GetXaxis()->CenterTitle("Fe(4-3)/Si(3-2)"); gr2->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#else
   gr2->SetTitle(";Fe/Si ref.;Fe(5-4)/Si(3-2)");
   gr2->GetXaxis()->CenterTitle("Fe/Si ref."); gr2->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#endif
   gr2->Draw("");
   c2->SaveAs("/Users/chiu.i-huan/Desktop/integ_fe.pdf");

   TCanvas *c3 = new TCanvas("c3","c3",0,0,3200,3200);
   x[1]=black_al42_snip/black_si32_snip;
   y[1]=black_al43_snip/black_si32_snip;
   xe[1]=black_al42_snip/black_si32_snip*(sqrt(pow(black_al42_snip_error/black_al42_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
   ye[1]=black_al43_snip/black_si32_snip*(sqrt(pow(black_al43_snip_error/black_al43_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
   x[3] =dew_al42_snip/dew_si32_snip;
   y[3] =dew_al43_snip/dew_si32_snip;
   xe[3]=dew_al42_snip/dew_si32_snip*(sqrt(pow(dew_al42_snip_error/dew_al42_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
   ye[3]=dew_al43_snip/dew_si32_snip*(sqrt(pow(dew_al43_snip_error/dew_al43_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
   x[2] =dewbar_al42_snip/dewbar_si32_snip;
   y[2] =dewbar_al43_snip/dewbar_si32_snip;
   xe[2]=dewbar_al42_snip/dewbar_si32_snip*(sqrt(pow(dewbar_al42_snip_error/dewbar_al42_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
   ye[2]=dewbar_al43_snip/dewbar_si32_snip*(sqrt(pow(dewbar_al43_snip_error/dewbar_al43_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
   x[4] =dewbar35_al42_snip/dewbar35_si32_snip;
   y[4] =dewbar35_al43_snip/dewbar35_si32_snip;
   xe[4]=dewbar35_al42_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_al42_snip_error/dewbar35_al42_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
   ye[4]=dewbar35_al43_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_al43_snip_error/dewbar35_al43_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
   x[5] =white_al42_snip/white_si32_snip;
   y[5] =white_al43_snip/white_si32_snip;
   xe[5]=white_al42_snip/white_si32_snip*(sqrt(pow(white_al42_snip_error/white_al42_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
   ye[5]=white_al43_snip/white_si32_snip*(sqrt(pow(white_al43_snip_error/white_al43_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
#if defined(__reference__)
   y[1]=black_alsi_ref;
   y[3]=dew_alsi_ref;
   y[2]=dewbar_alsi_ref;
   y[4]=dewbar35_alsi_ref;
   y[5]=white_alsi_ref;
#endif
   TGraph* gr3 = new TGraph(np,x,y);
   gr3->SetMarkerStyle(8);
   gr3->SetMarkerSize(2);
   gr3->SetMarkerColor(4);
#if not defined(__reference__)
   gr3->SetTitle(";Al(4-2)/Si(3-2);Al(4-3)/Si(3-2)");
   gr3->GetXaxis()->CenterTitle("Al(4-2)/Si(3-2)"); gr3->GetYaxis()->CenterTitle("Al(4-3)/Si(3-2)");
#else
   gr3->SetTitle(";Al(4-2)/Si(3-2);Al/Si ref.");
   gr3->GetXaxis()->CenterTitle("Al(4-2)/Si(3-2)"); gr->GetYaxis()->CenterTitle("Al/Si ref.");
#endif
   gr3->Draw("");
   c3->SaveAs("/Users/chiu.i-huan/Desktop/snip_al.pdf");

   TCanvas *c4 = new TCanvas("c4","c4",0,0,3200,3200);
   x[5]=black_fe43_snip/black_si32_snip;
   y[5]=black_fe54_snip/black_si32_snip;
   xe[5]=black_fe43_snip/black_si32_snip*(sqrt(pow(black_fe43_snip_error/black_fe43_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
   ye[5]=black_fe54_snip/black_si32_snip*(sqrt(pow(black_fe54_snip_error/black_fe54_snip,2)+pow(black_si32_snip_error/black_si32_snip,2)));
   x[3] =dew_fe43_snip/dew_si32_snip;
   y[3] =dew_fe54_snip/dew_si32_snip;
   xe[3]=dew_fe43_snip/dew_si32_snip*(sqrt(pow(dew_fe43_snip_error/dew_fe43_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
   ye[3]=dew_fe54_snip/dew_si32_snip*(sqrt(pow(dew_fe54_snip_error/dew_fe54_snip,2)+pow(dew_si32_snip_error/dew_si32_snip,2)));
   x[4] =dewbar_fe43_snip/dewbar_si32_snip;
   y[4] =dewbar_fe54_snip/dewbar_si32_snip;
   xe[4]=dewbar_fe43_snip/dewbar_si32_snip*(sqrt(pow(dewbar_fe43_snip_error/dewbar_fe43_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
   ye[4]=dewbar_fe54_snip/dewbar_si32_snip*(sqrt(pow(dewbar_fe54_snip_error/dewbar_fe54_snip,2)+pow(dewbar_si32_snip_error/dewbar_si32_snip,2)));
   x[2] =dewbar35_fe43_snip/dewbar35_si32_snip;
   y[2] =dewbar35_fe54_snip/dewbar35_si32_snip;
   xe[2]=dewbar35_fe43_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_fe43_snip_error/dewbar35_fe43_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
   ye[2]=dewbar35_fe54_snip/dewbar35_si32_snip*(sqrt(pow(dewbar35_fe54_snip_error/dewbar35_fe54_snip,2)+pow(dewbar35_si32_snip_error/dewbar35_si32_snip,2)));
   x[1] =white_fe43_snip/white_si32_snip;
   y[1] =white_fe54_snip/white_si32_snip;
   xe[1]=white_fe43_snip/white_si32_snip*(sqrt(pow(white_fe43_snip_error/white_fe43_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
   ye[1]=white_fe54_snip/white_si32_snip*(sqrt(pow(white_fe54_snip_error/white_fe54_snip,2)+pow(white_si32_snip_error/white_si32_snip,2)));
#if defined(__reference__)
   x[5]=black_fesi_ref;
   x[3]=dew_fesi_ref;
   x[4]=dewbar_fesi_ref;
   x[2]=dewbar35_fesi_ref;
   x[1]=white_fesi_ref;
#endif
   TGraph* gr4 = new TGraph(np,x,y);
   gr4->SetMarkerStyle(8);
   gr4->SetMarkerSize(2);
   gr4->SetMarkerColor(4);
#if not defined(__reference__)
   gr4->SetTitle(";Fe(4-3)/Si(3-2);Fe(5-4)/Si(3-2)");
   gr4->GetXaxis()->CenterTitle("Fe(4-3)/Si(3-2)"); gr4->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#else
   gr4->SetTitle(";Fe/Si ref.;Fe(5-4)/Si(3-2)");
   gr4->GetXaxis()->CenterTitle("Fe/Si ref."); gr4->GetYaxis()->CenterTitle("Fe(5-4)/Si(3-2)");
#endif
   gr4->Draw("");
   c4->SaveAs("/Users/chiu.i-huan/Desktop/snip_fe.pdf");

} 
