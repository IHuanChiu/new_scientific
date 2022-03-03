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

#if defined(__reference__)
   const char *h_addname="_ref";
#else
   const char *h_addname="";
#endif

void mk_correlation_fitting(){
gROOT->ProcessLine("gErrorIgnoreLevel = kFatal;");
// *** bin_index ***
//1 Si32 : 76 keV 
//2 Al43 : 23 keV 
//3 Al42 : 89 keV 
//4 Fe54 : 43 keV 
//5 Fe43 : 92 keV 
//6 Ca43 : 55 keV 
//7 Ca32 : 156 keV 
//8 Mg32 : 66 keV 
//9 Cu43 : 116 keV 
//10 Fegamma : 126 keV
   
  #ifdef __CINT__
    gROOT->LoadMacro("AtlasLabels.C");
    gROOT->LoadMacro("AtlasUtils.C");
  #endif
  SetAtlasStyle();

  // *** set reference (from terada) ***
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

  // *** get all hist. ***
  TFile *hint = new TFile("./intensity_files/intensity_sum.root","read");
  TH1F *h_white[7], *h_black[7], *h_dew[7], *h_dewbar[7], *h_dewbar35[7];
  for (int i = 0; i < 6; i++){
     h_white[i+1]=(TH1F*)hint->Get(Form("white_CH%d",i+1));
     h_black[i+1]=(TH1F*)hint->Get(Form("black_CH%d",i+1));
     h_dew[i+1]=(TH1F*)hint->Get(Form("dew_CH%d",i+1));
     h_dewbar[i+1]=(TH1F*)hint->Get(Form("dewbar_CH%d",i+1));
     h_dewbar35[i+1]=(TH1F*)hint->Get(Form("dew_35_CH%d",i+1));
  }
  h_white[0] = (TH1F*)h_white[1]->Clone();
  h_black[0] = (TH1F*)h_black[1]->Clone();
  h_dew[0] = (TH1F*)h_dew[1]->Clone();
  h_dewbar[0] = (TH1F*)h_dewbar[1]->Clone();
  h_dewbar35[0] = (TH1F*)h_dewbar35[1]->Clone();
  for (int j = 2; j < 7; j++){
     h_white[0]->Add(h_white[j],1);
     h_black[0]->Add(h_black[j],1);
     h_dew[0]->Add(h_dew[j],1);
     h_dewbar[0]->Add(h_dewbar[j],1);
     h_dewbar35[0]->Add(h_dewbar35[j],1);
  }
  
  
  // *** Set par. for hist. ***
  TH1F* h_white_sum, *h_black_sum, *h_dew_sum, *h_dewbar_sum, *h_dewbar35_sum;
  TF1 *fline[5][7];//[Types][Chs]
  TCanvas *c[5][7];
  TGraphAsymmErrors* gr[5][7];
  TGraph *grfit[5][7];
  Double_t x[10],y[10],xe[10],ye[10];
  int np=6;//five samples + zero point
  x[0]=0;y[0]=0;xe[0]=0;ye[0]=0;

  
  // *** loop hist. ***
  for (int hist_id=0; hist_id < 7; hist_id++){
     std::cout << "\n" << std::endl;
     std::cout << " *** CH index : " << hist_id << " *** " << std::endl;
     h_white_sum = (TH1F*)h_white[hist_id]->Clone();
     h_black_sum = (TH1F*)h_black[hist_id]->Clone();
     h_dew_sum = (TH1F*)h_dew[hist_id]->Clone();
     h_dewbar_sum =(TH1F*)h_dewbar[hist_id]->Clone();
     h_dewbar35_sum = (TH1F*)h_dewbar35[hist_id]->Clone();

   //fitting value
   double black_si32 =h_black_sum->GetBinContent(1); 
   double black_al43 =h_black_sum->GetBinContent(2); 
   double black_al42 =h_black_sum->GetBinContent(3); 
   double black_fe54 =h_black_sum->GetBinContent(4); 
   double black_fe43 =h_black_sum->GetBinContent(5); 
   double black_ca43 =h_black_sum->GetBinContent(6)-0.172*h_black_sum->GetBinContent(10); 
   double black_ca32 =h_black_sum->GetBinContent(7)-0.172*h_black_sum->GetBinContent(10); 
   double black_mg32 =h_black_sum->GetBinContent(8); 
   double black_si32_error = h_black_sum->GetBinError(1);
   double black_al43_error = h_black_sum->GetBinError(2);
   double black_al42_error = h_black_sum->GetBinError(3);
   double black_fe54_error = h_black_sum->GetBinError(4);
   double black_fe43_error = h_black_sum->GetBinError(5);
   double black_ca43_error = h_black_sum->GetBinError(6);
   double black_ca32_error = h_black_sum->GetBinError(7);
   double black_mg32_error = h_black_sum->GetBinError(8);

   double white_si32 =h_white_sum->GetBinContent(1); 
   double white_al43 =h_white_sum->GetBinContent(2); 
   double white_al42 =h_white_sum->GetBinContent(3); 
   double white_fe54 =h_white_sum->GetBinContent(4); 
   double white_fe43 =h_white_sum->GetBinContent(5); 
   double white_ca43 =h_white_sum->GetBinContent(6)-0.172*h_dew_sum->GetBinContent(10); 
   double white_ca32 =h_white_sum->GetBinContent(7)-0.172*h_dew_sum->GetBinContent(10); 
   double white_mg32 =h_white_sum->GetBinContent(8); 
   double white_si32_error = h_white_sum->GetBinError(1); 
   double white_al43_error = h_white_sum->GetBinError(2);
   double white_al42_error = h_white_sum->GetBinError(3);
   double white_fe54_error = h_white_sum->GetBinError(4);
   double white_fe43_error = h_white_sum->GetBinError(5);
   double white_ca43_error = h_white_sum->GetBinError(6);
   double white_ca32_error = h_white_sum->GetBinError(7);
   double white_mg32_error = h_white_sum->GetBinError(8);

   double dew_si32 =h_dew_sum->GetBinContent(1); 
   double dew_al43 =h_dew_sum->GetBinContent(2); 
   double dew_al42 =h_dew_sum->GetBinContent(3); 
   double dew_fe54 =h_dew_sum->GetBinContent(4); 
   double dew_fe43 =h_dew_sum->GetBinContent(5); 
   double dew_ca43 =h_dew_sum->GetBinContent(6)-0.172*h_dew_sum->GetBinContent(10); 
   double dew_ca32 =h_dew_sum->GetBinContent(7)-0.172*h_dew_sum->GetBinContent(10); 
   double dew_mg32 =h_dew_sum->GetBinContent(8); 
   double dew_si32_error = h_dew_sum->GetBinError(1); 
   double dew_al43_error = h_dew_sum->GetBinError(2); 
   double dew_al42_error = h_dew_sum->GetBinError(3); 
   double dew_fe54_error = h_dew_sum->GetBinError(4); 
   double dew_fe43_error = h_dew_sum->GetBinError(5); 
   double dew_ca43_error = h_dew_sum->GetBinError(6); 
   double dew_ca32_error = h_dew_sum->GetBinError(7); 
   double dew_mg32_error = h_dew_sum->GetBinError(8); 

   double dewbar_si32 =h_dewbar_sum->GetBinContent(1); 
   double dewbar_al43 =h_dewbar_sum->GetBinContent(2); 
   double dewbar_al42 =h_dewbar_sum->GetBinContent(3); 
   double dewbar_fe54 =h_dewbar_sum->GetBinContent(4); 
   double dewbar_fe43 =h_dewbar_sum->GetBinContent(5); 
   double dewbar_ca43 =h_dewbar_sum->GetBinContent(6)-0.172*h_dewbar_sum->GetBinContent(10); 
   double dewbar_ca32 =h_dewbar_sum->GetBinContent(7)-0.172*h_dewbar_sum->GetBinContent(10); 
   double dewbar_mg32 =h_dewbar_sum->GetBinContent(8); 
   double dewbar_si32_error = h_dewbar_sum->GetBinError(1); 
   double dewbar_al43_error = h_dewbar_sum->GetBinError(2); 
   double dewbar_al42_error = h_dewbar_sum->GetBinError(3); 
   double dewbar_fe54_error = h_dewbar_sum->GetBinError(4); 
   double dewbar_fe43_error = h_dewbar_sum->GetBinError(5); 
   double dewbar_ca43_error = h_dewbar_sum->GetBinError(6); 
   double dewbar_ca32_error = h_dewbar_sum->GetBinError(7); 
   double dewbar_mg32_error = h_dewbar_sum->GetBinError(8); 

   double dewbar35_si32 =h_dewbar35_sum->GetBinContent(1); 
   double dewbar35_al43 =h_dewbar35_sum->GetBinContent(2); 
   double dewbar35_al42 =h_dewbar35_sum->GetBinContent(3); 
   double dewbar35_fe54 =h_dewbar35_sum->GetBinContent(4); 
   double dewbar35_fe43 =h_dewbar35_sum->GetBinContent(5); 
   double dewbar35_ca43 =h_dewbar35_sum->GetBinContent(6)-0.172*h_dewbar35_sum->GetBinContent(10); 
   double dewbar35_ca32 =h_dewbar35_sum->GetBinContent(7)-0.172*h_dewbar35_sum->GetBinContent(10); 
   double dewbar35_mg32 =h_dewbar35_sum->GetBinContent(8); 
   double dewbar35_si32_error = h_dewbar35_sum->GetBinError(1); 
   double dewbar35_al43_error = h_dewbar35_sum->GetBinError(2); 
   double dewbar35_al42_error = h_dewbar35_sum->GetBinError(3); 
   double dewbar35_fe54_error = h_dewbar35_sum->GetBinError(4); 
   double dewbar35_fe43_error = h_dewbar35_sum->GetBinError(5); 
   double dewbar35_ca43_error = h_dewbar35_sum->GetBinError(6); 
   double dewbar35_ca32_error = h_dewbar35_sum->GetBinError(7); 
   double dewbar35_mg32_error = h_dewbar35_sum->GetBinError(8); 


   // ***** figure-1 *****
   c[0][hist_id] = new TCanvas(Form("c1_%d",hist_id),Form("c1_%d",hist_id),0,0,1000,800);
   fline[0][hist_id] = new TF1(Form("fline_1_%d",hist_id),"pol1",0,1);
//   fline[0][hist_id]->FixParameter(0,0);
   fline[0][hist_id]->SetLineColor(2);
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
   gr[0][hist_id] = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr[0][hist_id]->SetMarkerStyle(8);
   gr[0][hist_id]->SetMarkerSize(1);
   gr[0][hist_id]->SetMarkerColor(4);
#if not defined(__reference__)
   gr[0][hist_id]->SetTitle(";Al(4-2)/Si(3-2), black->dew->white;Al(4-3)/Si(3-2)");
   gr[0][hist_id]->GetXaxis()->CenterTitle(); 
   gr[0][hist_id]->GetYaxis()->CenterTitle();
   fline[0][hist_id]->SetTitle(";Al(4-2)/Si(3-2), black->dew->white;Al(4-3)/Si(3-2)");
   fline[0][hist_id]->GetXaxis()->CenterTitle(); 
   fline[0][hist_id]->GetYaxis()->CenterTitle();
#else
   gr[0][hist_id]->SetTitle(";Al/Si ref., black->dew->white;Al(4-2)/Si(3-2)");
   gr[0][hist_id]->GetXaxis()->CenterTitle(); 
   gr[0][hist_id]->GetYaxis()->CenterTitle();
   fline[0][hist_id]->SetTitle(";Al/Si ref., black->dew->white;Al(4-2)/Si(3-2)");
   fline[0][hist_id]->GetXaxis()->CenterTitle(); 
   fline[0][hist_id]->GetYaxis()->CenterTitle();
#endif
   gr[0][hist_id]->Draw("AP");
   grfit[0][hist_id] = new TGraph(np,x,y);
   std::cout << " Al fitting " << std::endl;
   grfit[0][hist_id]->Fit(Form("fline_1_%d",hist_id),"qn");
   fline[0][hist_id]->Draw("same");
   c[0][hist_id]->SaveAs(Form("/Users/chiu.i-huan/Desktop/temp_output/integ_al%s_%d.pdf",h_addname,hist_id));
   std::cout << "Al | Y | " << " black " << y[1] << " dew " << y[2] << " dewbar " << y[3] << " dewbar35 " << y[4] << " white " << y[5] << std::endl;
   std::cout << "Al | X | " << " black " << x[1] << " dew " << x[2] << " dewbar " << x[3] << " dewbar35 " << x[4] << " white " << x[5] << std::endl;



   // ***** figure-2 *****
   c[1][hist_id] = new TCanvas(Form("c2_%d",hist_id),Form("c2_%d",hist_id),0,0,1000,800);
   fline[1][hist_id] = new TF1(Form("fline_2_%d",hist_id),"pol1",0,1);
//   fline[1][hist_id]->FixParameter(0,0);
   fline[1][hist_id]->SetLineColor(2);
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
   gr[1][hist_id] = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr[1][hist_id]->SetMarkerStyle(8);
   gr[1][hist_id]->SetMarkerSize(1);
   gr[1][hist_id]->SetMarkerColor(4);
#if not defined(__reference__)
   gr[1][hist_id]->SetTitle(";Fe(4-3)/Si(3-2), white->dew->black;Fe(5-4)/Si(3-2)");
   gr[1][hist_id]->GetXaxis()->CenterTitle(); 
   gr[1][hist_id]->GetYaxis()->CenterTitle();
   fline[1][hist_id]->SetTitle(";Fe(4-3)/Si(3-2), white->dew->black;Fe(5-4)/Si(3-2)");
   fline[1][hist_id]->GetXaxis()->CenterTitle(); 
   fline[1][hist_id]->GetYaxis()->CenterTitle();
#else
   gr[1][hist_id]->SetTitle(";Fe/Si ref., white->dew->black;Fe(5-4)/Si(3-2)");
   gr[1][hist_id]->GetXaxis()->CenterTitle(); 
   gr[1][hist_id]->GetYaxis()->CenterTitle();
   fline[1][hist_id]->SetTitle(";Fe/Si ref., white->dew->black;Fe(5-4)/Si(3-2)");
   fline[1][hist_id]->GetXaxis()->CenterTitle(); 
   fline[1][hist_id]->GetYaxis()->CenterTitle();
#endif
   gr[1][hist_id]->Draw("AP");
   grfit[1][hist_id] = new TGraph(np,x,y);
   std::cout << " Fe fitting " << std::endl;
   grfit[1][hist_id]->Fit(Form("fline_2_%d",hist_id),"qn");
   fline[1][hist_id]->Draw("same");
   c[1][hist_id]->SaveAs(Form("/Users/chiu.i-huan/Desktop/temp_output/integ_fe%s_%d.pdf",h_addname,hist_id));
   std::cout << "Fe | Y | " << " black " << y[5] << " dew " << y[4] << " dewbar " << y[3] << " dewbar35 " << y[2] << " white " << y[1] << std::endl;
   std::cout << "Fe | X | " << " black " << x[5] << " dew " << x[4] << " dewbar " << x[3] << " dewbar35 " << x[2] << " white " << x[1] << std::endl;



   // ***** figure-3 *****
   c[2][hist_id] = new TCanvas(Form("c3_%d",hist_id),Form("c3_%d",hist_id),0,0,1000,800);
   fline[2][hist_id] = new TF1(Form("fline_3_%d",hist_id),"pol1",0,1);
//   fline[2][hist_id]->FixParameter(0,0);
   fline[2][hist_id]->SetLineColor(2);
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
   x[5]=black_ca32/black_si32;
   xe[5]=black_ca32/black_si32*(sqrt(pow(black_ca32_error/black_ca32,2)+pow(black_si32_error/black_si32,2)));
   x[4] =dew_ca32/dew_si32;
   xe[4]=dew_ca32/dew_si32*(sqrt(pow(dew_ca32_error/dew_ca32,2)+pow(dew_si32_error/dew_si32,2)));
   x[3] =dewbar_ca32/dewbar_si32;
   xe[3]=dewbar_ca32/dewbar_si32*(sqrt(pow(dewbar_ca32_error/dewbar_ca32,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   x[2] =dewbar35_ca32/dewbar35_si32;
   xe[2]=dewbar35_ca32/dewbar35_si32*(sqrt(pow(dewbar35_ca32_error/dewbar35_ca32,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   x[1] =white_ca32/white_si32;
   xe[1]=white_ca32/white_si32*(sqrt(pow(white_ca32_error/white_ca32,2)+pow(white_si32_error/white_si32,2)));
#if defined(__reference__)
   y[5]=black_ca32/black_si32;
   y[4]=dew_ca32/dew_si32;
   y[3]=dewbar_ca32/dewbar_si32;
   y[2]=dewbar35_ca32/dewbar35_si32;
   y[1]=white_ca32/white_si32;
   ye[5]=black_ca32/black_si32*(sqrt(pow(black_ca32_error/black_ca32,2)+pow(black_si32_error/black_si32,2)));
   ye[4]=dew_ca32/dew_si32*(sqrt(pow(dew_ca32_error/dew_ca32,2)+pow(dew_si32_error/dew_si32,2)));
   ye[3]=dewbar_ca32/dewbar_si32*(sqrt(pow(dewbar_ca32_error/dewbar_ca32,2)+pow(dewbar_si32_error/dewbar_si32,2)));
   ye[2]=dewbar35_ca32/dewbar35_si32*(sqrt(pow(dewbar35_ca32_error/dewbar35_ca32,2)+pow(dewbar35_si32_error/dewbar35_si32,2)));
   ye[1]=white_ca32/white_si32*(sqrt(pow(white_ca32_error/white_ca32,2)+pow(white_si32_error/white_si32,2)));
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
   gr[2][hist_id] = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr[2][hist_id]->SetMarkerStyle(8);
   gr[2][hist_id]->SetMarkerSize(1);
   gr[2][hist_id]->SetMarkerColor(4);
#if not defined(__reference__)
   gr[2][hist_id]->SetTitle(";Ca(3-2)/Si(3-2), white->dew->black;Ca(4-3)/Si(3-2)");
   gr[2][hist_id]->GetXaxis()->CenterTitle(); 
   gr[2][hist_id]->GetYaxis()->CenterTitle();
   fline[2][hist_id]->SetTitle(";Ca(3-2)/Si(3-2), white->dew->black;Ca(4-3)/Si(3-2)");
   fline[2][hist_id]->GetXaxis()->CenterTitle(); 
   fline[2][hist_id]->GetYaxis()->CenterTitle();
#else
   gr[2][hist_id]->SetTitle(";Ca/Si ref., white->dew->black;Ca(3-2)/Si(3-2)");
   gr[2][hist_id]->GetXaxis()->CenterTitle(); 
   gr[2][hist_id]->GetYaxis()->CenterTitle();
   fline[2][hist_id]->SetTitle(";Ca/Si ref., white->dew->black;Ca(3-2)/Si(3-2)");
   fline[2][hist_id]->GetXaxis()->CenterTitle(); 
   fline[2][hist_id]->GetYaxis()->CenterTitle();
#endif
   gr[2][hist_id]->Draw("AP");
   grfit[2][hist_id] = new TGraph(np,x,y);
   std::cout << " Ca fitting " << std::endl;
   grfit[2][hist_id]->Fit(Form("fline_3_%d",hist_id),"qn");
   fline[2][hist_id]->Draw("same");
   c[2][hist_id]->SaveAs(Form("/Users/chiu.i-huan/Desktop/temp_output/integ_ca%s_%d.pdf",h_addname,hist_id));
   std::cout << "Ca | Y | " << " black " << y[5] << " dew " << y[4] << " dewbar " << y[3] << " dewbar35 " << y[2] << " white " << y[1] << std::endl;
   std::cout << "Ca | X | " << " black " << x[5] << " dew " << x[4] << " dewbar " << x[3] << " dewbar35 " << x[2] << " white " << x[1] << std::endl;



   // ***** figure-4 *****
   c[3][hist_id] = new TCanvas(Form("c4_%d",hist_id),Form("c4_%d",hist_id),0,0,1000,800);
   fline[3][hist_id] = new TF1(Form("fline_4_%d",hist_id),"pol1",0,1);
//   fline[3][hist_id]->FixParameter(0,0);
   fline[3][hist_id]->SetLineColor(2);
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
   gr[3][hist_id] = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr[3][hist_id]->SetMarkerStyle(8);
   gr[3][hist_id]->SetMarkerSize(1);
   gr[3][hist_id]->SetMarkerColor(4);
   gr[3][hist_id]->SetTitle(";Mg/Si ref., white->dew->black;Mg(3-2)/Si(3-2)");
   gr[3][hist_id]->GetXaxis()->CenterTitle(); 
   gr[3][hist_id]->GetYaxis()->CenterTitle();
   fline[3][hist_id]->SetTitle(";Mg/Si ref., white->dew->black;Mg(3-2)/Si(3-2)");
   fline[3][hist_id]->GetXaxis()->CenterTitle(); 
   fline[3][hist_id]->GetYaxis()->CenterTitle();
   gr[3][hist_id]->Draw("AP");
   grfit[3][hist_id] = new TGraph(np,x,y);
   std::cout << " Mg fitting " << std::endl;
   grfit[3][hist_id]->Fit(Form("fline_4_%d",hist_id),"qn");
   fline[3][hist_id]->Draw("same");
   c[3][hist_id]->SaveAs(Form("/Users/chiu.i-huan/Desktop/temp_output/integ_mg%s_%d.pdf",h_addname,hist_id));
   std::cout << "Mg | Y | " << " black " << y[5] << " dew " << y[4] << " dewbar " << y[3] << " dewbar35 " << y[2] << " white " << y[1] << std::endl;
   std::cout << "Mg | X | " << " black " << x[5] << " dew " << x[4] << " dewbar " << x[3] << " dewbar35 " << x[2] << " white " << x[1] << std::endl;



   // ***** figure-4 *****
   c[4][hist_id] = new TCanvas(Form("c5_%d",hist_id),Form("c5_%d",hist_id),0,0,1000,800);
   fline[4][hist_id] = new TF1(Form("fline_5_%d",hist_id),"pol1",0,1);
//   fline[4][hist_id]->FixParameter(0,0);
   fline[4][hist_id]->SetLineColor(2);
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
   gr[4][hist_id] = new TGraphAsymmErrors(np,x,y,xe,xe,ye,ye);
   gr[4][hist_id]->SetMarkerStyle(8);
   gr[4][hist_id]->SetMarkerSize(1);
   gr[4][hist_id]->SetMarkerColor(4);
   gr[4][hist_id]->SetTitle(";Fe(5-4)/Si(3-2), white->dew->black;Al(4-2)/Si(3-2)");
   gr[4][hist_id]->GetXaxis()->CenterTitle(); 
   gr[4][hist_id]->GetYaxis()->CenterTitle();
   fline[4][hist_id]->SetTitle(";Fe(5-4)/Si(3-2), white->dew->black;Al(4-2)/Si(3-2)");
   fline[4][hist_id]->GetXaxis()->CenterTitle(); 
   fline[4][hist_id]->GetYaxis()->CenterTitle();
   gr[4][hist_id]->Draw("AP");
   grfit[4][hist_id] = new TGraph(np,x,y);
   grfit[4][hist_id]->Fit(Form("fline_5_%d",hist_id),"qn");
//   fline[4][hist_id]->Draw("same");
   c[4][hist_id]->SaveAs(Form("/Users/chiu.i-huan/Desktop/temp_output/comparison_feal_iter_%d.pdf",hist_id));
   std::cout << " Fe vs. Al " << std::endl;
   std::cout << "Al | Y | " << " black " << y[5] << " dew " << y[4] << " dewbar " << y[3] << " dewbar35 " << y[2] << " white " << y[1] << std::endl;
   std::cout << "Fe | X | " << " black " << x[5] << " dew " << x[4] << " dewbar " << x[3] << " dewbar35 " << x[2] << " white " << x[1] << std::endl;

   } //loop hist_id


   // *** store all hist. ***
   TFile* fout = new TFile(Form("./comparison_output%s.root", h_addname),"recreate");
   fout->cd();
   for(int i = 0; i < 5; i++){
      for(int j = 0; j < 7; j++){
         fline[i][j]->Write();
         gr[i][j]->SetName(Form("gr_%d_%d",i,j));
         grfit[i][j]->SetName(Form("grfit_%d_%d",i,j));
         gr[i][j]->Write();
         grfit[i][j]->Write();
      }
   }
} 

