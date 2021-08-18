/// \file
/// \ingroup tutorial_spectrum
/// \notebook
/// Getting Contours From TH2D.
/// Illustrates how to find peaks in histograms.
///
/// This script generates a random number of gaussian peaks
/// on top of a linear background.
/// The position of the peaks is found via TSpectrum and injected
/// as initial values of parameters to make a global fit.
/// The background is computed and drawn on top of the original histogram.
///
/// This script can fit "peaks' heights" or "peaks' areas" (comment out
/// or uncomment the line which defines `__PEAKS_C_FIT_AREAS__`).
///
/// To execute this example, do (in ROOT 5 or ROOT 6):
///
/// ~~~{.cpp}
///  root > .x peaks.C  (generate 10 peaks by default)
///  root > .x peaks.C++ (use the compiler)
///  root > .x peaks.C++(30) (generates 30 peaks)
/// ~~~
///
/// To execute only the first part of the script (without fitting)
/// specify a negative value for the number of peaks, eg
///
/// ~~~{.cpp}
///  root > .x peaks.C(-20)
/// ~~~
///
/// \macro_output
/// \macro_image
/// \macro_code
///
/// \author Rene Brun

#include "TCanvas.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TRandom.h"
#include "TSpectrum.h"
#include "TVirtualFitter.h"

//
// Comment out the line below, if you want "peaks' heights".
// Uncomment the line below, if you want "peaks' areas".
//

//#define __PEAKS_C_FIT_AREAS__ 1 /* fit peaks' areas */

Int_t np=50;
Int_t myEnergy_min=0;
//const char *f_name = "/Users/chiu.i-huan/Desktop/new_scientific/CdTe123/data/J-PARC2021JuneCdTe123/live_data0715_Ba133.mca.root";
const char *f_name = "/Users/chiu.i-huan/Desktop/new_scientific/CdTe123/data/J-PARC2021JuneCdTe123/live_data0715_Co57.mca.root";

Int_t npeaks;//maximum
Double_t fpeaks(Double_t *x, Double_t *par) {
   Double_t result = par[0] + par[1]*x[0];
   for (Int_t p=0;p<npeaks;p++) {
      Double_t norm  = par[3*p+2]; // "height" or "area"
      Double_t mean  = par[3*p+3];
      Double_t sigma = par[3*p+4];
#if defined(__PEAKS_C_FIT_AREAS__)
      norm /= sigma * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
      result += norm*TMath::Gaus(x[0],mean,sigma);
   }
   return result;
}
void peaks() {
   TFile* fout = new TFile("./findpeak.root","recreate");

   npeaks = TMath::Abs(np);

   TFile *ff = new TFile(f_name,"read");
   TTree *tt = (TTree*)ff->Get("tree");
   tt->Draw("energy >> h(600,0,150)");
   TH1D* h=(TH1D*)gDirectory->Get("h");
   fout->cd();
   h->Write();

   Int_t Energy_max=h->GetXaxis()->GetXmax();
   Int_t Energy_min=h->GetXaxis()->GetXmin();
   if (Energy_min < myEnergy_min){
      Energy_min = myEnergy_min;
      h->GetXaxis()->SetRangeUser(Energy_min,Energy_max);
   }

   //generate n peaks at random
   Double_t par[3000];
   par[0] = 5;
   par[1] = -0.6/1000;
   Int_t p;
   for (p=0;p<npeaks;p++) {
      par[3*p+2] = 50; // "height"
      par[3*p+3] = Energy_min+gRandom->Rndm()*Energy_max; // "mean", gRandom->Rndm(): 0~1
      par[3*p+4] = 0.1+0.5*gRandom->Rndm(); // "sigma"
#if defined(__PEAKS_C_FIT_AREAS__)
      par[3*p+2] *= par[3*p+4] * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
   }
   TF1 *f = new TF1("f",fpeaks,Energy_min,Energy_max,2+3*npeaks);//name, fcn, xmin, xmax, npar (three par. for each peak)
   f->SetNpx(10000);
   f->SetParameters(par);
   TCanvas *c1 = new TCanvas("c1","c1",10,10,1000,900);
   c1->Divide(1,2);
   c1->cd(1);
   h->Draw();
   TH1F *h2 = (TH1F*)h->Clone("h2");
   //Use TSpectrum to find the peak candidates
   TSpectrum *s = new TSpectrum(npeaks);
   s->SetResolution(1);//determines resolution of the neighbouring peaks default value is 1 correspond to 3 sigma distance between peaks.
   Int_t nfound = s->Search(h,0.1,"",0.001);
   printf("Found %d candidate peaks to fit\n",nfound);
   
   //Estimate background using TSpectrum::Background
   TH1 *hb = s->Background(h,20,"same");
   if (hb) c1->Update();
   if (np <0) return;

    // ***********************************************************************************************************************************
   //estimate linear background using a fitting method
   c1->cd(2);
   TF1 *fline = new TF1("fline","pol1",0,Energy_max);
   h->Fit("fline","qn");
   //Loop on all found peaks. Eliminate peaks at the background level
   par[0] = fline->GetParameter(0);
   par[1] = fline->GetParameter(1);
   npeaks = 0;
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,00,00)
   Double_t *xpeaks; // ROOT 6
#else
   Float_t *xpeaks; // ROOT 5
#endif
   xpeaks = s->GetPositionX();
   for (p=0;p<nfound;p++) {
      Double_t xp = xpeaks[p];
      std::cout << " Found peak at : " << xp << " (Index "<<p+1<< ")" << std::endl;
      Int_t bin = h->GetXaxis()->FindBin(xp);
      Double_t yp = h->GetBinContent(bin);
      if (yp-TMath::Sqrt(yp) < fline->Eval(xp)) continue;
      //Set initial range
      par[3*npeaks+2] = yp; // "height"
      par[3*npeaks+3] = xp; // "mean"
      par[3*npeaks+4] = 0.2; // "sigma"
#if defined(__PEAKS_C_FIT_AREAS__)
      par[3*npeaks+2] *= par[3*npeaks+4] * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
      npeaks++;
   }
   printf("Found %d useful peaks to fit\n",npeaks);
   printf("Now fitting: Be patient\n");
   TF1 *fit = new TF1("fit",fpeaks,Energy_min,Energy_max,2+3*npeaks);
   //we may have more than the default 25 parameters
   TVirtualFitter::Fitter(h2,10+3*npeaks);
   fit->SetParameters(par);
   for (p=0;p<nfound;p++) { 
     Double_t xp = xpeaks[p];
      //Fix fitting range
//     fit->FixParameter(3*p+3,xp);
     fit->SetParLimits(3*p+3,xp-2,xp+2);
     fit->SetParLimits(3*p+4,0,0.5);
   }
   fit->SetNpx(10000);
   h2->Fit("fit","q");
   c1->SaveAs("./findpeak.pdf");
   std::cout << " Chisquare : " << f->GetChisquare() << std::endl;
   for (p=0;p<nfound;p++) {
#if defined(__PEAKS_C_FIT_AREAS__)
      std::cout << " Index : " << p+1 << fixed << setprecision(3)
                << "  Energy : "<< fit->GetParameter(3*p+3) << " \u00b1 " << fit->GetParError(3*p+3) 
                << "  Sigma : " << fit->GetParameter(3*p+4) << " \u00b1 " << fit->GetParError(3*p+4)
                << "  Area : "  << fit->GetParameter(3*p+2) << " \u00b1 " << fit->GetParError(3*p+2)
                << std::endl;
#else
      ROOT::Math::IntegratorOneDimOptions::SetDefaultRelTolerance(1.E-12);
      Double_t error;
      Double_t error_bkg;
      Int_t bin_up = h2->FindBin(fit->GetParameter(3*p+3)+3*fit->GetParameter(3*p+4));
      Int_t bin_down = h2->FindBin(fit->GetParameter(3*p+3)-3*fit->GetParameter(3*p+4));
      TF1 *f_temp = new TF1("f_temp","gaus",Energy_min,Energy_max);
      f_temp->FixParameter(0,fit->GetParameter(3*p+2));//height
      f_temp->FixParameter(1,fit->GetParameter(3*p+3));//mean
      f_temp->FixParameter(2,fit->GetParameter(3*p+4));//sigma
      if (fit->GetParameter(3*p+2) == 0 || fit->GetParameter(3*p+3) == 0 || fit->GetParameter(3*p+4) == 0) continue;
      TLine* lup = new TLine(fit->GetParameter(3*p+3)+3*fit->GetParameter(3*p+4),0,fit->GetParameter(3*p+3)+3*fit->GetParameter(3*p+4),1000);
      TLine* ldown = new TLine(fit->GetParameter(3*p+3)-3*fit->GetParameter(3*p+4),0,fit->GetParameter(3*p+3)-3*fit->GetParameter(3*p+4),1000);
      std::cout << " Index : " << p+1 << fixed << setprecision(1)
                << "  Energy : " << fit->GetParameter(3*p+3) << " \u00b1 "   << fit->GetParError(3*p+3) 
                << "  Sigma : "  << fit->GetParameter(3*p+4) << " \u00b1 "   << fit->GetParError(3*p+4)
                << "  Height : " << fit->GetParameter(3*p+2) << " \u00b1 " << fit->GetParError(3*p+2)
//                << "  Area : "  << f_temp->Integral(Energy_min,Energy_max) 
//                << "  bin up : "  << bin_up << " bin down : " << bin_down
//                << "  Area peak : "  << h2->IntegralAndError(bin_down,bin_up,error) << " Area bkg : " << hb->IntegralAndError(bin_down,bin_up,error_bkg)
                << "  Signal : "  << h2->IntegralAndError(bin_down,bin_up,error)-hb->IntegralAndError(bin_down,bin_up,error_bkg) << " \u00b1 " << sqrt(error*error+error_bkg*error_bkg)
                << "  Area : "  << h2->IntegralAndError(bin_down,bin_up,error) << " \u00b1 " << error << " BKG : " << hb->IntegralAndError(bin_down,bin_up,error_bkg) << " \u00b1 " << error_bkg
                << std::endl;
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
      lup->SetLineColor(9);
      ldown->SetLineColor(5);
      f_temp->SetLineColor(3);
      f_temp->Draw("same C");
      lup->Draw("same");
      ldown->Draw("same");
   }
   hb->Write();fline->Write();fit->Write();
   fout->Write();

}

#if !defined(__CINT__) && defined(__PEAKS_C_FIT_AREAS__)
#undef __PEAKS_C_FIT_AREAS__
#endif /* !defined(__CINT__) && defined(__PEAKS_C_FIT_AREAS__) */
